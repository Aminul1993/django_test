from django.shortcuts import render

def page_not_found(request,exception):
    return render(request,'error.html',{"error_msg" : "404","page_title": "404"},status=404)

def page_error_found(request,exception=None):
    return render(request,'error.html',{"error_msg" : "500","page_title": "500"},status=500)