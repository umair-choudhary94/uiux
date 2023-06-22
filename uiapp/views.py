from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request,"uiapp/home.html")

def bookmarks(request):
    return render(request,"uiapp/bookmarks.html")

def likedpost(request):
    return render(request,"uiapp/likedpost.html")

def notifications(request):
    return render(request,"uiapp/notifications.html")

def subscription(request):
    return render(request,"uiapp/subscription.html")

def wallet(request):
    return render(request,"uiapp/wallet.html")

def withdraw(request):
    return render(request,"uiapp/withdraw.html")

def payment_history(request):
    return render(request,"uiapp/paymenthistory.html")

def income(request):
    return render(request,"uiapp/income.html")

def customer_support(request):
    return render(request,"uiapp/customersupport.html")

def terms_condition(request):
    return render(request,"uiapp/terms.html")

def blocked_user(request):
    return render(request,"uiapp/blockeduser.html")

def payment_information1(request):
    return render(request,"uiapp/paymentinfo1.html")

def payment_information2(request):
    return render(request,"uiapp/paymentinfo2.html")

def new_post(request):
    return render(request,"uiapp/newpost.html")

def myprofile(request):
    return render(request,"uiapp/myprofile.html")

def edit_profile(request):
    return render(request,"uiapp/editprofile.html")
def chat(request):
    return render(request,"uiapp/chat.html")