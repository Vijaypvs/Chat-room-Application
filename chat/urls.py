from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'logout',views.logout,name='logout'),
    url(r'^$',views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    url(r'login',views.login, name='login'),
    url(r'register',views.register, name='register'),
]