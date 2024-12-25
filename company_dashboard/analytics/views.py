from django.shortcuts import render

# Create your views here.


def analytics(request):
    print("hello ")
    return render(request,'analytics.html')

