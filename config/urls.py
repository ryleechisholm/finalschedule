from app import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup, name="signup"),
    path('home/', views.home, name="home"),
    path('login/', views.login_page, name="login_page"),
    path('profile/', views.profile, name="profile"),
    path('logout/', views.logoutUser, name="logout"),
    path('admin-only/', views.admin_only, name="admin-only"),
    path('make-schedule/', views.make_schedule, name="make-schedule"),
    path('messagepage/', views.messagepage, name="messagepage"),
    path('updateprofile/', views.updateprofile, name="updateprofile")
]
