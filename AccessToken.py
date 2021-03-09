import requests # get/post requests module
from DatabaseConnection import DatabaseConnection

class AccessToken:

    # Initialize function with given arguments
    # client_id
    # client_secret
    # region
    def __init__(self, auth_params, region, database_params):
        self.auth_params = auth_params
        self.region = region
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

    # Token authentication from Blizzard OAuth API
    def requestToken(self):
        # Variables
        data = { 'grant_type': 'client_credentials' }
        auth = (self.auth_params['client_id'], self.auth_params['client_secret'])
        # Making POST request
        response = requests.post(('https://%s.battle.net/oauth/token' % self.region), data = data, auth = auth)
        # Check if response wasn't succesfull
        if self.checkResponseStatus(self.requestToken.__name__, response):
            return response.json()['access_token']
            
    # Token validation from Blizzard OAuth API
    def validateToken(self, token):
        # Variables 
        data = {'token' : token}
        # Making POST request
        response = requests.post(('https://%s.battle.net/oauth/check_token' % self.region), data = data)
        if not (self.checkResponseStatus(self.validateToken.__name__, response)):
            return self.requestToken()