import os
import shutil
import zipfile
import requests
import uuid
from shutil import copyfile
from filestack import Client
from .DbReader import DatabaseSchemaProvider, AdminDbReader


def reset_client_app_src_code_template():
    client_app_template_folderpath = './ClientAppGenerator/ClientAppTemplate'
    client_app_original_bak_zip_file_path = './ClientAppGenerator/TemplateFiles/ClientAppTemplate_Original.zip'
    root_path = './ClientAppGenerator'
    
    shutil.rmtree(client_app_template_folderpath, ignore_errors=True)
    with zipfile.ZipFile(client_app_original_bak_zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(root_path)
    

def basic_settings(api_client_package_id, api_base_path, list_master_config, list_table_config):
    login_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/login-screen/login-content/login-content.component.ts'
    register_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/login-screen/register-content/register-content.component.ts'
    sidebar_nav_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/sidebar-navigation/sidebar-navigation.component.ts'
    sidebar_nav_html_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/sidebar-navigation/sidebar-navigation.component.html'
    app_module_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/app.module.ts'
    env_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/environments/environment.ts'
    index_html_filepath = './ClientAppGenerator/ClientAppTemplate/src/index.html'
    login_html_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/login-screen/login-content/login-content.component.html'
    register_html_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/components/login-screen/login-screen.component.html'
    
    list_files = [login_ts_filepath, register_ts_filepath, 
                  sidebar_nav_ts_filepath, 
                  sidebar_nav_html_filepath, 
                  app_module_ts_filepath, 
                  env_ts_filepath, 
                  index_html_filepath,
                  login_html_filepath,
                  register_html_filepath
                  ]
    bussiness_name = [w for w in list_master_config if w.ConfigName == 'bussinessName'  ]
    client_api_package_name = '@hqhoangvuong/api-client-' + api_client_package_id
    client_api_package_metadata = 'hqhoangvuong-api-client-{0}.metadata.json'.format(api_client_package_id)
    hidden_entities = ''
    
    for table_config in list_table_config:
        hidden_entities += "    '{0}Service',\n".format(table_config.ModelName)
    
    for file_name in list_files:
        with open(file_name, 'r') as r:
            old_contens = r.readlines()
            new_contents = []
            for line in old_contens:
                if '[--ClientApiPackageName--]' in line:
                    line = line.replace('[--ClientApiPackageName--]', client_api_package_name)
                if '[--ClientApiMetadataFile--]' in line:
                    line = line.replace('[--ClientApiMetadataFile--]', client_api_package_metadata)
                if '[--ApiBasePath--]' in line:
                    line = line.replace('[--ApiBasePath--]', api_base_path)
                if '[--BussinessName--]' in line:
                    line = line.replace('[--BussinessName--]', bussiness_name[0].ConfigValue)
                if '[--ListHiddenEntities--]' in line:
                    line = hidden_entities
                new_contents.append(line)
            r.close()
        with open(file_name, 'w') as w:
            w.write(''.join(new_contents))
            w.close()
            
    download_bussiness_logo(list_master_config)


def routing_setting(list_table_configs):
    app_routing_module_ts_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/app-routing.module.ts'
    import_statement_component_table = "import {0} {1}TableUIComponent {2} from './components/user-logged-in/{3}-table-ui/{3}-table-ui.component';\n"
    path_declare_statement = '      {0} path: {1}, component: {2} {3},\n'
    import_contents = ''
    path_declare_contents = ''
    
    for table_config in list_table_configs:
        import_contents += import_statement_component_table.format('{', table_config.ModelName, '}', table_config.ModelName.lower())
        path_declare_contents += path_declare_statement.format('{',"'index/" + table_config.ModelName.lower() + "management'", table_config.ModelName + 'TableUIComponent', '}')
    
    initRoute = path_declare_statement.format('{',"''", table_config.ModelName + 'TableUIComponent', '}')
    
    with open(app_routing_module_ts_filepath, 'r') as r:
        routing_module_contents = r.readlines()
        modified_routing_module_contents = []
        for line in routing_module_contents:
            if '/** ImportHere. */' in line:
                line += import_contents
            if '/** PathDeclareHere. */' in line:
                line += path_declare_contents
            if '/** DefaultScreen. */' in line:
                line = line.replace('/** DefaultScreen. */', initRoute)
            modified_routing_module_contents.append(line)
        r.close()
    with open(app_routing_module_ts_filepath, 'w') as w:
        w.write(''.join(modified_routing_module_contents))
        w.close()
      

def app_module_settings(list_table_configs):
    app_module_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/app.module.ts'
    import_statement_component_table = "import {0} {1}TableUIComponent {2} from './components/user-logged-in/{3}-table-ui/{3}-table-ui.component';\n"
    declaration_statement = '    {0}TableUIComponent,\n'
    import_contents = ''
    declaration_contents = ''
    
    for table_config in list_table_configs:
        import_contents += import_statement_component_table.format('{', table_config.ModelName, '}', table_config.ModelName.lower())
        declaration_contents += declaration_statement.format(table_config.ModelName)
        
    with open(app_module_filepath, 'r') as r:
        app_module_contents = r.readlines()
        modified_app_module_contents = []
        for line in app_module_contents:
            if '[--ImportAppModule--]' in line:
                line = line.replace('[--ImportAppModule--]', import_contents)
            if '[--DeclareAppModule--]' in line:
                line = line.replace('[--DeclareAppModule--]', declaration_contents)
            modified_app_module_contents.append(line)
        r.close()
    with open(app_module_filepath, 'w') as w:
        w.write(''.join(modified_app_module_contents))
        w.close();
          
          
def create_ui_table_actions(list_table_configs, list_column_configs, list_foreign_key_config, api_client_package_id, dbinfo):
    client_api_package_name = '@hqhoangvuong/api-client-' + api_client_package_id
    delete_action_component_creator(list_table_configs, client_api_package_name)
    read_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo)
    create_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo)
    update_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo)
        
        
