from ConnectedRealms import ConnectedRealms
from DatabaseConnection import DatabaseConnection
from datetime import datetime # os datetime module
import pandas as pd # pandas library
import requests # get/post requests module
from io import StringIO

import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)

def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)

def addapt_numpy_float32(numpy_float32):
    return AsIs(numpy_float32)

def addapt_numpy_int32(numpy_int32):
    return AsIs(numpy_int32)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.float64, addapt_numpy_float64)
register_adapter(np.int64, addapt_numpy_int64)
register_adapter(np.float32, addapt_numpy_float32)
register_adapter(np.int32, addapt_numpy_int32)
register_adapter(np.ndarray, addapt_numpy_array)

class AuctionHouse:

    def __init__(self, database_params):
        self.connected_realms = ConnectedRealms(database_params)
        self.database = DatabaseConnection(database_params)

    def analyzeAuctions(self, auctions, connected_realm_id):
        auction_df = pd.DataFrame( auctions )
        #auction_df = self.database.Tables.Auctions()
        # Expand the item column
        auction_df.rename(columns={ auction_df.columns[0]: "auction_id"}, inplace = True)
        auction_df = pd.concat([auction_df.drop(['item'], axis=1), auction_df['item'].apply(pd.Series)], axis=1)# Drop 'bonus_list' and 'modifiers' 
        auction_df.rename(columns={ auction_df.columns[6]: "item_id"}, inplace = True)
        auction_df['unit_price'] = auction_df['unit_price'].fillna(auction_df['buyout'])
        auction_df.drop('buyout', axis=1, inplace=True)
        #   These are subgroups of an equipable item with the bonus stats (intellect agility, strength, etc)
        #makes int from float 
        int_64_cols = ['unit_price', 'bid', 'item_id']
        int_32_cols = ['context', 'pet_breed_id', 'pet_level', 'pet_quality_id', 'pet_species_id']
        auction_df[int_32_cols] = auction_df[int_32_cols].astype('Int32')
        auction_df[int_64_cols] = auction_df[int_64_cols].astype('Int64')
        auction_df['connected_realm_id'] = connected_realm_id
        auction_df['modifiers'] = auction_df['modifiers'].fillna('')
        auction_df['modifiers'] = auction_df['modifiers'].astype(str)
        return auction_df
        
    def getAuctions(self, token, region):
        #connected_realms_ids = self.connected_realms.getConnectedRealmsId(3, 'Doomhammer')
        params_data = {'namespace': 'dynamic-{}'.format(region[1]), 'locale': 'en_GB', 'access_token': token}

        for connected_realm_id in self.connected_realms.getConnectedRealmsId(region[0]):
            if (connected_realm_id == 1402): 
                response = requests.get('https://%s.api.blizzard.com/data/wow/connected-realm/%d/auctions' % (region[1], connected_realm_id), params=params_data)
                auction_df = self.analyzeAuctions(response.json()['auctions'], connected_realm_id)
                #print(auction_df)

                ################## 1
                #auction_df.to_sql(
                #    'temp_auctions', 
                #    con=self.database.engine, 
                #    index=False, 
                #    if_exists='replace'
                #)
                ################## 2
                #connection = self.database.engine.raw_connection()
                #cursor = connection.cursor()
                #buffer = StringIO()
                #auction_df.to_csv(buffer, index=False, header=False)
                #buffer.seek(0)
                #cursor.copy_from(buffer, 'temp_auctions', sep=",")
                #connection.commit()
                #print("copy_from_stringio() done")
                #cursor.close()
                ################## 3 
                
                s = self.database.session()
                s.bulk_insert_mappings(self.database.Tables.TempAuctions, auction_df.to_dict(orient="records"))
                s.close()

                #auction_df.to_sql('temp_auctions', con=self.database.engine, index=False, if_exists='append', chunksize=25000, method=None)

    def getAllAuctions(self, token):

        self.database.initConnection()
        regions = self.connected_realms.getRegions()
        for region in regions: 
            self.getAuctions(token, region)