from flask import Flask, request
import requests, random
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from pymongo import MongoClient
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello, World! ting tong"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    sender=request.form.get('From')
    mongo_client=MongoClient("mongodb+srv://mybotdatabase:mybotdatabase@cluster0-uuaih.mongodb.net/test?retryWrites=true&w=majority")
    db=mongo_client.get_database('mybotdatabase')
    records=db.mybot_collection     
    #records.update_many({'number':sender.strip()},{'$addToSet': {'requests':msg}},,upsert=True)
    #Dictionary 'links' To respond with random media images
    links={
        1:"https://animals.sandiegozoo.org/sites/default/files/2016-08/category-thumbnail-mammals_0.jpg",
        2:"https://ichef.bbci.co.uk/images/ic/480xn/p049tgdb.jpg",
        3:"https://404store.com/2017/07/26/Beautiful-Animal-Panther.jpg",
        4:"https://i.pinimg.com/originals/d8/02/ea/d802ea3a31a002a44cb4cb0eedd3fd80.jpg",
        5:"https://www.irishcentral.com/uploads/article/99949/cropped_GettyImages-940461304.jpg?t=1551257695"
        } 
    if request.values['NumMedia'] != '0':
        # Use the message SID as a filename.
        filename = request.values['MessageSid']+'.jpg'
        DOWNLOAD_DIRECTORY="images\\"
        with open('{}\\{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)
        # Create reply
        resp = MessagingResponse()
        resp.message(" Thanks for img")
        #TO STORE MESSAGE SENT AND RESPONSE
        records.update_one({'number':str(sender).strip()},{'$push': {'requests':image_url, 'responses':str(resp)[57:-21]}},upsert=True)
        return str(resp)
    else:
        resp = MessagingResponse() #response needs to be sent in a particular format...so we use this
        #resp.message("You said: {}".format(msg)).media("https://images.unsplash.com/photo-1543549790-8b5f4a028cfb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80")
        reply=fetch_reply(msg,sender)
        if(reply=='picture10'):
            resp.message("Here is an image").media(links[random.randint(1,5)])
            
        else:
            resp.message(reply)
            from utils import dict_news
            print("__________________________________________________________________________________________________")
            print("dict_news",dict_news)
            print("__________________________________________________________________________________________________")

            #STORE USER`S NEWS PREFERENCES
            
            if(dict_news['topic']!=""):
                records.update_one({'number':str(sender).strip()},{'$addToSet': {'news_topic':dict_news['topic'] }},upsert=True)
            if(dict_news['location']!=""):
                records.update_one({'number':str(sender).strip()},{'$addToSet': {'news_location':dict_news['location'] }},upsert=True)
            if(dict_news['language']!=""):
                records.update_one({'number':str(sender).strip()},{'$addToSet': {'news_language':dict_news['language'] }},upsert=True)
                
        
        #TO STORE MESSAGE SENT AND RESPONSE
        records.update_one({'number':str(sender).strip()},{'$push': {'requests':msg, 'responses':str(resp)[57:-21]}},upsert=True)
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

