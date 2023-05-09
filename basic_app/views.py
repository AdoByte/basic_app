from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from basic_app.forms import UserForm, UserInfoForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@login_required
def special(request):
    return render(request, 'basic_app/special.html', {})

def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')     #username in quotes
        password = request.POST.get('password')     #password in quotes

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))    #There should then be a logic in the html file (or somewhere) that allows its display when it's required or the other part displaying when that is required
            else:
                return HttpResponse("Account Not Active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and Password {}.".format(username,password))
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'basic_app/login.html', {})


def register(request):

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)

        profile_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

                profile.save()
                
            registered = True


        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserInfoForm()

    
    return render(request, 'basic_app/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form, 
                            'registered':registered})
