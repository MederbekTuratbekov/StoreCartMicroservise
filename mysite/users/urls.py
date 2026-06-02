from django.urls import path,include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users',UserProfileViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
]
