from logging import Logger
from rq.job import Job
from models import DbConnection
from models import ApiCreateResult
from DbSchemaReader import DbSchemaProvider
from shutil import copyfile
from flask import Flask, json, request, Response, jsonify
from filestack import Client
from builtins import any as b_any
from os.path import isfile, join
from os import listdir
from DbReader import AdminDbReader
from rq import Queue
from worker import conn
from flask_cors import CORS
import redis
import time
import os, sys
import subprocess
import uuid
import re
import shutil
import git
import inflect
import shlex
from api_client_creator import create_api_client, publish_package
import random as rng
import string
from rq.registry import FinishedJobRegistry, StartedJobRegistry
from ClientAppGenerator.app import create_client_frontend
sys.path.append('./ClientAppGenerator')

def create_model_files(dbconn):
    print('Generating model file....')
    script_path = ''
    model_guid = str(uuid.uuid4())

    if dbconn.DbType == 'mysql':
        script_path = './powershell-script/CreateModelFromMySQL.sh'
    if dbconn.DbType == 'mssql':
        script_path = './powershell-script/CreateModelFromMsSQL.sh'
    if dbconn.DbType == 'postgre':
        script_path = './powershell-script/CreateModelFromPostgreSQL.sh'

    command_list = shlex.split(script_path + ' ' +
                               dbconn.Server + ' ' +
                               dbconn.Database + ' ' +
                               dbconn.Username + ' ' +
                               dbconn.Password + ' ' +
                               model_guid + ' ' +
                               str(dbconn.ServerPort))
    p = subprocess.check_call(command_list)

    print('Done. \n')
    return model_guid


def get_list_model_name(modelguid, table_configs):
    model_path = './EFCoreScaffold/{0}'.format(modelguid)
    p = inflect.engine()
    chars = re.escape(string.punctuation)
    white_list = []
    for table in table_configs:
        white_list.append(table.Name.replace(' ', ''))

    only_files = [f[:-3] for f in listdir(model_path)
                  if isfile(join(model_path, f))
                  and b_any(
        f[:-3].lower() in x.lower() or f[:-3].lower() in str(p.singular_noun(re.sub(r'[' + chars + ']', '', x.lower()))) for x in white_list)
        and 'Context' not in f
    ]

    return only_files


def move_model_file_to_template_api(modelguid, tableconfigs):
    print('Refactoring created model files ....')
    for table in tableconfigs:
        filename = table.ModelName
        fin_path = os.path.join(
            './EFCoreScaffold', modelguid, filename + '.cs')
        fout_path = os.path.join(
            './CustomerTemplateAPI/CustomerTemplateAPI', 'Models', filename + '.cs')
        fin = open(fin_path, 'rt')
        fout = open(fout_path, 'w+')

        contents = fin.readlines()

        idx = 0
        contents.insert(0, 'using System.Text.Json.Serialization;\n')
        while idx < len(contents):
            if 'namespace EFCoreScaffoldexample' in contents[idx]:
                contents[idx] = 'namespace CustomerTemplateAPI.Models\n'
            if '[InverseProperty(' in contents[idx]:
                if '[ForeignKey(' not in contents[idx - 1]:
                    contents[idx] += '        [JsonIgnore]\n'
            idx += 1
        fout.write(''.join(contents))
    print('Done.\n')


