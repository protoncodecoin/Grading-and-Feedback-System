from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("unsupervised_students", views.UnsupervisedStudentsViewset)
# router.register("supervisors", views.SupervisorsViewset)

from . import views

urlpatterns = [
    path("", include(router.urls)),
    path("supervisor/", views.SupervisorListCreateAPIView.as_view()),
]
