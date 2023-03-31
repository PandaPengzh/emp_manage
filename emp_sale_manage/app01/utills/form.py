from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utills.bootstrap import BootstrapModelForm
from app01.utills.md5 import md5
from app01 import models
from django import forms


class UserModelForm(BootstrapModelForm):
    class Meta:
        model = models.employee   # 表名
        fields = ['name',"age","create_time","gender","depart"]  # 字段名


class PrettyModelForm(BootstrapModelForm):
    """添加页面的modelform"""

    # 手机号验证方式一：
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')]  # /d 表示匹配数字 0-9
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price','level','status']

    # 手机号验证方式二（不能存在同一个手机号）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()  # 返回的是true or false

        if exists:
            raise ValidationError("手机号已经存在")
        else:
            return txt_mobile


class NumbereditModelForm(BootstrapModelForm):
    """编辑页面的modelform"""
    # 手机号验证方式一：
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误')]  # /d 表示匹配数字 0-9
    )
    # mobile = forms.CharField(disabled=True,label='手机号')  # 不可更改

    class Meta:
        model = models.PrettyNum  # 表名
        fields = ['mobile','price','level','status']  # 字段名

    # 手机号验证方式二（钩子函数）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists() 
        # 排除自身以外和自己一样的手机号码

        if exists:
            raise ValidationError("手机号已经存在")
        else:
            return txt_mobile


class AdminModelForm(BootstrapModelForm):

    # 新建确认密码字段，对密码不可见
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['username','password','confirm_password']
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    # 输入的密码进行md5加密
    def clean_password(self):
        
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


    # 判断两次输入的密码是否相等（钩子函数）
    def clean_confirm_password(self):
        # print(self.cleaned_data)  # {'username': 'aaaa', 'password': '33ceb07bf4eeb3da587e268d663aba1a', 'confirm_password': '1213'}
        pwd = self.cleaned_data.get('password')
        confirm_pwd = self.cleaned_data.get('confirm_password')
        if pwd != md5(confirm_pwd):
            raise ValidationError('密码不一致')
        return confirm_pwd          # 返回的什么，此字段保存到数据库的就是什么


class AdminResetModelForm(BootstrapModelForm):

    # 新建确认密码字段，对密码不可见
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password','confirm_password']
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    
    def clean_password(self):
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        return pwd


   
    def clean_confirm_password(self):
        # print(self.cleaned_data)
        pwd = self.cleaned_data.get('password')
        confirm_pwd = self.cleaned_data.get('confirm_password')
        if pwd != confirm_pwd:
            raise ValidationError('与第一次输入的密码不一致！')
        return confirm_pwd          # 返回的什么，此字段保存到数据库的就是什么


class LoginForm(forms.Form):
    """ 登录页面form,(继承form和modelform是有区别的) """
    # 自定义了两个字段
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"用户名"}),
        # required=True
    )
    password= forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"密码"},render_value=True),
        # required=True
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"请输入验证码"}),
    )

    # 对你输入的密码进行加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    
class TaskModelForm(BootstrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class OrderModelForm(BootstrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid","create_time"]   # 排除某个字段
    

class uploadModelForm(BootstrapModelForm):
   
    # 不添加样式
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.Boss
        # 所有字段
        fields = "__all__"
        




