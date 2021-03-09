import requests # get/post requests module
from DatabaseConnection import DatabaseConnection
import json

class ConnectedRealms:

    # Initialize function with given arguments
    # client_id
    # client_secret
    # region
    def __init__(self, database_params):
        self.database = DatabaseConnection(database_params)

    # Check if request got response and the response status code    
    def checkResponseStatus(self, method, response):
        if response.status_code == 200:
            return True
        else:
            if not response: 
                self.database.insertLog((method + " Failed to reach response"))
            elif response.status_code != 200:
                self.database.insertLog((method + " Failed - Error Code: " + response.status_code))
            return False        

    # Get regions in array (0 - region_id, 1 - region_shortcut)
    def getRegions(self, name=''):
        name = '%' + name + '%'
        return self.database.selectRegions(name)

    def getConnectedRealmsId(self, region=0, name=''):
        name = '%' + name + '%'
        connected_realms_obj = self.database.selectConnectedRealmsId(region, name)
        connected_realms_ids = []
        for row in connected_realms_obj:
            connected_realms_ids.append(row[0])
        return connected_realms_ids

    def requestAllRealms(self, regions, token):

        self.realms = []
        for region in regions:
            self.requestRealms(region, token)
            
        self.database.insertRealms(self.realms)

    def requestRealms(self, region, token, page=1):
 
        params_data = {
            "namespace" : "dynamic-{}".format(region[1]),
            "locale" : "en_GB",
            "status.type" : "UP",
            "orderby" : "id",
            "_page" : page,
            "access_token" : token
        }
        response = requests.get('https://%s.api.blizzard.com/data/wow/search/connected-realm' % region[1], params=params_data)
        # Check if response wasn't succesfull
        if self.checkResponseStatus(self.requestRealms.__name__, response):
            for connected_realms in response.json()['results']:
                for realm in connected_realms['data']['realms']:

                    self.realms.append({
                        "realm_id" : realm['id'],
                        "connected_realm_id" : connected_realms['data']['id'],
                        "region_id" : region[0],
                        "name" : realm['name']['en_GB']
                    })
                   
            if response.json()['page'] < response.json()['pageCount']:
                requestRealms(region, token, page=(page+1))