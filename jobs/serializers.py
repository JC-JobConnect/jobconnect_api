from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Category, Job, Application, profile




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

    class Meta:
        model = Job
        fields = ['id', 'title', 'company', 'location', 'description', 'salary',
                  'company_logo', 'created_at', 'is_active', 'category', 'category_name']
        read_only_fields = ['created_at']




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data



    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


    
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