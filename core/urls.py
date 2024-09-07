from django.urls import path

from . import views

urlpatterns = [
    path("", views.redirect_to_login, name="redirect_to_login"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("student/", views.student_dashboard, name="student_dashboard"),
    path(
        "coordinator/",
        views.coordinator_dashboard,
        name="coordinator_dashboard",
    ),
    path("supervisor/", views.supervisor_dashboard, name="supervisor_dashboard"),
]