def create_application_db_context_file(modelguid, tableconfigs):
    print('Creating ApplicationDbContext file ....')
    model_path = './EFCoreScaffold/{0}'.format(modelguid)
    src_context_file_name = next(f for f in listdir(model_path)
                                 if isfile(join(model_path, f)) and 'Context' in f
                                 )

    src_db_context_file_path = './EFCoreScaffold/{0}/{1}'.format(
        modelguid, src_context_file_name)
    dest_db_context_file_path = './CustomerTemplateAPI/CustomerTemplateAPI/Data/ApplicationDbContext.cs'

    with open(src_db_context_file_path, "r") as f:
        contents = f.readlines()
        contents.insert(2,
                        'using CustomerTemplateAPI.Models;\n'
                        'using Microsoft.AspNetCore.Identity.EntityFrameworkCore;\n'
                        'using Microsoft.AspNetCore.Identity;\n')

        pattern = '(?<=\<)(.*?)(?=\>)'
        idx = 0
        first_db_set = False
        while idx < len(contents):
            line = contents[idx]
            if 'public virtual DbSet<' in line and not any(x for x in tableconfigs if
                                                           re.search(pattern, line).group(1) == x.ModelName):
                contents[idx] = ''
                continue

            if 'modelBuilder.Entity<' in line and not any(x for x in tableconfigs if
                                                          re.search(pattern, line).group(1) == x.ModelName):
                while True:
                    if '            });\n' in contents[idx]:
                        contents[idx] = ''
                        break
                    contents[idx] = ''
                    idx += 1
                continue

            if 'namespace EFCoreScaffoldexample.{0}'.format(modelguid) in line:
                contents[idx] = 'namespace CustomerTemplateAPI.Data'
                continue

            if 'public partial class {0}'.format(src_context_file_name[:-3]) in line:
                contents[idx] = 'public partial class ApplicationDbContext : DbContext\n'
                continue
            if 'public partial class ApplicationDbContext : DbContext' in line:
                contents[
                    idx] = 'public partial class ApplicationDbContext : IdentityDbContext<ApplicationUser, IdentityRole, string>'

            if src_context_file_name[:-3] in line:
                contents[idx] = line.replace(
                    src_context_file_name[:-3], 'ApplicationDbContext')

            if 'protected override void OnModelCreating(ModelBuilder modelBuilder)' in line:
                contents[idx +
                         1] += '            base.OnModelCreating(modelBuilder);\n'

            if not first_db_set and 'public virtual DbSet<' in line:
                first_db_set = True
            if '#warning To protect potentially sensitive' in line:
                contents[idx] = ''
                contents[idx + 1] = ''

            idx += 1

        with open(dest_db_context_file_path, 'w') as w:
            w.write(''.join(contents))
        print('Done.\n')


