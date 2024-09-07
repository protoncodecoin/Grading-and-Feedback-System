from django.contrib.auth import get_user_model

from rest_framework import viewsets, views, mixins, generics

from core.models import Supervisor, CustomUser
from .serializers import UnsupervisedStudentSerializer, SupervisorsSerializer


class UnsupervisedStudentsViewset(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = get_user_model().objects.filter(
        is_active=True, user_type=CustomUser.UserType.STUDENT
    )
    serializer_class = UnsupervisedStudentSerializer

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(is_active=True, user_type=CustomUser.UserType.STUDENT)
        )
        supervisors = Supervisor.objects.all()
        supervised_students_emails = [sup.student.email for sup in supervisors]
        queryset = queryset.exclude(email__in=supervised_students_emails)
        return queryset


class SupervisorListCreateAPIView(generics.ListCreateAPIView):

    queryset = get_user_model().objects.filter(
        is_active=True, user_type=CustomUser.UserType.SUPERVISOR
    )
    serializer_class = UnsupervisedStudentSerializer

    def post(self, request, *args, **kwargs):

        return super().create(request, *args, **kwargs)
