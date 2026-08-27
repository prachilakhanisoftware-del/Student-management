from django import forms
from .models import students
from django.contrib.auth.models import User
from .models import studentdocument


class Registerform(forms.ModelForm):

       password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter password",
            "class": "form-control"
        })
    )
       class Meta:
        model = User
        fields = ["username", "email", "password"]

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Enter username",
                "class": "form-control"
            }),

            "email": forms.EmailInput(attrs={
                "placeholder": "Enter email",
                "class": "form-control"
            }),
        }



def clean_username(self):

         username = self.cleaned_data["username"]

         if len(username) < 5:
            raise forms.ValidationError(
                "Username must contain at least 5 characters."
            )

         return username

    
             





class Studentform(forms.ModelForm):

    class Meta:
        model=students
        fields="__all__"

        widgets={
            "name": forms.TextInput(attrs={
                "placeholder":"enter name",
                "class":"form-control"
            }),
            "email":forms.EmailInput(attrs={
                "class":"form-control",
                "placeholder":"enter email"
            }),
            "course":forms.TextInput(attrs={
                "class":"form-control",
                "placeholder":"enter course"
             }),
              "teacher": forms.Select(attrs={
                "class": "form-control"
            }),

            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

        def clean_email(self):
         email = self.cleaned_data["email"]

         if students.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")

         return email



class StudentDocumentForm(forms.ModelForm):

    class Meta:
        model = studentdocument

        fields = [
            "document_type",
            "file"
        ]

        widgets = {

            "document_type": forms.Select(attrs={
                "class": "form-control"
            }),

            "file": forms.FileInput(attrs={
                "class": "form-control"}),}