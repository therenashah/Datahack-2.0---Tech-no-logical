from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('uploadhere/',views.uploadhere, name='uploadhere'),
    path('translator/',views.translator, name='translator'),
    path('mydocs/',views.mydocs, name='mydocs'),
     path('chatbot/', views.chatbot_view, name='chatbot'),
    #path('ajax_generate_summary/', views.ajax_generate_summary, name='ajax_generate_summary'),
]