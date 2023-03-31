from django.shortcuts import render,HttpResponse


def personal_list(request):

    return render(request,"person.html")


def introduce_list(request):
    return render(request,"introduce.html")