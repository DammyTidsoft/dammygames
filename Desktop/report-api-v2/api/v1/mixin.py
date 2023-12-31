from rest_framework.generics import GenericAPIView

from common.permissions import IsAdmin, IsQaid


class BaseAdminView(GenericAPIView):
    permission_classes = (IsAdmin,)
    tags = ["api/v1/"]


class BaseCreateView(GenericAPIView):
    permission_classes = (IsQaid,)
    tags = ["api/v1/"]
