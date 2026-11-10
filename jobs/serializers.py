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
    company_logo = serializers.ImageField(source='company.logo',read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'company_name', 'company_logo', 'location', 'description','job_type','responsibilities','requirements','work_mode','experience_level','salary','created_at', 'is_active', 'is_featured', 'category', 'category_name']
        read_only_fields = ['created_at']


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = [
            'user',
            'profile_picture',
            'full_name',
            'email',
            'phone',
            'location',
            'headline',
            'bio',
            'cv',
        ]
        read_only_fields = ['user', 'email']

    def validate_cv(self, value):
        if value:
            if not value.name.lower().endswith('.pdf'):
                raise serializers.ValidationError(
                    "Only PDF files are allowed."
                )

            if value.size > 250 * 1024:
                raise serializers.ValidationError(
                    "CV must be less than or equal to 250 KB."
                )

        return value


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
    full_name = serializers.CharField(source='profile.full_name', read_only=True, default="")
    phone = serializers.CharField(source='profile.phone', read_only=True, default="")
    location = serializers.CharField(source='profile.location', read_only=True, default="")
    headline = serializers.CharField(source='profile.headline', read_only=True, default="")
    bio = serializers.CharField(source='profile.bio', read_only=True, default="")
    
    profile_picture = serializers.ImageField(
        source='profile.profile_picture', 
        read_only=True, 
        allow_null=True
    )
    cv = serializers.FileField(
        source='profile.cv', 
        read_only=True, 
        allow_null=True
    )

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
            'full_name',
            'phone',
            'location',
            'headline',
            'bio',
            'profile_picture',
            'cv',
        ]
        read_only_fields = fields

class AdminUserDetailSerializer(AdminUserSerializer):
    educations = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()

    class Meta(AdminUserSerializer.Meta):
        fields = AdminUserSerializer.Meta.fields + [
            'educations',
            'experiences',
            'skills',
        ]
        read_only_fields = fields

    def _profile(self, obj):
        return getattr(obj, 'profile', None)

    def get_educations(self, obj):
        profile = self._profile(obj)
        if profile is None:
            return []
        return EducationSerializer(profile.educations.all(), many=True).data

    def get_experiences(self, obj):
        profile = self._profile(obj)
        if profile is None:
            return []
        return ExperienceSerializer(profile.experiences.all(), many=True).data

    def get_skills(self, obj):
        profile = self._profile(obj)
        if profile is None:
            return []
        return SkillSerializer(profile.skills.all(), many=True).data


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