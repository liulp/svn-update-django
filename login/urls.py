from django.conf.urls import url
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.signin, name='signin'),
    #url(r'^logout/$', views.logout, name='logout'),
    #url(r'^changepwd/$', views.changepwd, name='changepwd'),
    #url(r'^regist/$', views.regist, name='regist'),
    #url(r'^SendCode',views.sendcode),
    url(r'^checked', views.checked),

]