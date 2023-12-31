import json
import logging

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    def create_user(self, mkanid, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not mkanid:
            logger.info("User must have an mkanid")
            raise ValueError("Users must have an mkanid")
        user = self.model(mkanid=mkanid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_dila_qaid(self, mkanid, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not mkanid:
            logger.info("User must have an mkanid")
            raise ValueError("Users must have an mkanid")
        user = self.model(mkanid=mkanid, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mkanid, password):
        """Creates and saves a new super user"""
        user = self.create_user(mkanid, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using mkanid instead of username"""

    mkanid = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_details = models.JSONField(default=dict, null=True, blank=True)
    permissions = models.JSONField(default=list, null=True, blank=True)
    post = models.CharField(
        max_length=255, null=True, blank=True
    )  # Dila Qaid, State Qaid, Muqami Qaid, Mulk Officer

    objects = UserManager()

    USERNAME_FIELD = "mkanid"

    class Meta:
        db_table = "users"

    def get_user_data(self, refresh=True):
        from services.tajneed import TajneedService
        from common.permissions import get_permissions

        if not self.user_details or refresh:
            self.user_details = TajneedService(self).get_user_data(self.mkanid)

        if not self.permissions:
            self.permissions = get_permissions(self.user_details)
        if isinstance(self.user_details, str):
            self.user_details = json.loads(self.user_details)
        self.save()
        return self.user_details

    def get_service(self):
        from services.user import UserService

        return UserService(self)


class LoginAuditModel(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="audits"
    )
    logged_in_user = models.CharField(max_length=255, null=True, blank=True)
    logged_in_time = models.DateTimeField(auto_now_add=True)
    logged_in_name = models.CharField(max_length=255, null=True, blank=True)
    logged_in_success = models.BooleanField(default=True)
    message = models.CharField(max_length=255, null=True, blank=True)
