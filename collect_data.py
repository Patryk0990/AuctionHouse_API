import requests
from datetime import datetime
import pandas as pd

# Create a new Access Token
def create_access_token(id, secret, reg):
    data = { 'grant_type': 'client_credentials' }
    response = requests.post('https://%s.battle.net/oauth/token' % reg, data=data, auth=(id, secret))
    return response.json()['access_token']

def get_auctions(auth, conn_realm_id, reg):
    
    namespace_value = 'dynamic-{}'
    params_data = {'namespace': namespace_value.format(reg), 'locale': 'en_GB', 'access_token': auth}
    response = requests.get('https://%s.api.blizzard.com/data/wow/connected-realm/%d/auctions' % (reg, conn_realm_id), params=params_data)
    return response.json()['auctions']

def analyze_auctions(connected_realm_id, region): 
    #dane
    client_id = "a9c124cfb7de4af2be5cf1f874724e4b"
    client_secret = "m3LhynIPxteXWq9rWtopkdlZau18ma7P"

    #pobranie tokenu
    token = create_access_token(client_id, client_secret, region)
    auctions = get_auctions(token, connected_realm_id, region)
    auction_df = pd.DataFrame( auctions )

    # Expand the item column
    auction_df = auction_df.rename(columns={"id": "auction_id",})
    auction_df = pd.concat([auction_df.drop(['item'], axis=1), auction_df['item'].apply(pd.Series)], axis=1)# Drop 'bonus_list' and 'modifiers' 
    #   These are subgroups of an equipable item with the bonus stats (intellect agility, strength, etc)
    auction_df['collection_year'] = datetime.now().strftime('%Y')
    auction_df['collection_month'] = datetime.now().strftime('%m')
    auction_df['collection_day'] = datetime.now().strftime('%d')
    auction_df['collection_hour'] = datetime.now().strftime('%H')
    return auction_df

def get_doomhammer():

    connected_realm_id = 1402
    region = "eu"
    filename = datetime.now().strftime('Doomhammer_EU-%Y-%m-%d-%H-%M.csv')
    analyzed_auction_df = analyze_auctions(connected_realm_id, region)
    analyzed_auction_df.to_csv(filename, index=False)
