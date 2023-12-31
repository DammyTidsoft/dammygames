from rest_framework import serializers

from users.models import LoginAuditModel, User


class LoginAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAuditModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "mkanid",
            "details",
        )

    def get_details(self, obj):
        return obj.get_user_data()


class LoginSerializer(serializers.Serializer):
    mkanid = serializers.CharField(max_length=10)
    password = serializers.CharField()
