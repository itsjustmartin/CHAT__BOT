from django.urls import include,path
from bot import views

urlpatterns = [
    path('get',views.botAPI.as_view()),
    path('test/',views.test),

    
]