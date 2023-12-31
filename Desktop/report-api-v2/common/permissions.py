from typing import List

from rest_framework.permissions import BasePermission


def get_permissions(user_data: dict) -> List[str]:
    posts = user_data.get("post", "").lower().split("/")
    for post in posts:
        if (
            "muhtamim" in post or "mulk" in post or "muhtamin" in post
        ):  # We'll refactor this
            return ["READ:0", "WRITE:0"]
        if post == "state qaid":
            return ["READ:1", "WRITE:1"]
        if post == "dila qaid":
            return ["READ:2", "WRITE:2"]
        if post == "muqami qaid":
            return ["READ:3", "WRITE:3"]
    return []


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        permissions = ["READ:0", "WRITE:0"]
        return all([permission in user.permissions for permission in permissions])


class IsQaid(BasePermission):
    """
    Permission for Qaideens
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        permissions = ["READ:1", "WRITE:1", "READ:2", "WRITE:2", "READ:3", "WRITE:3"]
        # True if at least 2 permissions are present
        return (
            len(
                [
                    permission
                    for permission in permissions
                    if permission in user.permissions
                ]
            )
            >= 2
        )
