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
class Permission(models.Model):
    class Meta:
        permissions = (
            ('manage_constant_data', '管理常量数据'),
            ('manage_user', '管理用户'),
            ('user_logs', '查看用户操作日志'),
            ('manage_backups', '管理系统数据库备份'),
        )
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

class client(models.Model):
    customer_id = models.IntegerField(verbose_name='客户编号')
    surname = models.CharField(max_length=100,verbose_name='客户姓氏')
    credit_score = models.IntegerField(verbose_name='信用分数')
    geography = models.CharField(max_length=100,verbose_name='客户所在地')
    gender = models.CharField(max_length=50,verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    tenure = models.IntegerField(verbose_name='成为银行客户年数')
    balance = models.FloatField(verbose_name='账户余额')
    num_of_products = models.IntegerField(verbose_name='客户使用产品数量')
    has_cr_card = models.IntegerField(verbose_name='是否拥有本行信用卡')
    is_active_member = models.IntegerField(verbose_name='是否为活跃用户')
    estimated_salary = models.FloatField(verbose_name='估计薪资')
    exited = models.IntegerField(verbose_name='是否已流失')
    Label = models.IntegerField(verbose_name='标签')
    Score = models.FloatField(verbose_name='分数')
