import logging

from django.urls import path
from .views import ObtainJWT, LogoutView, LoginAudit

logger = logging.getLogger(__name__)

urlpatterns = [
    path("login/", ObtainJWT.as_view()),
    path("logout/", LogoutView.as_view()),
    path("login/audit/", LoginAudit.as_view()),
]