def create_repositories(tableconfigs, columnconfigs):
    print('Create repositories and their interfaces ....')
    repository_template_file_path = './file-templates/TemplateRepository.cs'
    interface_template_file_path = './file-templates/TemplateRepositoryInterface.cs'
    destination_repository_file_path = './CustomerTemplateAPI/CustomerTemplateAPI/Repositories/{0}Repository.cs'
    destination_model_file_name = './CustomerTemplateAPI/CustomerTemplateAPI/Models/{0}.cs'
    destination_repository_interface_file_path = \
        './CustomerTemplateAPI/CustomerTemplateAPI/Repositories/Interfaces/I{0}Repository.cs'

    with open(repository_template_file_path, "r") as f:
        repo_contents = f.readlines()

    with open(interface_template_file_path, 'r') as f:
        repo_interface_contents = f.readlines()

    for current_table in tableconfigs:
        if current_table.IsHidden == 1:
            continue

        primary_keys = sorted([w for w in columnconfigs if w.TableId == current_table.Id
                               and w.IsPrimaryKey == 1], key=lambda x: x.OrdinalPosition)

        foreign_keys = list((w for w in columnconfigs if w.TableId == current_table.Id
                             and w.IsForeignKey == 1))
        pk_params = ''
        params_assign = ''

        for idx in range(len(primary_keys)):
            key = primary_keys[idx]
            field_name = key.PropertyName.lower()
            pk_data_type_net = db_to_net_data_type_convert(key.DataType)
            pk_params += '{0} {1},'.format(pk_data_type_net, field_name)
            params_assign += 'parameters[{0}] = {1};\n'.format(
                str(idx), field_name)
        pk_params = pk_params[:-1]

        with open(destination_model_file_name.format(current_table.ModelName), 'r') as f:
            model_contents = f.readlines()

        with open(destination_repository_interface_file_path.format(current_table.ModelName), 'w') as w:
            new_contents = []
            for line in repo_interface_contents:
                new_contents.append(
                    line.replace('---InterfaceName---',
                                 'I{0}Repository'.format(current_table.ModelName))
                    .replace('---ModelName---', current_table.ModelName)
                    .replace('---FKParams---', pk_params))
            w.write(''.join(new_contents))
            w.close()

        with open(destination_repository_file_path.format(current_table.ModelName), "w") as w:
            new_contents = []
            idx = 0
            while idx < len(repo_contents):
                line = repo_contents[idx]
                if 'return GetAll().AsQueryable();' in line:
                    internal_idx = 0
                    while internal_idx < len(model_contents):
                        if '[ForeignKey(nameof(' in model_contents[internal_idx]:
                            condition = True
                            fk_count = 0
                            include_clause = ''
                            while condition:
                                internal_idx += 1
                                if 'public virtual' in model_contents[internal_idx]:
                                    include_clause += '.Include(m => m.{0})'.format(
                                        model_contents[internal_idx].split()[3])
                                    fk_count += 1
                                if internal_idx == len(model_contents) - 1 or fk_count == len(foreign_keys):
                                    line = line[:-2] + \
                                        include_clause + line[-2:]
                                    condition = False
                        internal_idx += 1
                if '---FKParams---' in line:
                    line = line.replace('---FKParams---', pk_params)
                if '// Some binding here' in line:
                    line = line.replace('// Some binding here', params_assign)
                if '<--NumberOfFK-->' in line:
                    line = line.replace('<--NumberOfFK-->',
                                        str(len(primary_keys)))

                new_contents.append(line
                                    .replace('---RepositoryName---', '{0}Repository'.format(current_table.ModelName))
                                    .replace('---ModelName---', current_table.ModelName)
                                    .replace('---InterfaceName---', 'I{0}Repository'.format(current_table.ModelName)))
                idx += 1
            w.write(''.join(new_contents))
            w.close()
    print('Done.\n')


def edit_startup_file(tableconfigs, servertype):
    print('Configuring startup file ....')
    startup_file_path = './CustomerTemplateAPI/CustomerTemplateAPI/Startup.cs'
    with open(startup_file_path, "r") as r:
        contents = r.readlines()
        new_contents = []
        idx = 0
        while idx < len(contents):
            line = contents[idx]
            if 'ApplicationDbContext DI declare' in line:
                if servertype == 'mysql':
                    line = '            services.AddDbContext<ApplicationDbContext>(options =>\n' \
                           '            {\n' \
                           '                options.UseMySql(Configuration.GetConnectionString("DefaultConnection"),\n' \
                           '                    Microsoft.EntityFrameworkCore.ServerVersion.FromString("8.0.23-mysql"));\n' \
                           '            });\n'
                elif servertype == 'mssql':
                    line = '            services.AddDbContext<ApplicationDbContext>(options =>\n' \
                           '            {\n' \
                           '                options\n' \
                           '                .UseSqlServer(\n' \
                           '                    Configuration.GetConnectionString("DefaultConnection"),\n' \
                           '                                    optionsBuilder => optionsBuilder.MigrationsAssembly("CustomerTemplateAPI"));\n' \
                           '            });\n'
                elif servertype == 'postgre':
                    line = '            services.AddDbContext<ApplicationDbContext>(options =>\n' \
                           '            {\n' \
                           '                options\n' \
                           '                .UseNpgsql(\n' \
                           '                    Configuration.GetConnectionString("DefaultConnection"),\n' \
                           '                                    optionsBuilder => optionsBuilder.MigrationsAssembly("CustomerTemplateAPI"));\n' \
                           '            });\n'
            elif 'Repository DI declare' in line:
                line = ''
                for table in tableconfigs:
                    if table.IsHidden == 1:
                        continue
                    line += '            services.AddScoped<I{0}Repository,{0}Repository>();\n'.format(
                        table.ModelName)
            new_contents.append(line)
            idx += 1

    with open(startup_file_path, 'w') as w:
        w.write(''.join(new_contents))
    print('Done. \n')


