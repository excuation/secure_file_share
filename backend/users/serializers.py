from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSignupSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('client', 'Client'), ('ops', 'Ops')], write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop("role")

        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )

        if role == 'client':
            user.is_client_user = True
            user.is_active = False  # needs email verification
        elif role == 'ops':
            user.is_ops_user = True
            user.is_active = True
            user.email_verified = False

        user.set_password(validated_data['password'])
        user.save()
        return user
