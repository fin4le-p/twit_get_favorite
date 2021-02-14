import tweepy
import os
import mysql.connector
import datetime
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.environ.get('CONSUMER_KEY')
consumer_secret = os.environ.get('CONSUMER_SECRET')
access_key = os.environ.get('ACCESS_KEY')
access_secret = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

favoCountPage: int = 1
favoMaxCount: int = 0
toDayFavo: int = 0

def favoGet(contPage):
    global toDayFavo
    favoCount: int = 0

    try:

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    
        # DBcon
        conn = mysql.connector.connect(
            host='0.0.0.0',
            port='3306',
            user='user',
            password='password',
            database='schema',
            charset='utf8mb4'
        )
        
        cur = conn.cursor(buffered=True)

        cur.execute("SELECT * FROM TWITTER_FAVO_TIMELINE where got_at=(select max(got_at) from TWITTER_FAVO_TIMELINE);")
        selectData = cur.fetchall()
    
        tweets = api.favorites("FIN4LE_P", count=200, page=favoCountPage)
    
        for tweet in tweets:

            favoCount += 1

            for selectDataOne in range(len(selectData)):
                if str(selectData[selectDataOne][0]) == str(tweet.id) and str(selectData[selectDataOne][1]) == str(tweet.user.screen_name):
                    favoCount = 999
                    break
            else:
                twid: int = tweet.id
                user: str = tweet.user.screen_name
                toDt = datetime.datetime.today()
                date = tweet.created_at
                text: str = tweet.text
                favo = int = tweet.favorite_count
                retw = int = tweet.retweet_count

                cur.execute("INSERT INTO TWITTER_FAVO_TIMELINE VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (twid, user, toDt, date, text, favo, retw))
                conn.commit()

                toDayFavo += 1

                continue

            break    
            
        return favoCount
    
    except tweepy.error.TweepError as e:
        print("err")
        print(e.reason)
    except mysql.connector.Error as e:
        print("Error code:", e.errno)        # error number
        print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
        print("Error message:", e.msg)       # error message
        print("Error:", e)                   # errno, sqlstate, msg values
        s = str(e)
        print("Error:", s)                   # errno, sqlstate, msg values
    finally:
        cur.close()
        conn.close()

print("start_favo_count")
favoMaxCount = favoGet(favoCountPage)

while True:
    if favoMaxCount != 999:
        favoCountPage += 1
        favoMaxCount = favoGet(favoCountPage)
    else:
        break

print("toDayFavo : " + str(toDayFavo))
print("success")