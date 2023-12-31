from django.urls import path, include

urlpatterns = [
    path("admin/", include("api.v1.admin.urls"), name="admin"),
    path("/", include("api.v1.user.urls"), name="user"),
]
