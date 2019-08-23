from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import logout
from .forms import UserregisterForm,LoginForm,PasswordChangeForm,PasswordResetForm,UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import userdata,Profile

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method=='POST':
        form=UserregisterForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            user=userdata(username=username,email=email,password=password)
            user.save()
            messages.success(request,'You have registered successfully,you can login now')
            return redirect('login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form=UserregisterForm()
        return render(request,'register.html',{'form':form})

def Login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user=userdata.objects.filter(username=username,password=password)
            if user:
                return redirect('profile')
            else:
                messages.success(request,'Please enter a correct username and password')
                return redirect('login')
    else:
        form=LoginForm()
        return render(request,'login.html',{'form':form})

def Logout(request):
    return render(request,'logout.html')

def password_Change(request):
    if request.method=='POST':
        form=PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password=request.POST['old_password']
            password=request.POST['new_password']
            data=userdata.objects.filter(user=request.user)
            if data:
                   data.update(password=password)
                   messages.success(request,'Your password was Changed,You can login now')
                   return redirect('login')
            else:
                messages.success(request,'your view has errors')
                return redirect('change_password')

        else:
            return render(request, 'change_password.html', {'form': form})
    else:
        form=PasswordChangeForm()
        return render(request,'change_password.html',{'form':form})



def UserProfileUpdate(request):
    if request.method=='POST':
          u_form=UserUpdateForm(request.POST)
          p_form=ProfileUpdateForm(request.POST,request.FILES)
          context = {
              'u_form': u_form,
              'p_form': p_form
          }
          if u_form.is_valid() and p_form.is_valid():
              username=request.POST['username']
              email=request.POST['email']
              udata=userdata.objects.get(username=username,email=email)
              pdata=Profile(user_id=udata.id,profile=request.FILES['profile'])
              pdata.save()
              messages.success(request,f'your account has been updated')
              return redirect('profile')
          else:
              return render(request, 'profile.html', context)
    else:
        u_form = UserUpdateForm()
        p_form = ProfileUpdateForm()
        context={
             'u_form':u_form,
              'p_form':p_form
        }
        return render(request,'profile.html',context)
