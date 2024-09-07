from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import random

from .manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None

    class UserType(models.TextChoices):
        STUDENT = "student", "Student"
        COORDINATOR = "coordinator", "Coordinator"
        SUPERVISOR = "supervisor", "Supervisor"

    email = models.EmailField(_("email_address"), unique=True)
    user_generated_id = models.CharField(max_length=300, blank=True)
    user_type = models.CharField(
        max_length=15, choices=UserType.choices, help_text="Type of user"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self) -> str:
        return super().get_full_name()

    def save(self, *args, **kwargs):
        if self.user_generated_id == "":
            user: str = self.email.split("@")[0]
            self.user_generated_id = user + str(random.randrange(1, 10000))

        super(CustomUser, self).save(*args, **kwargs)


class Supervisor(models.Model):
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supervised"
    )
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supervisor_students",
    )

    def __str__(self):
        return f"{self.supervisor.email} supervises {self.student.email}"


class ProjectManager(models.Manager):

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_active=True)


class Project(models.Model):
    title = models.CharField(max_length=500)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now=True)

    active_objects = ProjectManager()  # custom manager
    objects = models.Manager()

    def __str__(self):
        return self.title


class SubmittedWork(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="submitted_projects"
    )
    project_title = models.CharField(max_length=500, blank=False, default="")
    file = models.FileField(upload_to="Projects/%Y/%m/%d")
    date_submitted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_full_name()}: {self.project.title}"


class FeedBack(models.Model):

    class Grade(models.TextChoices):
        A_PLUS = "A+", "A+"
        A = "A", "A"
        B_PLUS = "b+", "B+"
        B = "B", "B"
        C = "c", "C"
        d = "D", "D"
        f = "F", "F"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="feedback"
    )
    # supervisor = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supervisor"
    # )
    work = models.ForeignKey(SubmittedWork, on_delete=models.CASCADE)
    grade = models.CharField(max_length=5, choices=Grade.choices)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.message
