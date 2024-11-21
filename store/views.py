from django.shortcuts import render,redirect
from .models import Product,Category,Profile
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from payment.models import ShippingAddress
from payment.forms import ShippingForm

from django import forms
from .forms import SignUpForm,UserUpdateForm,ChanePasswordForm,UserInfoForm
from django.db.models import Q
import json
from cart.cart import Cart

def search(request):
    # determine they filled the form 
    if request.method == "POST" :
        searched =request.POST['searched']
        search_value = request.POST['searched']
        # query the products in DB
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched ))
        if not searched :
            messages.success(request, f"No product found on your search {request.POST['searched']}")
            return render(request,'search.html',{'search_value':search_value})
        else:
            return render(request,'search.html',{'searched':searched})

    else:
        return render(request,'search.html',{})



def update_info(request):
    if request.user.is_authenticated :
        # get the current user info 
        current_user = Profile.objects.get(user__id=request.user.id)
        # get the current user shipping info 
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # get orginal user form 
        form = UserInfoForm(request.POST or None, instance=current_user)
        # get orginginal user shipping form 
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid() :
            # saving user info details 
            form.save()
            # saving shipping info details 
            shipping_form.save()
            messages.success(request, "User Info updated!!")
            return redirect('home')
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.success(request, "Must be Logged-In to access the page..")
        redirect('home')


def update_password(request):
    if request.user.is_authenticated :
        current_user = request.user

        # did they fill out the form
        if request.method == 'POST':
            form = ChanePasswordForm(current_user, request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Password Changed Successfully")
                login(request,current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChanePasswordForm(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request, "You must be logged-in")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated :
        current_user = User.objects.get(pk=request.user.id)
        user_form = UserUpdateForm(request.POST or None, instance=current_user)

        if user_form.is_valid() :
            user_form.save()

            login(request, current_user)
            messages.success(request, "User updated suucesfully!!")
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request, "Must be Logged-In to access the page..")
        redirect('home')




def category_summary(request):
        categorys = Category.objects.all()
        return render(request,'category_summary.html',{'categorys':categorys})
    

def category(request, cat):
    name = cat.replace("-"," ")
    
    try:
        category = Category.objects.get(name=name)
        products = Product.objects.filter(category=category)
        return render(request,'category.html',{'product':products,'category':category})
    except:
        messages.success(request, ("Category Doesn't exist"))
        return redirect('home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request,'product.html',{'product':product})


def home(request):
    products = Product.objects.all()
    return render(request,'home.html',{'product':products})



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # shopping cart stuff 
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from db 
            saved_cart =current_user.old_cart
            # conver db string to python dictionary using json loads 
            if saved_cart:
                # convert dictionary using json 
                converted_cart = json.loads(saved_cart)
                # add the loaded cart dictionary to session 
                cart = Cart(request)
                # loop through the cart and add the items from databse 
                for key, value in converted_cart.items() :
                    cart.db_add(product=key, quantity=value)

            messages.success(request, ("Successfully logged-in"))
            return redirect('home')
        else:
            messages.success(request, ("Incorrect credentials try again...."))
            return redirect('login')
    else:
        return render(request,'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("logged out successfully"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request, ("Username created - please fill below...."))
            return redirect('update_info')
        else:
            messages.success(request, ("Error in registration"))
            return redirect('register')
    else:
        return render(request,'registration.html',{'form':form})