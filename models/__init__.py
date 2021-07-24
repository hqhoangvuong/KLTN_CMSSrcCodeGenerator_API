class ColumnConfig:
    def __init__(self, id, tableid, name, isprimarykey, isforeignkey, ordinalposition, datatype):
        self.Id = id
        self.TableId = tableid
        self.ColumnName = name
        self.PropertyName = ''
        self.IsPrimaryKey = isprimarykey
        self.IsForeignKey = isforeignkey
        self.OrdinalPosition = ordinalposition
        self.DataType = datatype
        
class TableConfig:
    def __init__(self, id, name, explicitname, ishidden, actiongroup):
        self.Id = id
        self.Name = name
        self.ExplicitName = explicitname
        self.ModelName = ''
        self.IsHidden = ishidden
        self.ActionGroup = actiongroup

class DbConnection:
    def __init__(self, server, username, password, database, dbtype, port):
        self.Server = server
        self.Username = username
        self.Password = password
        self.Database = database
        self.DbType = dbtype
        self.ServerPort = port
        
class UserDbConnInfo:
    def __init__(self, id, guid, user_id, db_type, server, username, password, initial_catalog):
        self.Id = id
        self.Guid = guid
        self.UserId = user_id
        self.DbType = db_type
        self.Server = server
        self.Username = username
        self.Password = password
        self.InitialCatalog = initial_catalog
        
class ApiCreateResult:
    def __init__(self, status, api_guid, api_download_link, error_msg='', package_name='', db_guid='', client_app_guid='', client_app_download_link=''):
        self.Status = status
        self.ApiGuid = api_guid
        self.ClientAppGuid = client_app_guid
        self.ApiDownloadLink = api_download_link
        self.ClientAppDownloadLink = client_app_download_link
        self.PackageName = package_name
        self.ErrorMessage = error_msg
        self.DbGuid = db_guid
        