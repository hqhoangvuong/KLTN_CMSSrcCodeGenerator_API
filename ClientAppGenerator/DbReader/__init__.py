import psycopg2
import pymssql
from mysql.connector import connect, Error
from ..Models import *


class DatabaseSchemaProvider:
    def __init__(self):
        pass

    def db_settings_reader(self, dbinfo):
        conn = None
        try:
            if dbinfo.DbType == 'mssql':
                conn = pymssql.connect(
                    server=dbinfo.Server,
                    port=dbinfo.ServerPort,
                    user=dbinfo.Username,
                    password=dbinfo.Password,
                    database=dbinfo.Database
                )
            elif dbinfo.DbType == 'mysql':
                conn = connect(
                    host=dbinfo.Server,
                    port=dbinfo.ServerPort,
                    user=dbinfo.Username,
                    password=dbinfo.Password,
                    database=dbinfo.Database
                )
            elif dbinfo.DbType == 'postgre':
                conn = psycopg2.connect(
                    host=dbinfo.Server,
                    port=dbinfo.ServerPort,
                    user=dbinfo.Username,
                    password=dbinfo.Password,
                    database=dbinfo.Database
                )
            cursor = conn.cursor()
            selectTableConfig, selectColumnConfig, selectForeignKeyConfig, selectMasterConfig = '', '', '', ''
            listTableConfig = []
            listColumnConfig = []
            listMasterConfig = []
            listForeignKeyConfig =[]

            if dbinfo.DbType != 'postgre':
                selectTableConfig = 'SELECT * FROM SystemTableConfigs'
                selectColumnConfig = 'SELECT * FROM SystemTableColumnConfigs'
                selectForeignKeyConfig = 'SELECT * FROM SystemTableForeingKeyConfigs'
                selectMasterConfig = 'SELECT * FROM SystemMasterConfigs'
            else:
                selectTableConfig = 'SELECT * FROM public."SystemTableConfigs"'
                selectColumnConfig = 'SELECT * FROM public."SystemTableColumnConfigs"'
                selectForeignKeyConfig = 'SELECT * FROM public."SystemTableForeingKeyConfigs"'
                selectMasterConfig = 'SELECT * FROM public."SystemMasterConfigs"'

            cursor.execute(selectTableConfig)
            tableRows = cursor.fetchall()
            for row in tableRows:
                item = TableConfig(
                    row[0], row[1], row[2], row[3], row[4], row[8])
                listTableConfig.append(item)

            cursor.execute(selectColumnConfig)
            columnrows = cursor.fetchall()
            for row in columnrows:
                item = ColumnConfig(
                    row[0], row[1], row[2], row[12], row[13], row[6], row[4], row[18], row[3], row[10], row[19])
                listColumnConfig.append(item)
                
            cursor.execute(selectForeignKeyConfig)
            columnrows = cursor.fetchall()
            for row in columnrows:
                item = ForeignKeyConfig(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], 
                )
                listForeignKeyConfig.append(item)
            
            cursor.execute(selectMasterConfig)
            columnrows = cursor.fetchall()
            for row in columnrows:
                item = MasterConfig(
                    row[0], row[1], row[2]
                )
                listMasterConfig.append(item)
                
            return listTableConfig, listColumnConfig, listForeignKeyConfig, listMasterConfig
        except Error as e:
            print(e)


class AdminDbReader:
    def __init__(self):
        self.query = 'SELECT * FROM UserDatabaseInfos'

    def get_db_conn_info(self, db_guid):
        try:
            conn = pymssql.connect(
                server='vuonghuynhsolutions.tech',
                user='vuongqhhuynh',
                password='Hoangvuong1024',
                database='nhomeadmin51'
            )

            cursor = conn.cursor()
            cursor.execute(self.query)
            fetchedList = cursor.fetchall()
            result = [e for e in fetchedList if e[1] == db_guid]

            db_type = ''

            if result[0][3] == 0:
                db_type = 'mssql'
            elif result[0][3] == 1:
                db_type = 'mysql'
            elif result[0][3] == 2:
                db_type = 'postgre'

            return_obj = DbConnection(
                result[0][4], result[0][5], result[0][6], result[0][7], db_type, result[0][17])
            return return_obj
        except Exception as ex:
            print(ex)

    def populate_status(self, db_guid, api_download_link, api_guid):
        try:
            conn = pymssql.connect(
                server='vuonghuynhsolutions.tech',
                user='vuongqhhuynh',
                password='Hoangvuong1024',
                database='nhomeadmin51'
            )

            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM UserDatabaseInfos WHERE Guid = '{0}'".format(db_guid))
            fetchedList = cursor.fetchall()
            result = [e for e in fetchedList if e[1] == db_guid]
            if result != None:
                sql = "UPDATE UserDatabaseInfos SET DownloadLinkApi = '{0}', Status = 'Finished', BackEndId = '{2}' WHERE Guid = '{1}'".format(api_download_link,
                                                                                                                                               db_guid,
                                                                                                                                               api_guid
                                                                                                                                               )
                cursor.execute(sql)
                conn.commit()
        except Exception as ex:
            print(ex)
