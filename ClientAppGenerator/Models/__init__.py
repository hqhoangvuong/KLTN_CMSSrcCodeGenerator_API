class ColumnConfig:
    def __init__(self, id, tableid, name, isprimarykey, isforeignkey, ordinalposition, datatype, propertyname, explicitname, displaycomponent, isautoincremental):
        self.Id = id
        self.TableId = tableid
        self.ColumnName = name
        self.ExplicitName = explicitname
        self.PropertyName = propertyname
        self.IsPrimaryKey = isprimarykey
        self.IsForeignKey = isforeignkey
        self.DisplayComponent = displaycomponent
        self.OrdinalPosition = ordinalposition
        self.DataType = datatype
        self.IsAutoIncremental = isautoincremental


class TableConfig:
    def __init__(self, id, name, explicitname, ishidden, actiongroup, modelname):
        self.Id = id
        self.Name = name
        self.ExplicitName = explicitname
        self.ModelName = modelname
        self.IsHidden = ishidden
        self.ActionGroup = actiongroup


class ForeignKeyConfig:
    def __init__(self, id, fkname, srctblname, srccolname, srccolpos, reftblname, refcolname, refcolpos, mappedrefcolname, mappedrefcolpos):
        self.Id = id
        self.FkName = fkname
        self.SourceTableName = srctblname
        self.SourceColumnName = srccolname
        self.SourceColumnOrdinalPos = srccolpos
        self.RefrencedTableName = reftblname
        self.RefrencedColumnName = refcolname
        self.RefrencedColumnOrdinalPos = refcolpos
        self.MappedRefrencedColumnName = mappedrefcolname
        self.MappedRefrencedColumnOrdinalPos = mappedrefcolpos


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
    def __init__(self, status, api_guid, api_download_link, error_msg='', package_name='', db_guid=''):
        self.Status = status
        self.ApiGuid = api_guid
        self.ApiDownloadLink = api_download_link
        self.PackageName = package_name
        self.ErrorMessage = error_msg
        self.DbGuid = db_guid

class MasterConfig:
    def __init__(self, id, config_name, config_value):
        self.Id = id
        self.ConfigName = config_name
        self.ConfigValue = config_value
