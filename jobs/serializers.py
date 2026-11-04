from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Job, Application, profile, Company




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Category already exists.")
        return value




class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_logo = serializers.ImageField(source='company.logo',read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'company_name', 'company_logo', 'location', 'description',
                  #new
                  'job_type','responsibilities','requirements',
                   
                  #optional
                  'work_mode','experience_level',

                  'salary','created_at', 'is_active', 'is_featured', 'category', 'category_name']
        read_only_fields = ['created_at']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ['user', 'bio', 'location', 'birth_date']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company = serializers.CharField(source='job.company', read_only=True)
    class Meta:
        model = Application
        fields = ['id','job','job_title','company','full_name','email',
                  'cover_letter','status','applied_at']
        read_only_fields = ['status','applied_at']


    def validate(self, attrs):
        user = self.context['request'].user
        if Application.objects.filter(user=user, job=attrs['job']).exists():
            raise serializers.ValidationError("You already applied for this job.")
        return attrs


class AdminApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )
    company = serializers.CharField(
        source='job.company',
        read_only=True
    )
    applicant_username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Application
        fields = ['id','user','applicant_username','job','job_title','company','full_name','email',
                  'cover_letter','status','applied_at',]
        read_only_fields = fields


class AdminApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'date_joined',
        ]
        read_only_fields = fields


class AdminUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']


class CompanySerializer(serializers.ModelSerializer):
    vacancy = serializers.SerializerMethodField(read_only=True)
    jobs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'location', 'bio', 'logo','created_at', 'vacancy', 'jobs']
        read_only_fields = ['created_at', 'vacancy', 'jobs']

    def get_vacancy(self, obj):
        return obj.jobs.filter(is_active=True).count()

    def get_jobs(self, obj):
        try:
            active_jobs = obj.jobs.filter(is_active=True).select_related('category')

            result = []
            for job in active_jobs:
                result.append({
                    "id": job.id,
                    "title": job.title,
                    "location": job.location,
                    "salary": str(job.salary) if job.salary is not None else None,
                    "description": job.description,
                    "responsibilities":job.responsibilities,
                    "requirements":job.requirements,
                    "is_featured": job.is_featured,
                    "is_active": job.is_active,
                    "category": job.category_id,
                    "category_name": job.category.name if job.category else None,
                    "created_at": job.created_at.isoformat() if job.created_at else None,
                })
            return result
        except Exception as e:
            print("Error serializing jobs for company:", e)
            return []