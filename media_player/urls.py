from django.conf.urls import patterns, url
from media_player import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r"^(?P<media_src>[\w.,/_\-\'\!\ ]+)$", views.media_player, name='media_player'),
)
