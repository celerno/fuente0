from django.conf.urls import url

from www import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^estado$', views.estado, name='estado'),
  url(r'^refresh$', views.refresh, name='refresh')
]