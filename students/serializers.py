from rest_framework import serializers
from .models import students,User,studentdocument

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model=students
        # exclude = ["photo"]
        fields = "__all__"
        read_only_fields = ["id"]

        extra_kwargs = {
            "course": {
                "required": False
            }

        }
    def validate_age(self, value):

         if value < 18:
            raise serializers.ValidationError(
                "Age must be greater than 18."
            )

         return value

    def validate_name(self, value):

         if not value.isalpha():
          raise serializers.ValidationError(
            "Name should contain only letters."
        )

         return value

    def validate_email(self, value):

         if not value.endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Only Gmail is allowed."
            )

         return value

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

class StudentDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = studentdocument
        fields = "__all__"
        read_only_fields = ["id", "uploaded_at"]