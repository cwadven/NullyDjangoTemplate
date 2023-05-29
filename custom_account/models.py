from django.contrib.auth.models import AbstractUser
from django.db import models

from custom_account.consts import UserStatusExceptionTypeSelector
from custom_account.managers import CustomUserManager


class UserProvider(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'custom_account_user_provider'


class UserStatus(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'custom_account_user_status'


class UserType(models.Model):
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'custom_account_user_type'


class User(AbstractUser):
    nickname = models.CharField(max_length=45, blank=True, null=True, db_index=True, unique=True)
    user_type = models.ForeignKey(UserType, models.DO_NOTHING, db_column='user_type_id', blank=True, null=True)
    user_status = models.ForeignKey(UserStatus, models.DO_NOTHING, db_column='user_status_id', blank=True, null=True)
    user_provider = models.ForeignKey(UserProvider, models.DO_NOTHING, db_column='user_provider_id', blank=True, null=True)
    img = models.CharField(max_length=256, blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        managed = True
        db_table = 'custom_account_user'
        verbose_name = '일반 사용자'
        verbose_name_plural = '일반 사용자'

    def raise_if_inaccessible(self):
        if self.user_status_id != 1:
            raise UserStatusExceptionTypeSelector(self.user_status_id).selector()
