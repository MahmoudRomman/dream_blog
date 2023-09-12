from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from posts.models import Category
from django.contrib.auth.decorators import login_required
from validate_email import validate_email
from accounts import models as accounts_model
# Create your views here.


# def register(request):
#     categories = Category.objects.all()
#     if request.method == "POST":
#         form = forms.MyUserCreationForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             email_validation = validate_email(email, verify=True) 
#             print(email_validation)
#             if email_validation:
#                 form.save()
#                 username = form.cleaned_data.get('username')
#                 messages.success(request, f'Account has been created for {username}, Login to continue.')

#                 return redirect('user-login')
#             else:
#                 messages.error(request, f'{email} is invalid')
#                 return redirect('user-register')

#     else:
#         form = forms.MyUserCreationForm()
        
#     context = {
#         'form' : form,
#         'categories' : categories,
#     }
#     return render(request, 'accounts/register.html', context)



def register(request):
    categories = Category.objects.all()
    form = forms.MyUserCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}, Login to continue.')

            return redirect('user-login')

        else:
            messages.error(request, "Sorry, try again.")
            form = forms.MyUserCreationForm()
        
    context = {
        'form' : form,
        'categories' : categories,
    }
    return render(request, 'accounts/register.html', context)




@login_required(login_url='user-login')
def profile(request, pk):
    categories = Category.objects.all()
    context = {
        'categories' : categories,
    }

    return render(request, 'accounts/profile.html', context)



# @login_required(login_url='user-login')
# def profile_update(request, pk):
#     categories = Category.objects.all()
#     user_profile = accounts_model.User.objects.filter(pk=request.user.id)


#     if request.method == "POST":
#         user_form = forms.UserUpdateForm(request.POST, instance=request.user)
#         profile_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user)


#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('user-profile', pk=request.user.id)
        
#     else:
#         user_form = forms.UserUpdateForm(instance=request.user)
#         profile_form = forms.ProfileUpdateForm(instance=request.user)

#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'categories' : categories,
#         'user_profile' : user_profile,
#     }

#     return render(request, 'accounts/profile_update.html', context)




@login_required(login_url='user-login')
def profile_update(request, pk):
    categories = Category.objects.all()
    user_profile = accounts_model.User.objects.filter(pk=request.user.id)


    if request.method == "POST":
        user_form = forms.UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form = forms.UserUpdateForm(request.POST, request.FILES, instance=request.user)
            user_form.save()
            return redirect('user-profile', pk=request.user.id)
        
    else:
        user_form = forms.UserUpdateForm(instance=request.user)


    context = {
        'user_form': user_form,
        'categories' : categories,
        'user_profile' : user_profile,
    }

    return render(request, 'accounts/profile_update.html', context)



@login_required(login_url='user-login')
def about(request):
    categories = Category.objects.all()

    context = {
        'categories' : categories,
    }

    return render(request, 'accounts/about.html', context)


