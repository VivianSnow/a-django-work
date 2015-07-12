from django.conf.urls import patterns, url
from login import views

 
urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^logout/$',views.logout,name = 'logout'),                   
    #url(r'^index/$',views.index,name = 'index'),
    url(r'^s-index/$', views.index, name = 's-index'),
    url(r'^s-profile/$', views.s_profile, name = 's-profile'),
    url(r'^s-grade-list/$', views.s_grade_list, name = 's-grade-list'),
    url(r'^t-index/$', views.t_index, name = 't-index'),
    url(r'^t-profile/$', views.t_profile, name = 't-profile'),
    url(r's-change-password/$', views.s_change_password, name = 's-change-password'),
)