def populate_model_name(tableconfigs, columnconfigs, modelguid):
    model_path = './EFCoreScaffold/{0}'.format(modelguid)
    model_file_path = './EFCoreScaffold/{0}/{1}.cs'
    model_file_list = [f[:-3]
                       for f in listdir(model_path) if isfile(join(model_path, f))]
    p = inflect.engine()
    chars = re.escape(string.punctuation)
    for tbl_idx in range(len(tableconfigs)):
        clean_tbl_name = re.sub(r'[' + chars + ']', '', tableconfigs[tbl_idx].Name.lower().replace(' ', ''))
        if str(p.singular_noun(clean_tbl_name)) != 'False':
            clean_tbl_name = p.singular_noun(clean_tbl_name)

        for correspond_model_name in model_file_list:
            if correspond_model_name.lower() == clean_tbl_name:
                tableconfigs[tbl_idx].ModelName = correspond_model_name
                break
        with open(model_file_path.format(modelguid, tableconfigs[tbl_idx].ModelName), 'r') as r:
            model_contents = r.readlines()
            for content_idx in range(len(model_contents)):
                line = model_contents[content_idx]
                if '[Column("' in line:
                    expression = '(?<=\")(.*?)(?=\")'
                    model_column_name = re.search(expression, line).group(0)
                    if model_column_name is None:
                        continue
                    correspond_column = next(r for r in columnconfigs if r.ColumnName == model_column_name
                                             and r.TableId == tableconfigs[tbl_idx].Id)
                    while True:
                        content_idx += 1
                        if '{ get; set; }' in model_contents[content_idx]:
                            correspond_column.PropertyName = model_contents[content_idx].split()[
                                2]
                            break
                elif '{ get; set; }' in line:
                    model_column_name = line.split()[2]
                    correspond_column = None
                    for column in columnconfigs:
                        if column.ColumnName == model_column_name and column.TableId == tableconfigs[tbl_idx].Id:
                            correspond_column = column
                            break

                    if correspond_column is not None:
                        correspond_column.PropertyName = model_column_name
                        
                        
def generate_conn_str(conn_info):
    if conn_info.DbType == 'mssql':
        return 'Data Source={0},{4};Initial Catalog={1};User ID={2};Password={3}'.format(conn_info.Server, conn_info.Database, conn_info.Username, conn_info.Password, conn_info.ServerPort)
    elif conn_info.DbType == 'mysql':
        return 'Data Source={0};Port={4};Initial Catalog={1};User ID={2};Password={3}'.format(conn_info.Server, conn_info.Database, conn_info.Username, conn_info.Password, conn_info.ServerPort)
    elif conn_info.DbType == 'postgre':
        return 'Host={0};Port={4};Database={1};Username={2};Password={3}'.format(conn_info.Server, conn_info.Database, conn_info.Username, conn_info.Password, conn_info.ServerPort)

def get_random_string(length):
    letters = string.ascii_letters + string.digits
    result_str = ''.join(rng.choice(letters) for i in range(length))
    return result_str

def update_appsettings(conn_info):
    print('Updating appsettings.json ...')
    file_path = './CustomerTemplateAPI/CustomerTemplateAPI/appsettings.json'
    with open(file_path, "r") as r:
        contents = r.readlines()
        new_contents = []
        idx = 0
        while idx < len(contents):
            line = contents[idx]
            if '---ConnectionStringHere---' in line:
                line = line.replace('---ConnectionStringHere---', generate_conn_str(conn_info))
            elif '---JWTSecretKeyHere---' in line:
                line = line.replace('---JWTSecretKeyHere---', get_random_string(60)) 
            new_contents.append(line)
            idx += 1
            
        with open(file_path, 'w') as w:
            w.write(''.join(new_contents))
    print('Done.')

