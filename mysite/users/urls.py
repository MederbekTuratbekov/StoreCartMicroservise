from django.urls import path, include
from rest_framework import routers
from .views import RegisterView, CustomLoginView, LogoutView, UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]