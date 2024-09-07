from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Project, FeedBack, SubmittedWork, Supervisor

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "user_type",
        "user_generated_id",
        "id",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
        "user_type",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "is_staff",
                    "is_active",
                    "user_type",
                    "user_generated_id",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "first_name",
                    "last_name",
                    "is_active",
                    "user_type",
                    "user_generated_id",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Customize fields displayed on the admin site
    """

    list_display = [
        "title",
        "is_active",
        "created_on",
        "deadline",
    ]
    list_filter = [
        "title",
        "is_active",
        "created_on",
        "deadline",
    ]
    ordering = [
        "is_active",
    ]
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(SubmittedWork)
class SubmittedWorkAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "project",
        "file",
    ]

    list_filter = [
        "student",
        "project",
    ]


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "work",
        "grade",
        "message",
    ]


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    list_display = ["supervisor"]
