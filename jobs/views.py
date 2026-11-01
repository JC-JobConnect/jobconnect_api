from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError

from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Job, Application
from .serializers import *
from .models import profile



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created_at', 'salary']


    def get_queryset(self):
        return Job.objects.filter(is_active=True).select_related('category')

class AdminJobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related('category').all().order_by('-created_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAdminUser]


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
            'applications': Application.objects.count(),
        })


class AdminDashboardStatsView(CountsView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        data = super().get(request).data

        data.update({
            'users': User.objects.count(),
            'total_jobs': Job.objects.count(),
            'active_featured': Job.objects.filter(
                is_featured=True,
                is_active=True
            ).count(),
        })

        return Response(data)




class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj, _ = profile.objects.get_or_create(user=self.request.user)
        
        return obj





class AdminApplicationListView(generics.ListAPIView):
    serializer_class = AdminApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = Application.objects.select_related(
        'user', 'job'
    ).all().order_by('-applied_at')



class AdminApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = AdminApplicationStatusSerializer
    permission_classes = [permissions.IsAdminUser]


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = User.objects.all().order_by('-date_joined')


class AdminUserStatusUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminUserStatusSerializer
    permission_classes = [permissions.IsAdminUser]