from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Job, Application, Company
from .serializers import *
from .models import profile



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


class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError("You already applied for this job.")



class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).select_related('job')



class CountsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'jobs': Job.objects.filter(is_active=True).count(),
            'users': User.objects.count(),
            'applications': Application.objects.count(),
        })




class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = profile.objects.get_or_create(user=self.request.user)
        
        return obj


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    pagination_class = None