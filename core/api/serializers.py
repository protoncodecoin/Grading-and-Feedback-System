from django.contrib.auth import get_user_model

from rest_framework import serializers

from core.models import Supervisor


class UnsupervisedStudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the User Model
    """

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "full_name",
        ]

    def get_full_name(self, obj):
        if isinstance(obj, get_user_model()):
            return f"{obj.get_full_name()}"


class SupervisorsSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Supervisor
        fields = [
            "supervisor",
            "student",
            "full_name",
        ]

    def get_full_name(self, obj):
        if isinstance(obj, Supervisor):
            return f"{obj.supervisor.first_name} {obj.supervisor.last_name}"
