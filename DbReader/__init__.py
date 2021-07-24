import pymssql
from models import DbConnection


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

    def populate_status(self, db_guid, api_download_link, api_guid, frontend_id, clientapp_download_link):
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
                sql = "UPDATE UserDatabaseInfos SET DownloadLinkApi = '{0}', Status = 'Finished', BackEndId = '{2}', FrontEndId = '{3}', DownloadLinkClientApp = '{4}' WHERE Guid = '{1}'".format(api_download_link,
                                                                                                                                                                                                  db_guid,
                                                                                                                                                                                                  api_guid,
                                                                                                                                                                                                  frontend_id,
                                                                                                                                                                                                  clientapp_download_link
                                                                                                                                                                                                  )
                cursor.execute(sql)
                conn.commit()
        except Exception as ex:
            print(ex)

    def get_email_of_user_by_db_guid(self, db_guid):
        try:
            conn = pymssql.connect(
                server='vuonghuynhsolutions.tech',
                user='vuongqhhuynh',
                password='Hoangvuong1024',
                database='nhomeadmin51'
            )

            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT TOP(1) usr.Email, usrDb.InitialCatalog, usrDb.DownloadLinkApi, usrDb.DownloadLinkClientApp FROM AspNetUsers usr (NOLOCK) INNER JOIN UserDatabaseInfos usrDb (NOLOCK) ON usr.Id = usrDb.UserId WHERE usrDb.Guid = '{0}'".format(db_guid))
            fetchedList = cursor.fetchall()
            return fetchedList[0][0], fetchedList[0][1], fetchedList[0][2], fetchedList[0][3]
        except Exception as ex:
            print(ex)
