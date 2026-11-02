from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Job, Application, Profile, Company,Education, Experience, Skill




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

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'company_name', 'location', 'description', 'salary',
                   'created_at', 'is_active', 'is_featured', 'category', 'category_name']
        read_only_fields = ['created_at']


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'profile_picture','full_name','email','phone', 'location', 'headline','bio','cv']
        read_only_fields = ['user','email']

    def validate_cv(self, value):
        if value:
            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError("Only PDF files are allowed.")
 
            if value.size >= 250 * 1024:
                raise serializers.ValidationError("CV size must be less than 250 KB.")

        return value


    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id',
            'degree',
            'institution',
            'field_of_study',
            'result',
        ]

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'job_title',
            'company_name',
            'currently_working',
            'responsibilities',
        ]

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'skill_name',
            'skill_level',
        ]

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