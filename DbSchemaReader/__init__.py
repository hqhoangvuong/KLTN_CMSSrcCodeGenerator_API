import psycopg2
import pymssql
from getpass import getpass
from mysql.connector import connect, Error

from models import TableConfig
from models import ColumnConfig


class DbSchemaProvider:
    listTableConfig = []
    listColumnConfig = []

    selectTableConfig = 'SELECT * FROM SystemTableConfigs'
    selectColumnConfig = 'SELECT * FROM SystemTableColumnConfigs'
    selectForeignKeyConfig = 'SELECT * FROM SystemTableForeingKeyConfigs'

    def __init__(self):
        listTableConfig = []
        listColumnConfig = []

    def get_schema(self, dbconn):
        listTableConfig = []
        listColumnConfig = []
        if dbconn.DbType == 'mysql':
            self.mysql_server(dbconn.Server, dbconn.Username,
                              dbconn.Password, dbconn.Database, dbconn.ServerPort)
        elif dbconn.DbType == 'mssql':
            self.mssql_server(dbconn.Server, dbconn.Username,
                              dbconn.Password, dbconn.Database, dbconn.ServerPort)
        elif dbconn.DbType == 'postgre':
            self.postgre_sql_server(
                                    dbconn.Server, dbconn.Username, dbconn.Password, 
                                    dbconn.Database, dbconn.ServerPort)

        return self.listTableConfig, self.listColumnConfig

    def mssql_server(self, server, user, password, database, svport):
        try:
            conn = pymssql.connect(server=server,
                                   port=svport,
                                   user=user,
                                   password=password,
                                   database=database)

            cursor = conn.cursor()

            cursor.execute(self.selectTableConfig)
            tablerows = cursor.fetchall()
            for row in tablerows:
                item = TableConfig(row[0], row[1], row[2], row[3], row[4])
                self.listTableConfig.append(item)

            cursor.execute(self.selectColumnConfig)
            columnrows = cursor.fetchall()
            for row in columnrows:
                item = ColumnConfig(
                    row[0], row[1], row[2], row[12], row[13], row[6], row[4])
                self.listColumnConfig.append(item)

            return self.listTableConfig, self.listColumnConfig
        except Error as ex:
            print(ex)

    def mysql_server(self, server, user, password, database, svport):
        try:
            with connect(
                    host=server,
                    port=svport,
                    user=user,
                    password=password,
                    database=database
            ) as conn:
                cursor = conn.cursor()
                cursor.execute(self.selectTableConfig)
                tablerows = cursor.fetchall()
                for row in tablerows:
                    item = TableConfig(row[0], row[1], row[2], row[3], row[4])
                    self.listTableConfig.append(item)

                cursor.execute(self.selectColumnConfig)
                columnrows = cursor.fetchall()
                for row in columnrows:
                    item = ColumnConfig(
                        row[0], row[1], row[2], row[12], row[13], row[6], row[4])
                    self.listColumnConfig.append(item)
        except Error as e:
            print(e)

    def postgre_sql_server(self, server, user, password, database, svport):
        try:
            conn = psycopg2.connect(
                host=server,
                port=svport,
                database=database,
                user=user,
                password=password
            )
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM public."SystemTableConfigs"')
            tablerows = cursor.fetchall()
            for row in tablerows:
                item = TableConfig(row[0], row[1], row[2], row[3], row[4])
                self.listTableConfig.append(item)

            cursor.execute('SELECT * FROM public."SystemTableColumnConfigs"')
            columnrows = cursor.fetchall()
            for row in columnrows:
                item = ColumnConfig(
                    row[0], row[1], row[2], row[12], row[13], row[6], row[4])
                self.listColumnConfig.append(item)
        except Error as e:
            print(e)
            return e.msg

    def update_model_name_for_table_config(self, dbconn, table_list):
        conn = None
        update_query = 'UPDATE SystemTableConfigs SET ModelName = {0} WHERE Id = {1}'
        update_query_postgre = 'UPDATE public."SystemTableConfigs" SET "ModelName" = {0} WHERE "Id" = {1}'
        try:
            if dbconn.DbType == 'mssql':
                conn = pymssql.connect(
                    server=dbconn.Server,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    database=dbconn.Database,
                    port=dbconn.ServerPort
                )
            elif dbconn.DbType == 'mysql':
                conn = connect(
                    host=dbconn.Server,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    database=dbconn.Database,
                    port=dbconn.ServerPort
                )
            elif dbconn.DbType == 'postgre':
                conn = psycopg2.connect(
                    host=dbconn.Server,
                    database=dbconn.Database,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    port=dbconn.ServerPort
                )
            cursor = conn.cursor()

            for table_config in table_list:
                if dbconn.DbType != 'postgre':
                    cursor.execute(update_query.format(
                        "'" + table_config.ModelName + "'", table_config.Id))
                else:
                    cursor.execute(update_query_postgre.format(
                        "'" + table_config.ModelName + "'", table_config.Id))
                conn.commit()
            conn.close()
        except Error as e:
            print(e)
            return e.msg

    def update_property_name_for_table_column_config(self, dbconn, column_list):
        conn = None
        update_query = 'UPDATE SystemTableColumnConfigs SET PropertyName = {0} WHERE Id = {1}'
        update_query_postgre = 'UPDATE public."SystemTableColumnConfigs" SET "PropertyName" = {0} WHERE "Id" = {1}'
        try:
            if dbconn.DbType == 'mssql':
                conn = pymssql.connect(
                    server=dbconn.Server,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    database=dbconn.Database,
                    port=dbconn.ServerPort
                )
            elif dbconn.DbType == 'mysql':
                conn = connect(
                    host=dbconn.Server,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    database=dbconn.Database,
                    port=dbconn.ServerPort
                )
            elif dbconn.DbType == 'postgre':
                conn = psycopg2.connect(
                    host=dbconn.Server,
                    database=dbconn.Database,
                    user=dbconn.Username,
                    password=dbconn.Password,
                    port=dbconn.ServerPort
                )
            cursor = conn.cursor()

            for column_config in column_list:
                if dbconn.DbType != 'postgre':
                    cursor.execute(update_query.format(
                        "'" + column_config.PropertyName + "'", column_config.Id))
                else:
                    cursor.execute(
                        update_query_postgre.format("'" + column_config.PropertyName + "'", column_config.Id))
                conn.commit()
            conn.close()
        except Error as e:
            print(e)
            return e.msg
