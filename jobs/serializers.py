from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Job, Application

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class JobSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    company_logo = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = Job
        fields = ['id','title','company','location','description','salary',
                  'company_logo','created_at','is_active','category','category_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']
    def create(self, data):
        return User.objects.create_user(**data)

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