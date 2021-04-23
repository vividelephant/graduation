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
    customer_id = models.TextField(verbose_name='客户编号')
    surname = models.TextField(verbose_name='客户姓氏')
    credit_score = models.TextField(verbose_name='信用分数')
    geography = models.TextField(verbose_name='客户所在地')
    gender = models.TextField(verbose_name='性别')
    age = models.TextField(verbose_name='年龄')
    tenure = models.TextField(verbose_name='成为银行客户年数')
    balance = models.TextField(verbose_name='账户余额')
    num_of_products = models.TextField(verbose_name='客户使用产品数量')
    has_cr_card = models.TextField(verbose_name='是否拥有本行信用卡')
    is_active_member = models.TextField(verbose_name='是否为活跃用户')
    estimated_salary = models.TextField(verbose_name='估计薪资')
    exited = models.TextField(verbose_name='是否已流失')
    Label = models.TextField(verbose_name='标签')
    Score = models.TextField(verbose_name='分数')

class client_0(models.Model):
    id = models.IntegerField(primary_key=True)
    Label = models.TextField()
    Score = models.TextField()

class client_1(models.Model):
    id = models.TextField( primary_key=True)
    Label = models.TextField()
    Score = models.TextField()



class total_client(models.Model):
    client_id = models.TextField(null=True)
    customer_id = models.TextField(null=True, verbose_name='客户编号')
    surname = models.TextField(null=True, max_length=100,verbose_name='客户姓氏')
    credit_score = models.TextField(null=True, verbose_name='信用分数')
    geography = models.TextField(null=True, max_length=100,verbose_name='客户所在地')
    gender = models.TextField(null=True, max_length=50,verbose_name='性别')
    age = models.TextField(null=True, verbose_name='年龄')
    tenure = models.TextField(null=True, verbose_name='成为银行客户年数')
    balance = models.TextField(null=True, verbose_name='账户余额')
    num_of_products = models.TextField(null=True, verbose_name='客户使用产品数量')
    has_cr_card = models.TextField(null=True, verbose_name='是否拥有本行信用卡')
    is_active_member = models.TextField(null=True, verbose_name='是否为活跃用户')
    estimated_salary = models.TextField(null=True, verbose_name='估计薪资')
    exited = models.TextField(null=True, verbose_name='是否已流失')
    Label = models.TextField(null=True, verbose_name='标签')
    Score = models.TextField(null=True, verbose_name='分数')

    client_0_id = models.TextField(null=True)
    client_0_Label = models.TextField(null=True)
    client_0_Score = models.TextField(null=True)

    client_1_id = models.TextField(null=True)
    client_1_Label = models.TextField(null=True)
    client_1_Score = models.TextField(null=True)