def create_customer_api(dbconn, db_guid):
    try:
        model_guid = create_model_files(dbconn)
        (table_configs, column_configs) = DbSchemaProvider().get_schema(dbconn)
        reset_template_api_repo()
        populate_model_name(table_configs, column_configs, model_guid)
        create_application_db_context_file(model_guid, table_configs)
        move_model_file_to_template_api(model_guid, table_configs)
        create_repositories(table_configs, column_configs)
        create_api_controller(table_configs, column_configs)
        edit_startup_file(table_configs, dbconn.DbType)
        update_appsettings(dbconn)
        update_schema_names(dbconn, table_configs, column_configs)
        delete_used_generated_model(model_guid)
        file_link = upload_customer_api_to_filestack(model_guid)
        get_swagger_file(model_guid)
        package_identifier = create_api_client(model_guid)
        publish_package(package_identifier)
        api_base_path = 'http://vuonghuynhsolutions.tech:8808'
        client_app_guid, client_app_download_link = create_client_frontend(db_guid, api_base_path, str(package_identifier))
        print(model_guid)
        print(file_link)
        return model_guid, file_link, package_identifier, client_app_guid, client_app_download_link
    except Exception as ex:
        print(ex)
        raise ex
    finally:
        reset_template_api_repo()
        delete_used_generated_model(model_guid)



def update_schema_names(dbconn, tableconfigs, columnconfigs):
    DbSchemaProvider().update_model_name_for_table_config(dbconn, tableconfigs)
    DbSchemaProvider().update_property_name_for_table_column_config(dbconn, columnconfigs)


def create_api_controller(tableconfigs, columnconfigs):
    controller_template_file_path = './file-templates/TemplateController.cs'
    controller_write_path = './CustomerTemplateAPI/CustomerTemplateAPI/Controllers/{0}Controller.cs'
    with open(controller_template_file_path, 'r') as r:
        contents = r.readlines()
        list_visible_table = [w for w in tableconfigs if w.IsHidden == 0]
        for visible_table in list_visible_table:
            new_contents = []
            primary_keys = sorted([w for w in columnconfigs if w.TableId == visible_table.Id
                                   and w.IsPrimaryKey == 1], key=lambda x: x.OrdinalPosition)
            pk_params = ''
            pass_params = ''
            params_assign = ''
            post_fk_call_params_assign = ''
            put_fk_call_params_assign = ''
            delete_fk_call_params = ''
            delete_not_found_params = ''

            for idx in range(len(primary_keys)):
                key = primary_keys[idx]
                field_name = key.PropertyName.lower()
                pk_data_type_net = db_to_net_data_type_convert(key.DataType)
                pk_params += '{0} {1}, '.format(pk_data_type_net, field_name)
                params_assign += 'parameters[{0}] = {1};\n'.format(
                    str(idx), field_name)
                post_fk_call_params_assign += 'newItem.{}, '.format(
                    key.PropertyName)
                put_fk_call_params_assign += 'updatedItem.{}, '.format(
                    key.PropertyName)
                delete_fk_call_params += field_name + ', '
                pass_params += field_name + ', '
            pk_params = pk_params[:-2]
            post_fk_call_params_assign = post_fk_call_params_assign[:-2]
            put_fk_call_params_assign = put_fk_call_params_assign[:-2]
            delete_fk_call_params = delete_fk_call_params[:-2]
            delete_not_found_params = primary_keys[0].PropertyName.lower()
            pass_params = pass_params[:-2]

            model_name = visible_table.ModelName
            for line in contents:
                new_line = line
                if '[ClassController]' in line:
                    new_line = new_line.replace(
                        '[ClassController]', '{0}Controller'.format(model_name))
                if '[RepositoryInterface]' in line:
                    new_line = new_line.replace(
                        '[RepositoryInterface]', 'I{0}Repository'.format(model_name))
                if '[ModelName]' in line:
                    new_line = new_line.replace('[ModelName]', model_name)
                if '---FKParams---' in line:
                    new_line = new_line.replace('---FKParams---', pk_params)
                if '---Params---' in line:
                    new_line = new_line.replace('---Params---', pass_params)
                if '--PostFkCallParams--' in line:
                    new_line = new_line.replace(
                        '--PostFkCallParams--', post_fk_call_params_assign)
                if '--PutFkCallParams--' in line:
                    new_line = new_line.replace(
                        '--PutFkCallParams--', put_fk_call_params_assign)
                if '[FirstFK]' in line:
                    new_line = new_line.replace(
                        '[FirstFK]', primary_keys[0].PropertyName)
                if '--DeleteFkCallParams--' in line:
                    new_line = new_line.replace(
                        '--DeleteFkCallParams--', delete_fk_call_params)
                if '--DeleteItemNotFound--' in line:
                    new_line = new_line.replace(
                        '--DeleteItemNotFound--', delete_not_found_params)
                if ('Uncomment Get all' in line or 'Uncomment Get by Id' in line) and 'R' in visible_table.ActionGroup:
                    new_line = ''
                if 'Uncomment Post' in line and 'C' in visible_table.ActionGroup:
                    new_line = ''
                if 'Uncomment Put' in line and 'U' in visible_table.ActionGroup:
                    new_line = ''
                if 'Uncomment Delete' in line and 'D' in visible_table.ActionGroup:
                    new_line = ''

                new_contents.append(new_line)
            with open(controller_write_path.format(model_name), 'w') as w:
                w.write(''.join(new_contents))


