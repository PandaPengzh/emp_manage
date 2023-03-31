from django.shortcuts import render


def chart_list(request):
    return render(request=request,template_name="chart_list.html")

