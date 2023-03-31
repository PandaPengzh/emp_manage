"""mysite2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from app01.views import depart,user,admin,login,task,order,chart,upload,personal
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 部门管理
    path('depart/list/',depart.depart_list),
    path('depart/add/',depart.depart_add),
    path('depart/delete/',depart.depart_delete),
    path('depart/<int:nid>/edit/',depart.depart_edit),
    path('depart/multi/',depart.depart_multi),

    # 用户管理
    path('user/list/',user.user_list),
    path('user/modelform/add/',user.user_modelform_add),
    path('user/<int:nid>/edit/',user.user_edit),
    path('user/<int:nid>/delete/',user.user_delete),

    # 组长管理
    path('admin/list/',admin.admin_list),
    path('admin/modelform/add/',admin.admin_modelform_add),
    path('admin/<int:nid>/edit/',admin.admin_edit),
    path('admin/<int:nid>/delete/',admin.admin_delete),
    path('admin/<int:nid>/reset/',admin.admin_reset),

    # 登录页面管理
    path('login/',login.login),
    path('logout/',login.logout),
    path('image/code/',login.code),

    # 任务页面管理：ajax求请
    path('task/list/',task.task_list),
    path('task/ajax/',task.task_ajax),  # 朝这个地址发的请求
    path('task/add/',task.task_add),  # 朝这个地址发的请求
    path('task/<int:nid>/delete/',task.task_delete),

    # 订单管理
    path('order/list/',order.order_list),  
    path('order/add/',order.order_add),
    path('order/delete/',order.order_delete),
    path('order/edit/',order.order_edit),
    path('order/editsave/',order.order_editsave),

    # 销售数据分析
    path('chart/list/',chart.chart_list),

    # 文件/图片上传
    path('upload/list/',upload.upload_list),
    path('upload/add/',upload.upload_add),
    path('upload/<int:nid>/delete/',upload.upload_delete),
    path('upload/<int:nid>/edit/',upload.upload_edit),

    # 个人页面
    path('personal/',personal.personal_list),
    path('introduce/',personal.introduce_list),

    # 路由重定向
    path('', depart.depart_list),
]
