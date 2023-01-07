import json
import random
import re
import requests
import datetime

from .models import response


class FbChatBotBase:
    #  ------------------------ Fill this with your page access token! -------------------------------
    PAGE_ACCESS_TOKEN = ""
    VERIFY_TOKEN = ""
    last_msg = ""
    last_req = None

    def linkPage(self, ptoken, vtoken):
        self.PAGE_ACCESS_TOKEN = ptoken
        self.VERIFY_TOKEN = vtoken

    def gethubrequest(self, request):
        self.last_req = request
        mode = request.GET["hub.mode"]
        token = request.GET["hub.verify_token"]
        challenge = request.GET["hub.challenge"]

        httpreturn = ""
        if (mode and token):
            if (mode == "subscribe" and token == self.VERIFY_TOKEN):
                httpreturn = challenge
            else:
                httpreturn = 'Error, invalid token'
        return httpreturn
    def checkRequestType(self, request):
        self.last_req = request

    def postToChat(self, jasonmsg):
        self.last_msg = jasonmsg
        for entry in self.last_msg['entry']:
            for message in entry['messaging']:
                if 'message' in message and 'sender' in message:
                    self.post_text_msg(message['sender']['id'],
                                       message['message']['text'])

                    # self.send(message['sender']['id'],str(self.last_msg))

        return "done"

    def post_text_msg(self, fbid, recevied_message):
        selectwords = {"hello": ['hello', 'hi', 'hey'], "what": ['what', "why", "who"], "joke": [
            'joke', 'jokes'], "human": ['human', 'robots'], "details": ['details', 'bot', 'detail']}

        user_text = re.sub(r"[^a-zA-Z0-9\s]", ' ',
                           recevied_message).lower().split()

        return_message = ''

        if any(word in user_text for word in selectwords.get("hello")):
            return_message += str(random.choice(
                response.objects.filter(category="hello")).mtext)
        elif any(word in user_text for word in selectwords.get("what")):
            return_message += str(random.choice(
                response.objects.filter(category="what")).mtext)
        elif any(word in user_text for word in selectwords.get("joke")):
            return_message += str(random.choice(
                response.objects.filter(category="joke")).mtext)
        elif any(word in user_text for word in selectwords.get("human")):
            return_message += str(random.choice(
                response.objects.filter(category="human")).mtext)

        if any(word in user_text for word in selectwords.get("details")):
            msg = str(random.choice(
                response.objects.filter(category="details")).mtext)
            self.send(fbid, msg)

        if not return_message:
            return_message = "this is auto chat bot messaging .. \n\nPlease make a question or wait for human respond\n\n"

        fn, ln, pic = self.getSenderInfo(fbid)
        now = datetime.datetime.now()
        greatings = ""
        if now.hour < 12:
            greatings = "Buenos días"
        elif now.hour > 18:
            greatings = "Buenas tardes"
        elif now.hour > 12:
            greatings = "Buenas tardes"

        return_message = f"{greatings} {fn} , \n{return_message}"

        self.send(fbid, return_message)

    def getSenderInfo(self, fbid):
        user_details_url = "https://graph.facebook.com/v2.6/%s" % fbid
        user_details_params = {
            'fields': 'first_name,last_name,profile_pic', 'access_token': f'{self.PAGE_ACCESS_TOKEN}'}
        user_details = requests.get(
            user_details_url, user_details_params).json()

        fn = user_details['first_name']
        ln = user_details['last_name']
        pic = user_details['profile_pic']

        return fn, ln, pic

    def send(self, fbid, return_message):
        post_message_url = f'https://graph.facebook.com/v2.6/me/messages?access_token={self.PAGE_ACCESS_TOKEN}'
        response_msg = json.dumps(
            {"recipient": {"id": fbid}, "message": {"text": return_message}})
        requests.post(post_message_url, headers={
            "Content-Type": "application/json"}, data=response_msg)
