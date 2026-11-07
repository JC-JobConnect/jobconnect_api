from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .models import (Category,Job,Application,Company,Profile,Education,Experience,Skill,)
from .serializers import *
from .models import Profile
from rest_framework.permissions import AllowAny



class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None



class AdminCategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    
    filterset_fields = ['category', 'location']

    search_fields = [
    'title',
    'company__name',   
    'category__name',
    ]

    ordering_fields = ['created_at', 'salary']

    def get_queryset(self):
        queryset = Job.objects.filter(
            is_active=True
        ).select_related('category', 'company')

        min_salary = self.request.query_params.get('min_salary')
        max_salary = self.request.query_params.get('max_salary')

        if min_salary:
            queryset = queryset.filter(salary__gte=min_salary)

        if max_salary:
            queryset = queryset.filter(salary__lte=max_salary)

        return queryset


class AdminJobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.select_related(
        'category',
        'company'
    ).all().order_by('-created_at')

    serializer_class = JobSerializer
    permission_classes = [permissions.IsAdminUser]



class ApplicationCreateView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError(
                "You already applied for this job."
            )


class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(
            user=self.request.user
        ).select_related('job')




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

    parser_classes = [
        MultiPartParser,
        FormParser,
        JSONParser,
    ]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )
        return profile




class EducationView(generics.ListCreateAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(
            profile__user=self.request.user
        )

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )

        serializer.save(profile=profile)


class EducationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Education.objects.filter(
            profile__user=self.request.user
        )




class ExperienceView(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(
            profile__user=self.request.user
        )

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )

        serializer.save(profile=profile)


class ExperienceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(
            profile__user=self.request.user
        )




class SkillView(generics.ListCreateAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(
            profile__user=self.request.user
        )

    def perform_create(self, serializer):
        profile, created = Profile.objects.get_or_create(
            user=self.request.user
        )

        serializer.save(profile=profile)


class SkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(
            profile__user=self.request.user
        )




class AdminApplicationListView(generics.ListAPIView):
    serializer_class = AdminApplicationSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = Application.objects.select_related(
        'user',
        'job',
        'job__company',
        'job__category',
    ).all().order_by('-applied_at')


class AdminApplicationStatusUpdateView(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = AdminApplicationStatusSerializer
    permission_classes = [permissions.IsAdminUser]




class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return AdminUserStatusSerializer

        return AdminUserSerializer




class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    pagination_class = None


class AdminCompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]
