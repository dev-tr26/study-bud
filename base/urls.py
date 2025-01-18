
from django.contrib import admin
from django.urls import path
from base import views 

urlpatterns = [
    path('login/',views.loginpage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('admin/', admin.site.urls),
    
    path('', views.home,name = "home"),
    path('room/<str:pk>/', views.room, name ="room"),
    path('profile/<int:pk>/',views.userprofile , name="user_profile"),
    
    path('create_room/', views.createroom, name="create_room"), 
    path('update_room/<str:pk>/',views.updatedRoom, name="update_room"),
    path('delete_room/<str:pk>/',views.deleteRoom, name="delete_room"),
    path('delete_message/<str:pk>/',views.deleteMessage, name="delete_message"),
    
    path('update_user/',views.updateUser, name="update_user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]
