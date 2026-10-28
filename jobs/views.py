from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Job, Application
from .serializers import *

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created_at', 'salary']
    def get_queryset(self):
        return Job.objects.filter(is_active=True).select_related('category')

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)   # never trust client user id

class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user)

class CountsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response({
            'jobs': Job.objects.count(),
            'users': User.objects.count(),
            'applications': Application.objects.count(),
        })