from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http.response import HttpResponse


from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from bot import botbase

# Create your views here.


PAGE_ACCESS_TOKEN = ""
VERIFY_TOKEN = "thisisrealtoken213321349827837"
class botAPI(generic.View):
    chatbot = botbase.FbChatBotBase()
    chatbot.linkPage(PAGE_ACCESS_TOKEN,VERIFY_TOKEN)
    def get(self, request, *args, **kwargs):
        message = self.chatbot.gethubrequest(request)
        return HttpResponse(message)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        msg=self.chatbot.postToChat(request)
        return HttpResponse(msg)

