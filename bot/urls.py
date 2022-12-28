from django.urls import include, path
from bot import views

urlpatterns = [
    path(r'token',
         views.botAPI.as_view()),  # r tag is needed

]
