from apscheduler.schedulers.blocking import BlockingScheduler
from AccessToken import AccessToken 
from ConnectedRealms import ConnectedRealms
from AuctionHouse import AuctionHouse
import config

sched = BlockingScheduler()

# Define objects
access_token = AccessToken(config.auth_params, 'eu', config.database_params)
auction_house = AuctionHouse(config.database_params)

# Define variables
auth_token = access_token.requestToken()

# Define jobs
# If token is invalid or old, create new
if not access_token.validateToken(auth_token):
    auth_token = access_token.requestToken()
auction_house.getAllAuctions(auth_token)



# If token is invalid or old, create new
#if not access_token.validateToken(auth_token):
#    auth_token = access_token.requestToken()
#    print("new token")

#@sched.scheduled_job('cron', second=0)
#def scheduled_job():
#    collect_data.get_doomhammer()

#sched.start()
