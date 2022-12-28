from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http.response import HttpResponse

import json
import random
import re
import requests

from .models import response

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator


# Create your views here.

#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "your access  token"
VERIFY_TOKEN = "your verification token"


class botAPI(generic.View):
    def get(self, request, *args, **kwargs):
        mode = request.GET["hub.mode"]
        token = request.GET["hub.verify_token"]
        challenge = request.GET["hub.challenge"]

        if (mode and token):
            if (mode == "subscribe" and token == VERIFY_TOKEN):
                return HttpResponse(challenge)
            else:
                return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        fb_message = json.loads(self.request.body.decode('utf-8'))
        for entry in fb_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    post_facebook_message(
                        message['sender']['id'], message['message']['text'])
        return HttpResponse('this is post method')


def post_facebook_message(fbid, recevied_message):
    selectwords = {"hello": ['hello', 'hi', 'hey'],
                   "what": ['what', "why", "who"],
                   "joke": ['joke'],
                   "human": ['human', 'more details']}

    user_text = re.sub(r"[^a-zA-Z0-9\s]", ' ',
                       recevied_message).lower().split()
    return_message = ''

    done = False

    for text in user_text:
        if any(word in user_text for word in selectwords.get("hello")) and not done:
            return_message += str(random.choice(
                response.objects.filter(category="hello")).mtext)
            done = True

        elif any(word in user_text for word in selectwords.get("what")) and not done:
            return_message += str(random.choice(
                response.objects.filter(category="what")).mtext)
            done = True
        elif any(word in user_text for word in selectwords.get("joke")) and not done:
            return_message += str(random.choice(
                response.objects.filter(category="joke")).mtext)
            done = True
        elif any(word in user_text for word in selectwords.get("human")) and not done:
            return_message += str(random.choice(
                response.objects.filter(category="human")).mtext)
            done = True
    if not return_message:
        return_message = "Welcome to chat bot messaging .. \n\nPlease make a question or wait for human respond\n\n"

    post_message_url = f'https://graph.facebook.com/v2.6/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    response_msg = json.dumps(
        {"recipient": {"id": fbid}, "message": {"text": return_message}})
    print(response_msg)
    status = requests.post(post_message_url, headers={
                           "Content-Type": "application/json"}, data=response_msg)
    print(status.json())