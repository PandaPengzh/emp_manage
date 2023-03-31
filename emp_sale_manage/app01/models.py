from django.db import models
from datetime import datetime
# Create your models here.


# 部门表
class Department(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title   # 输出department对象时返回的是title

# 员工表
class employee(models.Model):
    name = models.CharField(max_length=20,verbose_name='姓名')
    age = models.IntegerField(verbose_name="年龄")
    create_time = models.DateTimeField(verbose_name="入职日期")
    depart = models.ForeignKey(to='Department',to_field='id',on_delete=models.CASCADE,verbose_name="部门号") # 级联删除
    gender_choice = {
        (1,"男"),
        (2,"女"),
    }
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choice)

    def __str__(self):
        return self.name   # 输出department对象时返回的是title


# 靓号管理
class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号",max_length=11)
    price = models.IntegerField(verbose_name="价格",default=0)

    level_choice = (
        (1,"1级"),
        (2,"2级"),
        (3,"3级"),
        (4,"4级")
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)

    status_choice = (
        (1,"已占用"),
        (2,"未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=2)


# 管理员表
class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=60)

    def __str__(self) -> str:
        return self.username
    

# 任务表
class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详细信息")
    # emp_id
    emp = models.ForeignKey(verbose_name="员工", to="employee", on_delete=models.CASCADE,default=1)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE,default=1)


# 订单表
class Order(models.Model):
    """ 订单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="商品", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    create_time = models.DateTimeField(verbose_name="支付日期",default=datetime.now)
    category = models.CharField(verbose_name="商品分类", max_length=64,default=None)
    status_choices = (
        (1, "待支付"),
        (2, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    # admin_id
    emp = models.ForeignKey(verbose_name="员工", to="employee", on_delete=models.CASCADE,default=1)


# 信息上传
class Boss(models.Model):
    """ 文件信息的上传 """
    name = models.CharField(verbose_name="姓名",max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    img = models.FileField(verbose_name="头像",max_length=64)
