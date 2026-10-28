from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')


urlpatterns = [
    path('v1/categories/', CategoryListView.as_view()),
    path('v1/register/', RegisterView.as_view()),
    path('v1/applications/', ApplicationCreateView.as_view()),
    path('v1/my-applications/', MyApplicationsView.as_view()),
    path('v1/dashboard/counts/', CountsView.as_view()),
    path('v1/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('v1/profile/', ProfileView.as_view()),

]