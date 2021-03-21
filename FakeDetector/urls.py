from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name="index"),
    path('news/',views.news ,name="news"),
    path('news/news_search',views.news_search,name="news_search"),
    path('news_render',views.news_render,name="news_render"),
    path('verify_news',views.verify_news, name="verify_news"),
    path('news_checker', views.news_checker, name="news_checker"),
    path('phishing_detection', views.phishing_detection, name="phishing_detection"),
    path('phishing_checker', views.phishing_checker, name="phishing_checker")
]