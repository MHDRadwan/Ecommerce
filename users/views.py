from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from store.utils import  cartData,guestOrder
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from store.utils import cartData,CartItemsMixin

class CustomLoginView(CartItemsMixin, LoginView):
    template_name = 'login.html'

class CustomPasswordResetView(CartItemsMixin, PasswordResetView):
    template_name = 'password_reset.html'

class CustomPasswordResetDoneView(CartItemsMixin, PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(CartItemsMixin, PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

class CustomPasswordResetCompleteView(CartItemsMixin, PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    
def logout_view(request):
    data = cartData(request)
    cartItems = data['cartItems']
    logout(request)
    context = {'cartitems': cartItems}
    return render(request, 'logout.html',context)


def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = { 'cartitems': cartItems,'form': form}
    return render(request, 'register.html', context)


@login_required
def profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    # checks if the request method is POST. If it is, it means that the form has been submitted.
    if request.method == 'POST':
        # u_form: This is an instance of UserUpdateForm, which is initialized with the data from the POST request (request.POST).
        # It's also provided with the instance of the current user (request.user). This form is used to update user-related information.
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form: Similar to u_form, it's provided with the instance of the current user's profile (request.user.profile).
        # This form is used to update profile-related information.
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        # The form data is checked against various criteria, including field types, required fields, field lengths,
        # and any custom validation rules defined within the form classes.If the data passes all validation checks, is_valid() returns True,
        # indicating that the form data is valid. Otherwise, it returns False, indicating validation errors.
        if u_form.is_valid and p_form.is_valid():
            # The save() method is called on each valid form (u_form and p_form) to persist the updated data to the corresponding database tables.
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        # If the request method is not POST, it means it's a GET request, so the else block is executed. In this block,
        # two form instances (u_form and p_form) are created without any initial data.
        # They are initialized with the current user's information.
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        # Regardless of whether the request method is POST or GET, a context dictionary is created containing the form instances (u_form and p_form).
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cartitems': cartItems
    }
    return render(request, 'profile.html', context)