def db_to_net_data_type_convert(datatype):
    mysql_string = ['char', 'varchar', 'binary', 'varbinary', 'tinyblob', 'tinytext', 'text', 'blob', 'mediumtext',
                    'mediumblob', 'longtext', 'longblob', 'enum', 'set']
    mysql_numeric = ['bit', 'tinyint', 'bool', 'boolean',
                     'smallint', 'mediumint', 'int', 'integer', 'bigint']
    mysql_floating_point = ['float', 'double',
                            'double precision', 'decimal', 'dec']

    mssql_string = ["CHAR", "NCHAR", "VARCHAR", "NVARCHAR", "BINARY", "VARBINARY", "TINYBLOB", "TINYTEXT", "TEXT",
                    "BLOB", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT", "LONGBLOB"]
    mssql_numeric = ["BIT", "TINYINT", "BOOL", "BOOLEAN",
                     "SMALLINT", "MEDIUMINT", "INT", "INTEGER"]
    mssql_floating_point = ["FLOAT", "DOUBLE", "MONEY"]

    postgre_string = ['varchar', 'character varying', 'text', 'char']
    postgre_numeric = ['smallint', 'integer', 'bigint']
    postgre_floating_point = ['decimal', 'numeric', 'real', 'double']

    if datatype.lower() in mysql_string or datatype.upper() in mssql_string or datatype.lower() in postgre_string:
        return 'string'
    elif datatype.lower() in mysql_numeric or datatype.upper() in mssql_numeric or datatype.lower() in postgre_numeric:
        return 'int'
    elif datatype.lower() in mysql_floating_point or datatype.upper() in mssql_floating_point or datatype.lower() in postgre_floating_point:
        return 'double'


def reset_template_api_repo():
    print('Resetting working environment ....')
    repo = git.Repo('./CustomerTemplateAPI')
    repo.git.reset('--hard')
    repo.git.clean('-fdx')
    print('Done. \n')


def delete_used_generated_model(model_guid):
    remove_path = './EFCoreScaffold/{0}'.format(model_guid)
    if os.path.exists(remove_path):
        shutil.rmtree(remove_path)


def upload_customer_api_to_filestack(guid):
    print('Uploading generated API ....')
    file_path = './temp/{0}'.format(guid)
    shutil.copytree('./CustomerTemplateAPI', file_path,
                    ignore=shutil.ignore_patterns('.*'))
    if os.path.exists(file_path):
        if os.path.exists(file_path + '/CustomerTemplateAPI/bin'):
            shutil.rmtree(file_path + '/CustomerTemplateAPI/bin')
        if os.path.exists(file_path + '/CustomerTemplateAPI/obj'):
            shutil.rmtree(file_path + '/CustomerTemplateAPI/obj')
        shutil.make_archive(guid, 'zip', file_path)
        shutil.move('./{0}.zip'.format(guid), './temp')

        file_stack_client = Client('A3m68KhQQIWnhduCSOxwAz')
        filename = guid + '.zip'
        store_params = {
            "filename": filename}
        new_filelink = file_stack_client.upload(
            filepath=file_path + '.zip', store_params=store_params)

        shutil.rmtree(file_path)
    print('Done. \n')
    return(new_filelink.url)


def get_swagger_file(guid):
    print('Generating swagger.json')
    script_path_run = './powershell-script/RunDotNet.sh'
    program_file_path = './CustomerTemplateAPI/CustomerTemplateAPI/Program.cs'

    with open(program_file_path, 'r') as r:
        contents = r.readlines()
        for idx in range(len(contents)):
            if 'host.Run();' in contents[idx]:
                contents[idx] = ''
        with open(program_file_path, 'w') as w:
            w.write(''.join(contents))

    command_list = shlex.split(script_path_run)
    p = subprocess.check_call(command_list)

    print('Created swagger.json file')
    print('Copy swagger file to destinated folder')

    dst_path = "/root/swagger-codegen/user_api_swagger/swagger_{0}.json".format(
        guid)
    src_path = "/root/CustomerAPIGenerate/CustomerTemplateAPI/CustomerTemplateAPI/swagger.json"
    copyfile(src_path, dst_path)
    print('Done all')


# create_customer_api('vuonghuynhsolutions.tech', 'root', 'Hoangvuong1024', 'classicmodels', 'mysql')
# create_customer_api('vuonghuynhsolutions.tech', 'vuongqhhuynh', 'Hoangvuong1024', 'QuanLyQuanCafe', 'mssql')
# create_customer_api('vuonghuynhsolutions.tech', 'vuongqhhuynh', 'Hoangvuong1024', 'Northwind', 'mssql')


# dbConn = DbConnection('vuonghuynhsolutions.tech', 'sa',
#                       'Hoangvuong1024', 'chinook', 'postgre', 49154)

# dbConn = DbConnection('vuonghuynhsolutions.tech', 'vuongqhhuynh',
#                       'Hoangvuong1024', 'QuanLyQuanCafe', 'mssql', '1433')

# dbConn = DbConnection('vuonghuynhsolutions.tech', 'root',
#                      'Hoangvuong1024', 'classicmodels', 'mysql', '49153')


# create_customer_api(dbConn)

def generate_api_with_db_guid(db_guid):
    result = None
    if db_guid != '-1':
        db_conn = AdminDbReader().get_db_conn_info(db_guid)
        if db_conn == None:
            result = ApiCreateResult('Failed', '', '', 'Not found any database connection info matched with given guid', '', db_guid)
        else:
            api_guid, api_download_url, package_identifier, client_app_guid, client_app_download_link = '', '', '', '', ''
            try:
                api_guid, api_download_url, package_identifier, client_app_guid, client_app_download_link = create_customer_api(db_conn, db_guid)
            except Exception as ex:
                return ApiCreateResult('Failed', '', '', str(ex), db_guid=db_guid)
            result = ApiCreateResult('Success', api_guid, api_download_url, '', package_identifier, db_guid, client_app_guid, client_app_download_link)
    else:
        result = ApiCreateResult('Failed', '', '', 'Db_Guid must have value', '', db_guid)
        
    return result

app = Flask(__name__)
CORS(app)
q = Queue(connection=conn)

@app.route('/', methods=['GET'])
def hello():
    return "Congratulation, API Generator worked!"
    
    
@app.route('/create-api/<db_guid>', methods=['GET'])
def api_endpoint(db_guid):
    from app import generate_api_with_db_guid
    job = q.enqueue_call(func=generate_api_with_db_guid, args=(db_guid, ), result_ttl=5000)
    return jsonify({
                    'status':'processing', 
                    'dbGuid': db_guid,
                    'job': str(job.key).split(':')[2][:-1],
                    'enqueuedAt': str(job.enqueued_at)
                    })


@app.route("/get-generated-api/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        job_result = job.result
        result = ApiCreateResult(job_result.Status, 
                                 job_result.ApiGuid, 
                                 job_result.ApiDownloadLink, 
                                 job_result.ErrorMessage, 
                                 job_result.PackageName, 
                                 job_result.DbGuid,
                                 job_result.ClientAppGuid,
                                 job_result.ClientAppDownloadLink)
        return jsonify({
            'db_guid': result.DbGuid,
            'status': result.Status,
            'error_message': result.ErrorMessage,
            'api_guid': result.ApiGuid,
            'package_name': 'api-client-{0}'.format(result.PackageName),
            'api_download_link': result.ApiDownloadLink,
            'client_app_download_link': result.ClientAppDownloadLink,
            'client_app_guid': result.ClientAppGuid
        })
    else:
        job_status = ''
        if job.is_queued:
            job_status = 'in-queue'
        elif job.is_started:
            job_status = 'waiting'
        elif job.is_failed:
            job_status = 'failed'
        return jsonify({
            'db_guid': '',
            'status': job_status,
            'error_message': '',
            'api_guid': '',
            'package_name': '',
            'api_download_link': '',
            'client_app_download_link': '',
            'client_app_guid': ''
        })
        
@app.route("/get-all-jobs", methods=['GET'])
def get_all_job():
    registry = StartedJobRegistry('default', connection=conn)
    registry_finished = FinishedJobRegistry('default', connection=conn)
    queued_job_ids = registry.get_queue().job_ids
    running_job_ids = registry.get_job_ids()
    finished_job_ids = registry_finished.get_job_ids() 
    all_job_ids = queued_job_ids + running_job_ids + finished_job_ids
    job_list = []
    for job_id in all_job_ids:
        job = Job.fetch(job_id, connection=conn)
        result = None
        if job.is_finished:
            job_result = job.result
            result = ApiCreateResult(job_result.Status, 
                                     job_result.ApiGuid, 
                                     job_result.ApiDownloadLink, 
                                     job_result.ErrorMessage, 
                                     job_result.PackageName,
                                     job_result.DbGuid
                                     )
        else:
            job_status = ''
            if job.is_queued:
                job_status = 'in-queue'
            elif job.is_started:
                job_status = 'waiting'
            elif job.is_failed:
                job_status = 'failed'
            result = ApiCreateResult(job_status, 
                                     '', 
                                     ''
                                     )
        json_str = {
            'dbGuid': result.DbGuid,
            'status': result.Status,
            'error_message': result.ErrorMessage,
            'api_guid': result.ApiGuid,
            'package_name': 'api-client-{0}'.format(result.PackageName) if result.PackageName != '' else '',
            'api_download_link': result.ApiDownloadLink
        }
        job_list.append(json_str)
            
    return Response(json.dumps(job_list), mimetype='application/json')
            

if __name__ == '__main__':
    app.run(debug=True)
