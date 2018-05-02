from django.shortcuts import render
from basic_app import forms
# Create your views here.

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

def index(request):
    return render(request,'basic_app/index.html')

#@login_required
def special(request):
    return render(request,'basic_app/special.html')

@login_required

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered=False
    #user_form=forms.UserForm()
    #userprofile_form=forms.UserProfileInfoForm()
    if request.method=='POST':
        user_form=forms.UserForm(request.POST)
        userprofile_form=forms.UserProfileInfoForm(request.POST)

        if user_form.is_valid() and userprofile_form.is_valid():
            user=user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile=userprofile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']
            profile.save()

            registered=True

        else:
            print(user_form.errors,userprofile_form.errors)

    else:
        user_form=forms.UserForm()
        userprofile_form=forms.UserProfileInfoForm()

    #registered=True
    return render(request,'basic_app/registration.html',{
                            'registered':registered,
                            'user_form':user_form,
                            'userprofile_form':userprofile_form
    })


def user_login(request):

    if request.method=='POST':

        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                #print('logged in')
                return HttpResponseRedirect(reverse('basic_app:special'))

            else:
                return HttpResponse(request,'Account not active')
        else:
            print('someone tried to login and failed')
            print("Username {} tried to login using passowrd{}".format(username,password))
            return HttpResponse('invalid login details')


    else:
        return render(request,'basic_app/login.html',context={})
