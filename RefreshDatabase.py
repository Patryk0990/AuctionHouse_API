from AccessToken import AccessToken 
from ConnectedRealms import ConnectedRealms
from DatabaseConnection import DatabaseConnection
import config

# Recreate db
database = DatabaseConnection(config.database_params)
database.recreateTables()

# Get access token
access_token = AccessToken(config.auth_params, 'eu', config.database_params)
auth_token = access_token.requestToken()

# Get realms list
connected_realms = ConnectedRealms(config.database_params)
regions = connected_realms.getRegions()
connected_realms.requestAllRealms(regions, auth_token)