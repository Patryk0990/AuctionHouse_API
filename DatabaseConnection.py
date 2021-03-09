import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import Tables

class DatabaseConnection:
    
    def __init__(self, params):
        self.user = params['user']
        self.pwd = params['password']
        self.host = params['host']
        self.db = params['database']
        self.Tables = Tables
    
    def initConnection(self):
        self.engine = create_engine("postgresql+psycopg2://{}:{}@{}:5432/{}".format(self.user, self.pwd, self.host, self.db))
        self.session = sessionmaker(bind=self.engine)

    def insertRegions(self):
        self.initConnection()
        s = self.session()
        s.add(Tables.Regions(name = 'North America', shortcut = 'us'))
        s.add(Tables.Regions(name = 'Korea', shortcut = 'kr'))
        s.add(Tables.Regions(name = 'Europe', shortcut = 'eu'))
        s.add(Tables.Regions(name = 'Taiwan', shortcut = 'tw'))
        s.commit()
        s.close()    

    def selectRegions(self, name):
        self.initConnection()
        s = self.session()
        response = s.query(Tables.Regions.id, Tables.Regions.shortcut).filter(Tables.Regions.shortcut.like(name)).all()
        s.close()    
        return response

    # Write information to db    
    def insertLog(self, message):   
        self.initConnection()
        s = self.session()
        s.add(Tables.Logs(information = message))
        s.commit()
        s.close()


    def insertRealms(self, realms):
        self.initConnection()
        s = self.session()
        s.query(Tables.Realms).delete()
        s.commit()
        for realm in realms: 
            s.add(Tables.Realms(
                id = realm['realm_id'],
                connected_realm_id = realm['connected_realm_id'],
                region_id = realm['region_id'],
                name = realm['name'],
                )
            )
        s.commit()
        s.close()

    def selectConnectedRealmsId(self, region, name):
        self.initConnection()
        s = self.session()
        if region > 0:
            response = s.query(Tables.Realms.connected_realm_id).filter(Tables.Realms.region_id == region, Tables.Realms.name.like(name)).distinct().all()
        else :
            response = s.query(Tables.Realms.connected_realm_id).filter(Tables.Realms.name.like(name)).distinct().all()
        s.close()    
        return response

    def recreateTables(self):
        self.initConnection()
        Tables.Base.metadata.drop_all(self.engine)
        Tables.Base.metadata.create_all(self.engine)
        self.insertRegions()