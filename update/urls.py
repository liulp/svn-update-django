from django.conf.urls import url
from . import views, update_api

#from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.content, name='content'),
    url(r'^roll_back/$', views.roll_back, name='roll_back'),
    #url(r'^logout/$', views.logout, name='logout'),
    #url(r'^changepwd/$', views.changepwd, name='changepwd'),
    #url(r'^regist/$', views.regist, name='regist'),
    #url(r'^SendCode',views.sendcode),

]