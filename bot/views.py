from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http.response import HttpResponse

import json

from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator


# Create your views here.

from .botbase import FbChatBotBase
#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "puther"
VERIFY_TOKEN = "herand"


class botAPI(generic.View):

    chatbot = FbChatBotBase()
    chatbot.linkPage(PAGE_ACCESS_TOKEN, VERIFY_TOKEN)

    def get(self, request, *args, **kwargs):
        message = self.chatbot.gethubrequest(request)
        return HttpResponse(message)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        fb_message = json.loads(request.body.decode('utf-8'))
        return HttpResponse('this is post method')

def messengerplug(request):
    return render(request,'bot/messenger.html')