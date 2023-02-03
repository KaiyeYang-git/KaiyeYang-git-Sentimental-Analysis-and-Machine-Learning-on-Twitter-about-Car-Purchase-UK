import pandas as pd,requests as r,spacy, pyinflect,tweepy as tw, datetime as dt, rfc3339, warnings
from bs4 import BeautifulSoup as BS
from pyinflect import getAllInflections
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from itertools import cycle
warnings.filterwarnings('ignore')

car_url='https://www.thesaurus.com/browse/car'
buy_url='https://www.thesaurus.com/browse/buy'
buying_url='https://www.thesaurus.com/browse/buying'
drive_url='https://www.thesaurus.com/browse/drive'

def keyword_extract(url_name,class_name):
    page_name=r.get(url_name)
    soup_name=BS(page_name.content,'html.parser')
    key_soup=soup_name.find('ul', class_=class_name).find_all('a')
    list_name=[]
    for key in key_soup:
        new_key=key['href'][8:].replace('%20',' ')
        list_name.append(new_key)
    return list_name

car_sym=keyword_extract(car_url,'css-1xohnkh e1ccqdb60')[:14]
car_sym.insert(0,'car')
buy_sym=keyword_extract(buy_url,'css-wmtunb e1ccqdb60')[:4]
buy_sym.insert(0,'buy')
buying_sym=keyword_extract(buying_url,'css-1lj4erq e1ccqdb60')[:3]
buying_sym.insert(0,'buying')
buy_sym=buy_sym+buying_sym
drive_sym=keyword_extract(drive_url,'css-n85ndd e1ccqdb60')[:4]
drive_sym.insert(0,'drive')

car_sym.remove('ride')
car_sym.remove('auto')
car_sym.remove('machine')
car_sym.remove('motor')

nlp = spacy.load('en_core_web_sm')

buy_str=' '.join(buy_sym+['invest','shop','transact'])
buy_doc=nlp(buy_str)
buy_extension_list=[]
for num in range(len(buy_doc)):
    token = buy_doc[num]
    if token.tag_ in ['NN','VB','VBG','ABD','ADJ','ADV','VBN','VBZ']:
        buy_extension_list.append(token._.inflect('VB',inflect_oov=True))
buy_extension_list=[ele for ele in list(set(buy_extension_list)) if ele]

def extension(sym):
    sym_str=' '.join(sym)
    sym_token=nlp(sym_str)
    extension_list=[]
    for num in range(len(sym_token)):
        token = sym_token[num]
        if token.tag_ in ['NN','VB','VBG','ABD','ADJ','ADV','VBN','VBZ']:   
            if str(token)!=token._.inflect('VBD',inflect_oov=True)[:len(token)]:
                extension_list.append(token._.inflect('VBD',inflect_oov=True))              
            if str(token)!=token._.inflect('VBG',inflect_oov=True)[:len(token)]:
                 extension_list.append(token._.inflect('VBG',inflect_oov=True))
            if str(token)!=token._.inflect('VBN',inflect_oov=True)[:len(token)]:
                 extension_list.append(token._.inflect('VBN',inflect_oov=True))
            if str(token)!=token._.inflect('VBZ',inflect_oov=True)[:len(token)]:
                 extension_list.append(token._.inflect('VBZ',inflect_oov=True))
            if str(token)!=token._.inflect('VBP',inflect_oov=True)[:len(token)]:
                 extension_list.append(token._.inflect('VBP',inflect_oov=True))
    return extension_list

buy_sym=list(set(extension(buy_extension_list)+buy_extension_list))
buy_sym.append('acquisition')

drive_sym=list(set(extension(drive_sym)+drive_sym))

brand_list=['Ford','BMW','Volkswagen','Mercedes-Benz','Audi','Vauxhall','Toyota','Kia','Hyundai','Land Rover']

brand_abb=['VW','Mercedes','Voho','Landy','Bimmer','MBZ']

brand_model=['fiesta','corolla','Series','polo','sportage','tucson','corsa','A-Class','discovery','A3']

car_type=['coupe','hatchback','sedan','sports','suv']

keylist_of_car=car_sym+brand_list+brand_abb+brand_model+car_type
keylist_of_buy_drive=buy_sym+drive_sym

query_content='('+' '.join(keylist_of_car).replace(' ',' OR ')+') ('+' '.join(keylist_of_buy_drive).replace(' ',' OR ')+') lang:en place_country:GB -is:nullcast -has:links'

api_key='pZi7mlQG0A5Frc6aQtzH52VRK'
api_key_secret='XOoQZPHuLzSkB1hh7R6iqvCBAmkuVUOalg1cDN9Z2XUugvEPgn'

access_token='1531378317630357505-CzVmCo7jq1kpB48Mz5UUIP28h2E9ME'
access_token_secret='LeLA1ukTGtdJzINqr5LH2v9Rcs4X51MqAv9ydGQi5ecdT'

bearer_token='AAAAAAAAAAAAAAAAAAAAABzFdAEAAAAAjD2fd8TkXk8hresaamYulARzFYU%3Du05h4N7EfsuBtTAWZsARZpldU4lmTISdzV731S5kGWmQsEfoch'

client = tw.Client(bearer_token,api_key, api_key_secret,access_token, access_token_secret,wait_on_rate_limit=True)

def date_range(start_date, end_date):
    while start_date <= end_date:
        yield start_date
        start_date+=dt.timedelta(hours=8)

start_date = datetime(2019, 9, 1, 0, 00,00)
end_date = datetime(2022, 2, 1, 0, 00,00)

first_time=[]
second_time=[]
for single_date in date_range(start_date, end_date):
    first_time.append(single_date.strftime("%Y-%m-%d %H:%M:%S"))
    second_time.append(single_date.strftime("%Y-%m-%d %H:%M:%S"))

first_time=first_time[:-1]
second_time=second_time[1:]

def rfc_time_convetor(time_list):
    new_time_list=[]
    for single_record in time_list:
        datetime_object = datetime.strptime(single_record, "%Y-%m-%d %H:%M:%S")
        rfc_records=rfc3339.rfc3339(datetime_object)
        new_time_list.append(rfc_records)
    return new_time_list

rfc_first_time=rfc_time_convetor(first_time)
rfc_second_time=rfc_time_convetor(second_time)

for start_time, end_time in zip(rfc_first_time,rfc_second_time):
    tweet_info_small_list=[]
    tweets=client.search_all_tweets(
                            query_content,                            
                            end_time=end_time,       
                            start_time=start_time,
                            tweet_fields = ["created_at", "text", "lang"],
                            user_fields = ['name', 'username', "location"],
                            sort_order=['relevancy'],
                            expansions='author_id',
                            max_results=100)
    if tweets.includes['users']:
        for tweet,user in zip(tweets.data,tweets.includes['users']):
            tweet_info = {
            'created_at': tweet.created_at,
            'text': tweet.text,
            'source': tweet.source,
            'name': user.name,
            'username': user.username,
            'location': user.location}
            tweet_info_small_list.append(tweet_info)
    else:
        for tweet in tweets.data:
            tweet_info = {
            'created_at': tweet.created_at,
            'text': tweet.text,
            'source': tweet.source,
            'name': None,
            'username': None,
            'location': None}
            tweet_info_small_list.append(tweet_info)
            
    tweets_datasource = pd.DataFrame(tweet_info_small_list)
    tweets_datasource.to_csv('/home2/hzhx55/Dissertation/result.csv',sep=',', mode='a',encoding='utf_8')