from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("", views.login_page, name="login"),
    path("login/", views.login_page, name="login"),
    path('home/',views.home, name="home"),
    # path("login/", views.login_page, name="login"),
    path('delete/<int:id>/', views.delete_note, name="delete"),
    path('update/<int:id>/', views.update, name="update"),
    # path('', views.login_page, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_page, name='logout'),
    path('share/<uuid:token>/', views.public_view, name='public_view'),
    path('all_view/', views.all_view, name='all_view'),
    path('del_public/<int:id>/', views.public_del, name='public_del'),
    path('update_public/<int:id>/',views.public_update, name='public_update')

]
