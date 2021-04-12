from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('advancequery', views.advancequery, name='advancequery'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
    path('delete', views.delete, name='delete'),
    path('addcourse', views.addcourse, name = 'addcourse'),
    path('findcourse', views.findcourse, name = 'findcourse'),
    path('updatecourse', views.updatecourse, name = 'updatecourse'),
    path('deletecourse', views.deletecourse, name = 'deletecourse'),
    path('showalluser', views.showalluser, name='showalluser'),
]