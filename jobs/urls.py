from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

router = DefaultRouter()
router.register('jobs', JobViewSet, basename='jobs')
router.register('admin/jobs',AdminJobViewSet,basename='admin-jobs')
router.register('admin/categories',AdminCategoryViewSet,basename='admin-categories')

urlpatterns = [
    path('v1/categories/', CategoryListView.as_view()),
    path('v1/applications/', ApplicationCreateView.as_view()),
    path('v1/my-applications/', MyApplicationsView.as_view()),
    path('v1/', include(router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('v1/profile/', ProfileView.as_view()),
    path('v1/companies/', CompanyListView.as_view()),

    # Admin specific endpoints
    path('v1/dashboard/counts/', CountsView.as_view()),
    path('v1/admin/dashboard/',AdminDashboardStatsView.as_view(),name='admin-dashboard-stats'),
    path('v1/admin/applications/',AdminApplicationListView.as_view(),name='admin-applications'),
    path('v1/admin/applications/<int:pk>/status/',AdminApplicationStatusUpdateView.as_view(),name='admin-application-status-update'),
    path('v1/admin/users/',AdminUserListView.as_view(),name='admin-users'),
    path('v1/admin/users/<int:pk>/status/',AdminUserStatusUpdateView.as_view(),name='admin-user-status'),

]