def delete_action_component_creator(list_table_configs, client_api_package_name):
    delete_component_path = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-delete-ui-dialog'
    delete_component_filename = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-delete-ui-dialog/{0}-delete-ui-dialog.component.{1}'
    delete_html_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/delete-ui-dialog/delete-ui.component.html'
    delete_scss_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/delete-ui-dialog/delete-ui.component.scss'
    delete_ts_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/delete-ui-dialog/delete-ui.component.ts'
    import_list = []
    declare_list = []
    list_table_configs = [w for w in list_table_configs if 'D' in w.ActionGroup]
    
    for table_config in list_table_configs:
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        tableUiComponentPath = '{0}-table-ui/{0}-table-ui.component'.format(modelName.lower())
        deleteClassname = modelName + 'DeleteUIComponent'
        selectorName = 'app-{0}-delete-ui-dialog'.format(modelName.lower())
        urlName = '{0}-delete-ui-dialog.component'.format(modelName.lower()) 
        
        
        import_item = [deleteClassname, './components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-delete-ui-dialog/{0}-delete-ui-dialog.component'.format(table_config.ModelName.lower())]
        import_list.append(import_item)
        declare_list.append(deleteClassname)
        
        # Create delete action
        os.makedirs(delete_component_path.format(table_config.ModelName.lower()))
        # Create style file
        copyfile(delete_scss_template_path, delete_component_filename.format(table_config.ModelName.lower(), 'scss'))
        # Create Html file
        copyfile(delete_html_template_path, delete_component_filename.format(table_config.ModelName.lower(), 'html'))
        # create Ts file
        with open(delete_ts_template_path, 'r') as r:
            ts_contents = r.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--TableUIComponentPath--]' in line:
                    line = line.replace('[--TableUIComponentPath--]', tableUiComponentPath)
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName)
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--ClassName--]' in line:
                    line = line.replace('[--ClassName--]', deleteClassname)
                if '[--ApiClientPackageId--]' in line:
                    line = line.replace('[--ApiClientPackageId--]', client_api_package_name)
                modified_ts_contents.append(line)
            r.close()
        with open(delete_component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            w.write(''.join(modified_ts_contents))
            w.close()  
    update_app_module_file_for_action(import_list, declare_list)
    
    
def read_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo):
    read_component_path = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-read-ui-component'
    read_component_filename = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-read-ui-component/{0}-read-ui.component.{1}'
    read_html_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/read-ui/read-ui.component.html'
    read_scss_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/read-ui/read-ui.component.scss'
    read_ts_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/read-ui/read-ui.component.ts'
    read_html_data_field_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/read-ui/html_data_field_template.txt'
    import_list = []
    declare_list = []
    path_list = []
        
    for table_config in list_table_configs:
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        tableUiComponentPath = '{0}-table-ui/{0}-table-ui.component'.format(modelName.lower())
        readClassName = modelName + 'ReadUIComponent'
        selectorName = 'app-{0}-read-ui-component'.format(modelName.lower())
        urlName = '{0}-read-ui.component'.format(modelName.lower()) 
        
        import_item = [readClassName, './components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-read-ui-component/{0}-read-ui.component'.format(table_config.ModelName.lower())]
        path_item = "      { path: 'index/0/view/:id', component: ReadUIComponent },\n".replace('ReadUIComponent', readClassName).replace('0', modelName.lower() + 'management')
        import_list.append(import_item)
        declare_list.append(readClassName)
        path_list.append(path_item)
        
        html_data_field_template = ''
        html_insert = ''
        
        with open(read_html_data_field_template_path, 'r') as r1:
            html_data_field_template = ''.join(r1.readlines())
            r1.close()
        
        belonged_colum_config = [column_config for column_config in list_column_configs if column_config.TableId == table_config.Id]
        belonged_colum_config = sorted(list(belonged_colum_config),
                                       key=lambda x: x.OrdinalPosition)
        primary_key_column = [x for x in belonged_colum_config if x.IsPrimaryKey]
        
        input_component_idx = -1
        data_field = '\n'
        for column_config in belonged_colum_config:
            input_component_idx += 1
            if input_component_idx % 2 == 0:
                data_field += '      <div class="row" style="margin-bottom: 30px">\n'
                
            data_field += html_data_field_template.replace('[--DisplayName--]', column_config.ExplicitName) \
                                                 .replace('[--ModelNameWithLower--]', column_config.PropertyName[0].lower() + column_config.PropertyName[1:]) +'\n'
                                                 
            if input_component_idx % 2 == 1 or input_component_idx >= len(belonged_colum_config):
                data_field += '      </div>\n'
                html_insert += data_field
                data_field = '\n'
            
        # Create read action
        os.makedirs(read_component_path.format(table_config.ModelName.lower()))
        
        # Create html file
        with open(read_html_template_path, 'r') as r_html:
            html_contents = r_html.readlines()
            modified_html_contents = []
            for line in html_contents:
                if '[--InsertHere--]' in line:
                    line = html_insert
                if '[--ExceplitName--]' in line:
                    line = line.replace('[--ExceplitName--]', table_config.ExplicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                modified_html_contents.append(line)
            r_html.close()
        with open(read_component_filename.format(table_config.ModelName.lower(), 'html'), 'w') as w_html:
            w_html.write(''.join(modified_html_contents))
            w_html.close()  
        
        # Create style file
        copyfile(read_scss_template_path, read_component_filename.format(table_config.ModelName.lower(), 'scss'))
        
        # Create ts file
        with open(read_ts_template_path, 'r') as r_ts:
            ts_contents = r_ts.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--TableUIComponentPath--]' in line:
                    line = line.replace('[--TableUIComponentPath--]', tableUiComponentPath)
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName)
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--ClassName--]' in line:
                    line = line.replace('[--ClassName--]', readClassName)
                if '[--ApiClientPackageId--]' in line:
                    line = line.replace('[--ApiClientPackageId--]', client_api_package_name)
                if '[--ModelName--]' in line:
                    line = line.replace('[--ModelName--]', modelName)
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                modified_ts_contents.append(line)
            r_ts.close()
        with open(read_component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            w.write(''.join(modified_ts_contents))
            w.close()  
    update_app_module_file_for_action(import_list, declare_list)
    update_routing_file_for_action(import_list, path_list)
        
        
def create_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo):
    create_component_path = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-create-ui-component'
    create_component_filename = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-create-ui-component/{0}-create-ui.component.{1}'
    create_html_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/create-ui/create-ui.component.html'
    create_scss_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/create-ui/create-ui.component.scss'
    create_ts_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/create-ui/create-ui.component.ts'
    create_html_data_field_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/create-ui/html_data_field_template.txt'
    ddl_html_component_template = './ClientAppGenerator/TemplateFiles/HtmlComponent/DropDownList.txt'
    import_list = []
    declare_list = []
    path_list = []
    
    html_data_field_template = ''
    with open(create_html_data_field_template_path, 'r') as r1:
        html_data_field_template = ''.join(r1.readlines())
        r1.close()
        
    html_ddl_field_template = ''
    with open(ddl_html_component_template, 'r') as r2:
        html_ddl_field_template = ''.join(r2.readlines())
        r2.close()
        
    # list_table_configs = [w for w in list_table_configs if 'C' in w.ActionGroup]
    
    for table_config in list_table_configs:
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        explicitName = table_config.ExplicitName
        tableUiComponentPath = '{0}-table-ui/{0}-table-ui.component'.format(modelName.lower())
        createClassName = modelName + 'createUIComponent'
        selectorName = 'app-{0}-create-ui-component'.format(modelName.lower())
        urlName = '{0}-create-ui.component'.format(modelName.lower()) 
        belonged_fk = [w for w in list_foreign_key_config if w.SourceTableName == table_config.Name]
        IsGrantToCreate = False
        if 'C' in table_config.ActionGroup:
            IsGrantToCreate = True
                    
        import_item = [createClassName, './components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-create-ui-component/{0}-create-ui.component'.format(table_config.ModelName.lower())]
        path_item = "      { path: 'index/0/create', component: createUIComponent },\n".replace('createUIComponent', createClassName).replace('0', modelName.lower() + 'management')
        import_list.append(import_item)
        declare_list.append(createClassName)
        path_list.append(path_item)

        
        belonged_colum_config = [column_config for column_config in list_column_configs if column_config.TableId == table_config.Id]
        belonged_colum_config = sorted(list(belonged_colum_config),
                                       key=lambda x: x.OrdinalPosition)
        
        html_insert = ''
        primary_key_column = [x for x in belonged_colum_config if x.IsPrimaryKey]
        input_component_idx = -1
        data_field = '\n'
        for column_config in belonged_colum_config:
            if not (column_config.IsPrimaryKey == 1 and column_config.IsAutoIncremental == 1):
                input_component_idx += 1
                if input_component_idx % 2 == 0:
                    data_field += '      <div class="row" style="margin-bottom: 30px">\n'
                    
                if not column_config.IsForeignKey:
                    data_field += html_data_field_template.replace('[--DisplayName--]', column_config.ExplicitName) .replace('[--ModelNameWithLower--]', column_config.PropertyName[0].lower() + column_config.PropertyName[1:]) +'\n'
                else:
                    fk_refrenced_info = [w for w in belonged_fk if w.SourceColumnName == column_config.ColumnName][0]
                    fk_table_refrenced_info = [w for w in list_table_configs if w.Name == fk_refrenced_info.RefrencedTableName][0]
                    column_property_name = column_config.PropertyName
                    column_property_name_lower_first = column_config.PropertyName[0].lower() + column_config.PropertyName[1:]
                    table_model_name_lower_first = fk_table_refrenced_info.ModelName[0].lower() + fk_table_refrenced_info.ModelName[1:]
                    fk_items = table_model_name_lower_first + 'Items'
                    refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.RefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    mapped_refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.MappedRefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    data_field += html_ddl_field_template.replace('[--ColumnPropertyName--]', column_property_name) \
                                                         .replace('[--ColumnPropertyNameLowerFirst--]', column_property_name_lower_first).replace('[--FKItems--]', fk_items)  \
                                                         .replace('[--RefrencedColumnNameLowerFirst--]', refrenced_column_name[0].lower() + refrenced_column_name[1:]) \
                                                         .replace('[--MappedRefrencedColumnNameLowerFirst--]', mapped_refrenced_column_name[0].lower() + mapped_refrenced_column_name[1:]) \
                                                         .replace('[--DisplayName--]', column_config.ExplicitName)
                if input_component_idx % 2 != 0 or input_component_idx + 1 >= len([w for w in belonged_colum_config if not( w.IsPrimaryKey == 1 and w.IsAutoIncremental == 1)]):
                    data_field += '      </div>\n'
                    html_insert += data_field
                    data_field = '\n'

            
        # Create create action
        os.makedirs(create_component_path.format(table_config.ModelName.lower()))
        
        # Create html file
        with open(create_html_template_path, 'r') as r_html:
            html_contents = r_html.readlines()
            modified_html_contents = []
            for line in html_contents:
                if '[--InsertHere--]' in line:
                    line = html_insert
                if '[--ExceplitName--]' in line:
                    line = line.replace('[--ExceplitName--]', table_config.ExplicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                modified_html_contents.append(line)
            r_html.close()
        with open(create_component_filename.format(table_config.ModelName.lower(), 'html'), 'w') as w_html:
            w_html.write(''.join(modified_html_contents))
            w_html.close()  
        
        # Create style file
        copyfile(create_scss_template_path, create_component_filename.format(table_config.ModelName.lower(), 'scss'))
        
        fk_service_list = ''
        fk_model_list = ''
        fk_items = ''
        fk_services = ''
        inject_fk = ''
        fk_service_set_auth = ''
        fk_service_init = ''
        fk_item_init = ''
        fk_data_binding = ''
        
        for fk_config in belonged_fk:
            refrenced_table_details = [w for w in list_table_configs if w.Name == fk_config.RefrencedTableName][0]
            refrenced_column_details = [w for w in list_column_configs if w.ColumnName == fk_config.RefrencedColumnName and w.TableId == refrenced_table_details.Id][0]
            property_name = refrenced_table_details.ModelName
            property_name_first_lower = refrenced_table_details.ModelName[0].lower() + refrenced_table_details.ModelName[1:]
            
            if fk_config.RefrencedTableName != table_config.Name:
                fk_service_list += property_name + 'Service, '
                fk_model_list += property_name + ', '
            fk_items += '  ' + property_name_first_lower + 'Items: ' + property_name + '[] = [];\n'
            fk_services += '  ' +  property_name_first_lower + 'Service: ' + property_name + 'Service;\n'
            inject_fk += '    @Inject({0}Service) {1}srv:  {0}Service,\n'.format(property_name, property_name_first_lower)
            fk_service_set_auth += '    ' + property_name_first_lower + 'srv.defaultHeaders = new HttpHeaders({\n' \
                                   '      "Content-Type": "application/json",\n' \
                                   '      Authorization: "Bearer " + this.token,\n' \
                                   '    });\n'
            fk_service_init += '    this.{0}Service = {0}srv;\n'.format(property_name_first_lower)
            fk_item_init += '    this.{0}Items = {2} as {1}\n'.format(property_name_first_lower, property_name, '{}')
            
            fk_data_binding += '    this.' + property_name_first_lower + 'Service.api' + property_name + 'Get().subscribe((result) => {\n' \
                               '      this.' + property_name_first_lower + 'Items = result;\n' \
                               '    })\n' 
        # Create ts file
        with open(create_ts_template_path, 'r') as r_ts:
            ts_contents = r_ts.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--TableUIComponentPath--]' in line:
                    line = line.replace('[--TableUIComponentPath--]', tableUiComponentPath)
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName)
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--ClassName--]' in line:
                    line = line.replace('[--ClassName--]', createClassName)
                if '[--ApiClientPackageId--]' in line:
                    line = line.replace('[--ApiClientPackageId--]', client_api_package_name)
                if '[--ModelName--]' in line:
                    line = line.replace('[--ModelName--]', modelName)
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                if '[--FKServiceName--]' in line:
                    line = line.replace('[--FKServiceName--]', fk_service_list)
                if '[--FKModelName--]' in line:
                    line = line.replace('[--FKModelName--]', fk_model_list)
                if '[--FKItems--]' in line:
                    line = line.replace('[--FKItems--]', fk_items)
                if '[--FKServices--]' in line:
                    line = line.replace('[--FKServices--]', fk_services)
                if '[--InjectFK--]' in line:
                    line = line.replace('[--InjectFK--]', inject_fk)
                if '[--FKServiceSetAuth--]' in line:
                    line = line.replace('[--FKServiceSetAuth--]', fk_service_set_auth)
                if '[---FKItemsInit--]' in line:
                    line = line.replace('[---FKItemsInit--]', fk_item_init)
                if '[---FKServiceInit--]' in line:
                    line = line.replace('[---FKServiceInit--]', fk_service_init)
                if '[--FKDataBinding--]' in line:
                    line = line.replace('[--FKDataBinding--]', fk_data_binding)
                if '[--ExplicitName--]' in line:
                    line = line.replace('[--ExplicitName--]', explicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                if 'CreateLogicSession' in line and IsGrantToCreate:
                    line = ''
                modified_ts_contents.append(line)
            r_ts.close()
        with open(create_component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            w.write(''.join(modified_ts_contents))
            w.close()  
    update_app_module_file_for_action(import_list, declare_list)
    update_routing_file_for_action(import_list, path_list)


def update_action_component_creator(list_table_configs, list_column_configs, list_foreign_key_config, client_api_package_name, dbinfo):
    update_component_path = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component'
    update_component_filename = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component/{0}-update-ui.component.{1}'
    update_html_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/update-ui/update-ui.component.html'
    update_scss_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/update-ui/update-ui.component.scss'
    update_ts_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/update-ui/update-ui.component.ts'
    update_html_data_field_template_path = './ClientAppGenerator/TemplateFiles/ActionTemplate/update-ui/html_data_field_template.txt'
    ddl_html_component_template = './ClientAppGenerator/TemplateFiles/ActionTemplate/update-ui/html_drop_down_list.txt'
    import_list = []
    declare_list = []
    path_list = []
    
    html_data_field_template = ''
    with open(update_html_data_field_template_path, 'r') as r1:
        html_data_field_template = ''.join(r1.readlines())
        r1.close()
        
    html_ddl_field_template = ''
    with open(ddl_html_component_template, 'r') as r2:
        html_ddl_field_template = ''.join(r2.readlines())
        r2.close()
        
    # list_table_configs = [w for w in list_table_configs if 'C' in w.ActionGroup]
    
    for table_config in list_table_configs:
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        explicitName = table_config.ExplicitName
        tableUiComponentPath = '{0}-table-ui/{0}-table-ui.component'.format(modelName.lower())
        updateClassName = modelName + 'UpdateUIComponent'
        selectorName = 'app-{0}-update-ui-component'.format(modelName.lower())
        urlName = '{0}-update-ui.component'.format(modelName.lower()) 
        belonged_fk = [w for w in list_foreign_key_config if w.SourceTableName == table_config.Name]
                    
        import_item = [updateClassName, './components/user-logged-in/{0}-table-ui/{0}-table-ui-action/{0}-update-ui-component/{0}-update-ui.component'.format(table_config.ModelName.lower())]
        path_item = "      { path: 'index/0/update/:id', component: updateUIComponent },\n".replace('updateUIComponent', updateClassName).replace('0', modelName.lower() + 'management')
        import_list.append(import_item)
        declare_list.append(updateClassName)
        path_list.append(path_item)

        
        belonged_colum_config = [column_config for column_config in list_column_configs if column_config.TableId == table_config.Id]
        belonged_colum_config = sorted(list(belonged_colum_config),
                                       key=lambda x: x.OrdinalPosition)
        IsGrantToUpdate = False
        if 'U' in table_config.ActionGroup:
            IsGrantToUpdate = True
        
        html_insert = ''
        primary_key_column = [x for x in belonged_colum_config if x.IsPrimaryKey]
        input_component_idx = -1
        data_field = '\n'
        for column_config in belonged_colum_config:
            if not (column_config.IsPrimaryKey == 1 and column_config.IsAutoIncremental == 1):
                input_component_idx += 1
                if input_component_idx % 2 == 0:
                    data_field += '      <div class="row" style="margin-bottom: 30px">\n'
                    
                if not column_config.IsForeignKey:
                    data_field += html_data_field_template.replace('[--DisplayName--]', column_config.ExplicitName) .replace('[--ModelNameWithLower--]', column_config.PropertyName[0].lower() + column_config.PropertyName[1:]).replace('[--DisableIfPrimaryKey--]', 'disabled' if column_config.IsPrimaryKey else '') +'\n'
                else:
                    fk_refrenced_info = [w for w in belonged_fk if w.SourceColumnName == column_config.ColumnName][0]
                    fk_table_refrenced_info = [w for w in list_table_configs if w.Name == fk_refrenced_info.RefrencedTableName][0]
                    column_property_name = column_config.PropertyName
                    column_property_name_lower_first = column_config.PropertyName[0].lower() + column_config.PropertyName[1:]
                    table_model_name_lower_first = fk_table_refrenced_info.ModelName[0].lower() + fk_table_refrenced_info.ModelName[1:]
                    fk_items = table_model_name_lower_first + 'Items'
                    refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.RefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    mapped_refrenced_column_name = [w.PropertyName for w in list_column_configs if w.ColumnName == fk_refrenced_info.MappedRefrencedColumnName and w.TableId == fk_table_refrenced_info.Id][0]
                    data_field += html_ddl_field_template.replace('[--ColumnPropertyName--]', column_property_name) \
                                                         .replace('[--ColumnPropertyNameLowerFirst--]', column_property_name_lower_first).replace('[--FKItems--]', fk_items)  \
                                                         .replace('[--RefrencedColumnNameLowerFirst--]', refrenced_column_name[0].lower() + refrenced_column_name[1:]) \
                                                         .replace('[--MappedRefrencedColumnNameLowerFirst--]', mapped_refrenced_column_name[0].lower() + mapped_refrenced_column_name[1:]) \
                                                         .replace('[--DisplayName--]', column_config.ExplicitName)
                if input_component_idx % 2 == 1 or input_component_idx >= len(belonged_colum_config):
                    data_field += '      </div>\n'
                    html_insert += data_field
                    data_field = '\n'

            
        # create update action
        os.makedirs(update_component_path.format(table_config.ModelName.lower()))
        
        # create html file
        with open(update_html_template_path, 'r') as r_html:
            html_contents = r_html.readlines()
            modified_html_contents = []
            for line in html_contents:
                if '[--InsertHere--]' in line:
                    line = html_insert
                if '[--ExceplitName--]' in line:
                    line = line.replace('[--ExceplitName--]', table_config.ExplicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                modified_html_contents.append(line)
            r_html.close()
        with open(update_component_filename.format(table_config.ModelName.lower(), 'html'), 'w') as w_html:
            w_html.write(''.join(modified_html_contents))
            w_html.close()  
        
        # create style file
        copyfile(update_scss_template_path, update_component_filename.format(table_config.ModelName.lower(), 'scss'))
        
        fk_service_list = ''
        fk_model_list = ''
        fk_items = ''
        fk_services = ''
        inject_fk = ''
        fk_service_set_auth = ''
        fk_service_init = ''
        fk_item_init = ''
        fk_data_binding = ''
        
        for fk_config in belonged_fk:
            refrenced_table_details = [w for w in list_table_configs if w.Name == fk_config.RefrencedTableName][0]
            # refrenced_column_details = [w for w in list_column_configs if w.ColumnName == fk_config.RefrencedColumnName and w.TableId == refrenced_table_details.Id][0]
            property_name = refrenced_table_details.ModelName
            property_name_first_lower = refrenced_table_details.ModelName[0].lower() + refrenced_table_details.ModelName[1:]
            
            if fk_config.RefrencedTableName != table_config.Name:
                fk_service_list += property_name + 'Service, '
                fk_model_list += property_name + ', '
            fk_items += '  ' + property_name_first_lower + 'Items: ' + property_name + '[] = [];\n'
            fk_services += '  ' +  property_name_first_lower + 'Service: ' + property_name + 'Service;\n'
            inject_fk += '    @Inject({0}Service) {1}srv:  {0}Service,\n'.format(property_name, property_name_first_lower)
            fk_service_set_auth += '    ' + property_name_first_lower + 'srv.defaultHeaders = new HttpHeaders({\n' \
                                   '      "Content-Type": "application/json",\n' \
                                   '      Authorization: "Bearer " + this.token,\n' \
                                   '    });\n'
            fk_service_init += '    this.{0}Service = {0}srv;\n'.format(property_name_first_lower)
            fk_item_init += '    this.{0}Items = {2} as {1}\n'.format(property_name_first_lower, property_name, '{}')
            
            fk_data_binding += '    this.' + property_name_first_lower + 'Service.api' + property_name + 'Get().subscribe((result) => {\n' \
                               '      this.' + property_name_first_lower + 'Items = result;\n' \
                               '    })\n' 
        # update ts file
        with open(update_ts_template_path, 'r') as r_ts:
            ts_contents = r_ts.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--TableUIComponentPath--]' in line:
                    line = line.replace('[--TableUIComponentPath--]', tableUiComponentPath)
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName)
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--ClassName--]' in line:
                    line = line.replace('[--ClassName--]', updateClassName)
                if '[--ApiClientPackageId--]' in line:
                    line = line.replace('[--ApiClientPackageId--]', client_api_package_name)
                if '[--ModelName--]' in line:
                    line = line.replace('[--ModelName--]', modelName)
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                if '[--FKServiceName--]' in line:
                    line = line.replace('[--FKServiceName--]', fk_service_list)
                if '[--FKModelName--]' in line:
                    line = line.replace('[--FKModelName--]', fk_model_list)
                if '[--FKItems--]' in line:
                    line = line.replace('[--FKItems--]', fk_items)
                if '[--FKServices--]' in line:
                    line = line.replace('[--FKServices--]', fk_services)
                if '[--InjectFK--]' in line:
                    line = line.replace('[--InjectFK--]', inject_fk)
                if '[--FKServiceSetAuth--]' in line:
                    line = line.replace('[--FKServiceSetAuth--]', fk_service_set_auth)
                if '[---FKItemsInit--]' in line:
                    line = line.replace('[---FKItemsInit--]', fk_item_init)
                if '[---FKServiceInit--]' in line:
                    line = line.replace('[---FKServiceInit--]', fk_service_init)
                if '[--FKDataBinding--]' in line:
                    line = line.replace('[--FKDataBinding--]', fk_data_binding)
                if '[--ExplicitName--]' in line:
                    line = line.replace('[--ExplicitName--]', explicitName)
                if '[--LowerModelName--]' in line:
                    line = line.replace('[--LowerModelName--]', modelName.lower())
                if 'OnUpdate' in line and IsGrantToUpdate:
                    line = ''
                if '[--CastedIdSelectInput--]' in line:
                    data_type = db_to_net_data_type_convert(primary_key_column[0].DataType)
                    if data_type == 'string':
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInput')
                    else:
                        line = line.replace('[--CastedIdSelectInput--]', 'this.idSelectedInputNumber')
                modified_ts_contents.append(line)
            r_ts.close()
        with open(update_component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            w.write(''.join(modified_ts_contents))
            w.close()  
    update_app_module_file_for_action(import_list, declare_list)
    update_routing_file_for_action(import_list, path_list)


def update_app_module_file_for_action(import_list, declare_list):
    app_module_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/app.module.ts'
    import_statement = "import {0} from '{1}';\n"
    import_contents = ''
    declare_contents = ''
    
    for import_item in import_list:
        import_contents += import_statement.format('{ ' + import_item[0] + ' }', import_item[1])
    
    for declare_item in declare_list:
        declare_contents += '    ' + declare_item + ',\n'
    
    with open(app_module_filepath, 'r') as r:
        app_module_contents = r.readlines()
        modified_app_module_contents = []
        for line in app_module_contents:
            if '/** DeclareComponentForAction. */' in line:
                line += declare_contents
            if '/** ImportComponentForAction. */' in line:
                line += import_contents
            modified_app_module_contents.append(line)
        r.close()
    with open(app_module_filepath, 'w') as w:
            w.write(''.join(modified_app_module_contents))
            w.close()  
   
   
def update_routing_file_for_action(import_list, path_list):
    app_routing_filepath = './ClientAppGenerator/ClientAppTemplate/src/app/app-routing.module.ts'
    import_statement = "import {0} from '{1}';\n"
    import_contents = ''
    path_contents = ''        
    
    for import_item in import_list:
        import_contents += import_statement.format('{ ' + import_item[0] + ' }', import_item[1])
    
    path_contents = ''.join(path_list)
    
    with open(app_routing_filepath, 'r') as r:
        routing_contents = r.readlines()
        modified_routing_module_contents = []
        for line in routing_contents:
            if '/** PathDeclareHere. */' in line:
                line += path_contents
            if '/** ImportHere. */' in line:
                line += import_contents
            modified_routing_module_contents.append(line)
        r.close()
    with open(app_routing_filepath, 'w') as w:
            w.write(''.join(modified_routing_module_contents))
            w.close()  
        
    
def create_table_ui_component(list_table_configs, list_column_configs, api_client_package_id):
    component_path = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui'
    component_filename = './ClientAppGenerator/ClientAppTemplate/src/app/components/user-logged-in/{0}-table-ui/{0}-table-ui.component.{1}'
    html_template_path = './ClientAppGenerator/TemplateFiles/TableTemplate/template-table-ui.component.html'
    scss_template_path = './ClientAppGenerator/TemplateFiles/TableTemplate/template-table-ui.component.scss'
    ts_template_path = './ClientAppGenerator/TemplateFiles/TableTemplate/template-table-ui.component.ts'
    clientApiPackageName = '@hqhoangvuong/api-client-' + api_client_package_id
    
    for table_config in list_table_configs:
        list_belonged_column = [column for column in list_column_configs if column.TableId == table_config.Id] 
        list_belonged_column.sort(key=lambda x: x.OrdinalPosition, reverse=False)
        primary_key_column = [x for x in list_belonged_column if x.IsPrimaryKey]
        tableActionGroup = [False, False, False, False]
        
        if 'C' in table_config.ActionGroup:
            tableActionGroup[0] = True
        if 'R' in table_config.ActionGroup:
            tableActionGroup[1] = True
        if 'U' in table_config.ActionGroup:
            tableActionGroup[2] = True
        if 'D' in table_config.ActionGroup:
            tableActionGroup[3] = True
        
        os.makedirs(component_path.format(table_config.ModelName.lower()))
        
        html_contents = []
        
        # Copy style scss file
        copyfile(scss_template_path, component_filename.format(table_config.ModelName.lower(), 'scss'))
        
        # Copy html file
        table_columns_name_contents = ''
        table_columns_values_contents = ''
        for column in list_belonged_column:
            table_columns_name_contents += '                <th scope="col-md-auto"> {0} </th>\n'.format(column.ExplicitName)
            table_columns_values_contents += '                <td>{{ item.' + column.PropertyName[0].lower() + column.PropertyName[1:] + ' }}</td>\n'
            
        with open(html_template_path, 'r') as r:
            html_contents = r.readlines()
            modified_html_contents = []
            for line in html_contents:
                if '[--TableTitle--]' in line:
                    line = line.replace('[--TableTitle--]', table_config.ExplicitName)
                if '[--TableColumnsValues--]' in line:
                    line = ''
                    for column in list_column_configs:
                        line = table_columns_values_contents
                if '[--TableColumNames--]' in line:
                    line = ''
                    for column in list_column_configs:
                        line = table_columns_name_contents
                if '[--PrimaryKey--]' in line:
                    line = line.replace('[--PrimaryKey--]', primary_key_column[0].PropertyName[0].lower() + primary_key_column[0].PropertyName[1:])
                if '[--ModelLowerAll--]' in line:
                    line = line.replace('[--ModelLowerAll--]', table_config.ModelName.lower())
                if '[--IsCreateDisabled--]' in line:
                    line = line.replace('[--IsCreateDisabled--]', 'false' if tableActionGroup[0] else 'true')
                if '[--IsDisableUpdate--]' in line:
                    line = line.replace('[--IsDisableUpdate--]', 'false' if tableActionGroup[2] else 'true')
                if '[--IsDisableDelete--]' in line:
                    line = line.replace('[--IsDisableDelete--]', 'false' if tableActionGroup[3] else 'true')
                modified_html_contents.append(line)
        with open(component_filename.format(table_config.ModelName.lower(), 'html'), 'w') as w:
            new_html_content = ''.join(modified_html_contents)
            w.write(new_html_content)
            
        # Copy typescript file
        modelName = table_config.ModelName
        serviceName = modelName + 'Service'
        selectorName = 'app-{0}-table-ui'.format(modelName.lower())
        urlName = '{0}-table-ui.component'.format(modelName.lower())
        deleteComponentPath = './{0}-table-ui-action/{0}-delete-ui-dialog/{0}-delete-ui-dialog.component'.format(modelName.lower())
        with open(ts_template_path, 'r') as r:
            ts_contents = r.readlines()
            modified_ts_contents = []
            for line in ts_contents:
                if '[--DeleteUiComponent--]' in line:
                    line = line.replace('[--DeleteUiComponent--]', deleteComponentPath) if tableActionGroup[3] else ''
                if '[--ServiceName--]' in line:
                    line = line.replace('[--ServiceName--]', serviceName)
                if '[--ModelName--]' in line:
                    line = line.replace('[--ModelName--]', modelName)
                if '[--ClientApiPackageName--]' in line:
                    line = line.replace('[--ClientApiPackageName--]', clientApiPackageName)
                if '[--SelectorName--]' in line:
                    line = line.replace('[--SelectorName--]', selectorName) 
                if '[--UrlName--]' in line:
                    line = line.replace('[--UrlName--]', urlName)
                if '[--PrimaryKey--]' in line:
                    line = line.replace('[--PrimaryKey--]', primary_key_column[0].PropertyName[0].lower() + primary_key_column[0].PropertyName[1:])
                if '[--IsDisableUpdate--]' in line:
                    line = '' if tableActionGroup[2] else line
                if '[--IsDisableDelete--]' in line:
                    line = '' if tableActionGroup[3] else line
                modified_ts_contents.append(line)
        with open(component_filename.format(table_config.ModelName.lower(), 'ts'), 'w') as w:
            new_ts_content = ''.join(modified_ts_contents)
            w.write(new_ts_content)


def db_to_net_data_type_convert(datatype):
    mysql_string = ['char', 'varchar', 'binary', 'varbinary', 'tinyblob', 'tinytext', 'text', 'blob', 'mediumtext',
                    'mediumblob', 'longtext', 'longblob', 'enum', 'set']
    mysql_numeric = ['bit', 'tinyint', 'bool', 'boolean', 'smallint', 'mediumint', 'int', 'integer', 'bigint']
    mysql_floating_point = ['float', 'double', 'double precision', 'decimal', 'dec']

    mssql_string = ["CHAR", "NCHAR", "VARCHAR", "NVARCHAR", "BINARY", "VARBINARY", "TINYBLOB", "TINYTEXT", "TEXT",
                    "BLOB", "MEDIUMTEXT", "MEDIUMBLOB", "LONGTEXT", "LONGBLOB"]
    mssql_numeric = ["BIT", "TINYINT", "BOOL", "BOOLEAN", "SMALLINT", "MEDIUMINT", "INT", "INTEGER"]
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


def download_bussiness_logo(list_master_config):
    default_logo_filepath = './ClientAppGenerator/TemplateFiles/BussinessLogo.png'
    asset_image_folder_path = './ClientAppGenerator/ClientAppTemplate/src/assets/images'
    bussiness_logo_config_info = [w for w in list_master_config if w.ConfigName == 'BussinessLogo']
    if len(bussiness_logo_config_info) == 0:
        shutil.copy2(default_logo_filepath, asset_image_folder_path)
    else:
        url = bussiness_logo_config_info[0].ConfigValue
        r = requests.get(url, allow_redirects=True)
        open(asset_image_folder_path + '/BussinessLogo.png', 'wb').write(r.content)


def create_client_app(dbinfo, api_client_package_id, api_base_path):
    (list_table_configs, list_column_configs, list_foreign_key_config, list_master_config) = DatabaseSchemaProvider().db_settings_reader(dbinfo)
    list_table_configs = [w for w in list_table_configs if w.IsHidden == 0]
    
    reset_client_app_src_code_template()
    basic_settings(api_client_package_id, api_base_path, list_master_config, list_table_configs)
    create_table_ui_component(list_table_configs, list_column_configs, api_client_package_id)
    routing_setting(list_table_configs)
    app_module_settings(list_table_configs)
    create_ui_table_actions(list_table_configs, list_column_configs, list_foreign_key_config, api_client_package_id, dbinfo)
    
    print(api_client_package_id)


def upload_client_app_to_filestack(guid):
    print('Uploading generated Client App ....')
    file_path = './temp/{0}'.format(guid)
    shutil.copytree('./ClientAppGenerator/ClientAppTemplate', file_path,
                    ignore=shutil.ignore_patterns('.*'))
    if os.path.exists(file_path):
        shutil.make_archive(guid, 'zip', file_path)
        shutil.move('./{0}.zip'.format(guid), './temp')

        file_stack_client = Client('A3m68KhQQIWnhduCSOxwAz')
        filename = guid + '.zip'
        store_params = {
            "filename": filename
            }
        
        new_filelink = file_stack_client.upload(
            filepath=file_path + '.zip', store_params=store_params)

        shutil.rmtree(file_path)
    print('Done. \n')
    return(new_filelink.url)

# def main():
#     # db_guid = 'f3c17522-ced5-4269-b7db-a90a966341e3'
#     # db_guid = 'd467fcdd-b8ee-4699-91f4-27adbc94f583'
#     db_guid = 'f3a43925-19c5-438e-9e36-a3315e86f4c5'
#     api_base_path = 'http://vuonghuynhsolutions.tech:8808'
#     api_client_package_id = '478673'
    
#     db_info = AdminDbReader().get_db_conn_info(db_guid)
#     create_client_app(db_info, api_client_package_id, api_base_path)


# if __name__ == "__main__":
#     main()
    
def create_client_frontend(db_guid, api_base_path, api_client_package_id):
    db_info = AdminDbReader().get_db_conn_info(db_guid)
    client_app_guid = str(uuid.uuid4())
    create_client_app(db_info, api_client_package_id, api_base_path)
    client_app_download_link = upload_client_app_to_filestack(client_app_guid)
    return client_app_guid, client_app_download_link