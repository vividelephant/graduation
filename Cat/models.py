from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# # Create your models here.
# class cal(models.Model):
#     value_a = models.CharField(max_length=10)
#     value_b = models.CharField(max_length=10)
#     result = models.CharField(max_length=10)
# class Permission(models.Model):
#     class Meta:
#         permissions = (
#
#         )

class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    job_number = models.CharField(max_length=20, verbose_name='工号')
    telephone = models.CharField(max_length=20, verbose_name='电话号码')
    department = models.CharField(max_length=50, verbose_name='部门')

# 接收到save信号，将扩展表与原表绑定
@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()
