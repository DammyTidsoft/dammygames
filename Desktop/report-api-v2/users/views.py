from django.contrib.auth import logout
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from services.login import LoginService
from .models import LoginAuditModel
from .serializer import LoginAuditSerializer, LoginSerializer


class LoginAudit(generics.ListAPIView):
    queryset = LoginAuditModel.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginAuditSerializer


class ObtainJWT(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        mkanid = request.data.get("mkanid")
        password = request.data.get("password")
        login_service = LoginService(mkanid, password)
        status_code, data = login_service.login()
        return Response(data, status=status_code)


class LogoutView(APIView):
    def post(self, request):
        mkanid = request.user.mkanid

        try:
            logout(request)
            return Response(
                {"Success": "{} logged out successfully".format(mkanid)},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response({"Error": "User not found"})
