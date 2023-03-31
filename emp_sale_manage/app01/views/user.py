from django.shortcuts import render,HttpResponse,redirect
from django.utils.safestring import mark_safe  # 标记安全字符串
from app01.utills.pagination import Pagination
from app01.utills.form import UserModelForm  # 导入modelform组件
from app01 import models

# Create your views here.

# 用户管理
def user_list(request):
    """ 员工列表 """
    # for i in queryset:
    #     print(i.id,i.name,i.password,i.age,i.create_time,i.get_gender_display(),i.depart.title)

    queryset = models.employee.objects.all()  
    
    page_object = Pagination(request,queryset,page_size=10)  # 实例化分页对象

    context = {
        "queryset":page_object.queryset,
        "page_string":page_object.html_data()
        }

    return render(request,"user_list.html",context)


def user_modelform_add(request):
    """ 添加员工(modelform版) """
    if request.method == 'GET':
        form = UserModelForm()  # 实例化一个form对象
        return render(request,"user_modelform_add.html",{"form":form})

    else:
        form =UserModelForm(data=request.POST)  # 拿到post请求提交的数据

        if form.is_valid():  # 数据不为空(有效)
            form.save()      # 保存至数据库
            return redirect('http://127.0.0.1:8000/user/list/')
        else:
            return render(request,"user_modelform_add.html",{"form":form})

def user_edit(request,nid):

    """ 编辑员工 """
    row_object = models.employee.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = UserModelForm(instance=row_object)
        return render(request,"user_edit.html",{"form":form})

    else:
        form = UserModelForm(instance=row_object,data=request.POST)
        # 拿到post请求提交的数据

        if form.is_valid():  # 数据不为空(有效)
            form.save()      # 修改后，保存至数据库
            return redirect('http://127.0.0.1:8000/user/list/')
        else:
            return render(request,"user_edit.html",{"form":form})

def user_delete(request,nid):
    """ 删除员工 """
    if request.method == 'GET':
        models.employee.objects.filter(id=nid).delete()
        return redirect("http://127.0.0.1:8000/user/list/")