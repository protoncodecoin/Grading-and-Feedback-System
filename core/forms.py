from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model

from .models import CustomUser, FeedBack, Project, SubmittedWork, Supervisor


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)


class SubmittedWorkForm(forms.ModelForm):

    class Meta:
        model = SubmittedWork
        fields = ["project", "project_title", "file"]

    def __init__(self, *args, **kwargs):
        super(SubmittedWorkForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(is_active=True)


class FeedBackForm(forms.ModelForm):

    class Meta:
        model = FeedBack
        fields = [
            "grade",
            "work",
            "student",
            "message",
        ]

    def __init__(self, *args, **kwargs):
        super(FeedBackForm, self).__init__(*args, **kwargs)
        self.fields["student"].queryset = get_user_model().objects.filter(
            user_type=CustomUser.UserType.STUDENT
        )
