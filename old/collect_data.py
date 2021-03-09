# postgresql modules
import psycopg2
from sqlalchemy import create_engine
import requests # get/post requests module
from datetime import datetime # os datetime module
import pandas as pd # pandas library

# Create a new Access Token
def createAccessToken(id, secret, reg):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % reg, data=data, auth=(id, secret))
    return response.json()['access_token']

def getAuctions(auth, conn_realm_id, reg):
    
    namespace_value = 'dynamic-{}'
    params_data = {'namespace': namespace_value.format(reg), 'locale': 'en_GB', 'access_token': auth}
    response = requests.get('https://%s.api.blizzard.com/data/wow/connected-realm/%d/auctions' % (reg, conn_realm_id), params=params_data)
    return response.json()['auctions']

def analyzeAuctions(connected_realm_id, region): 
    #dane
    client_id = "a9c124cfb7de4af2be5cf1f874724e4b"
    client_secret = "m3LhynIPxteXWq9rWtopkdlZau18ma7P"

    #pobranie tokenu
    token = createAccessToken(client_id, client_secret, region)
    auctions = getAuctions(token, connected_realm_id, region)
    auction_df = pd.DataFrame( auctions )

    # Expand the item column
    auction_df = auction_df.rename(columns={"id": "auction_id",})
    auction_df = pd.concat([auction_df.drop(['item'], axis=1), auction_df['item'].apply(pd.Series)], axis=1)# Drop 'bonus_list' and 'modifiers' 
    #   These are subgroups of an equipable item with the bonus stats (intellect agility, strength, etc)
    auction_df['date'] = datetime.now()
    auction_df.astype({'unit_price': 'int64', 'buyout': 'int64', 'bid': 'int64', 'id': 'int64', 'context': 'int32', 'pet_breed_id': 'int32', 'pet_level': 'int32', 'pet_quality_id': 'int32', 'pet_species_id': 'int32'})
    #print(auction_df.dtypes)
    return auction_df

def getDoomhammer():

    connected_realm_id = 1402
    region = "eu"
    #filename = datetime.now().strftime('Doomhammer_EU-%Y-%m-%d-%H-%M.csv')
    analyzed_auction_df = analyzeAuctions(connected_realm_id, region)
    #print(analyzed_auction_df)
    #postDataToDB(analyzed_auction_df, 'Doomhammer')
    #analyzed_auction_df.to_csv(filename, index=False)

getDoomhammer()