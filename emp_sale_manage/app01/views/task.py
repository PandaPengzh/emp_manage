from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt  # 用于解决post请求需要csrf_token验证问题
from app01.utills.form import TaskModelForm
from app01.utills.pagination import Pagination  # 分页
from app01.models import Task
from django.http import JsonResponse  # 序列化存储
import json

def task_list(request):
    """ 任务列表 """
    # 拿数据
    queryset = Task.objects.all()
    # 分页
    page_object = Pagination(request,page_size=5,queryset=queryset)
    form = TaskModelForm()

    context = {
        "form":form,
        "queryset":page_object.queryset,
        "page_string":page_object.html_data()
    }

    return render(request,"task_list.html",context)


@csrf_exempt
def task_ajax(request):
    """ 请求处理 """
    print(request.GET)
    print(request.POST)

    data_dict = {
        "status":True,
        "data":{
            "name":"希区柯克",
            "flim":"惊魂记"
        }
    }
    return HttpResponse(json.dumps(data_dict))


@csrf_exempt
def task_add(request):
    """ 请求处理 """
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {
            "status":True,
            "data":{
                "name":"诺兰",
                "flim":"星际穿越"
            }
        }
        return HttpResponse(json.dumps(data_dict))  # 将请求成功的数据返回给客户端
    
    else:
        data_dict = {
            "status":False,
            "error":form.errors
        }
        return HttpResponse(json.dumps(data_dict))  # 将请求失败的数据返回给客户端
    

def task_delete(request,nid):
    """ 删除任务 """
    if request.method == 'GET':
        Task.objects.filter(id=nid).delete()

        # 重定向
        return redirect('http://127.0.0.1:8000/task/list/')
    

















