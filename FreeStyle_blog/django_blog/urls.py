from django.contrib import admin
from web.views import *
from backend.views import *
from django.urls import path
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainBlog/',mainBlog),
    path('giveLike/',giveLike),
    path('sign.html/',sign),
    path('login.html/',login, name="login"),
    path('logOut/',logOut),
    path('check_code/',checkCode),

    path('personalHomePage/<blogSite>/',personalHomePage),
    re_path('personalHomePage/(?P<blogSite>\w+)/(?P<condition>((date)|(category)|(tag)))/(?P<val>[0-9]+)/',personalClassPage),
    re_path('personalHomePage/(?P<blogSite>\w+)/(?P<condition>((date)|(category)|(tag)))/(?P<val>[0-9]+)/(?P<article_id>[0-9]+)/',oneArticle),
    re_path('personalHomePage/(?P<blogSite>\w+)/(?P<article_id>[0-9]+)/',oneArticle),

    path('backendManagement/<blogSite>/',backendManagement),
    re_path('backendManagement/(?P<blogSite>\w+)/(?P<blogCategory>((blog-)[0-9]+|(category-)[0-9]+))/',backendManagement),
    path('backendManagement/<blogSite>/createArticle.html/',createArticle),

    #普通用户，有创建，修改，删除功能
    re_path('backendManagement/(?P<blogSite>\w+)/troubleList.html/',trouble),
    re_path('backendManagement/(?P<blogSite>\w+)/createTrouble.html/',createTrouble),
    re_path('backendManagement/(?P<blogSite>\w+)/editTrouble-(?P<troubleId>[0-9]+).html/',editTrouble),
    re_path('backendManagement/(?P<blogSite>\w+)/detailTrouble-(?P<troubleId>[0-9]+).html/',detailTrouble),

    #超级用户
    re_path('backendManagement/(?P<blogSite>\w+)/troubleReport.html/',troubleReport),



]
