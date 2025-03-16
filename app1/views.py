from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db import IntegrityError
from .forms import *
from .models import *
from .cart import Cart

# User Profile View
def home(request):
    return render(request,'home.html')

@login_required
def profile_update(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("product_list")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "accounts/profile_update.html", {"user_form": user_form, "profile_form": profile_form})

@login_required
def profile_info(request):
   profile_info = request.user.profile
   return render(request, "accounts/profile.html",{'profile_inf':profile_info})

@login_required
def my_products(request):
    if hasattr(Product, 'user'):
        products = Product.objects.filter(user=request.user)
    else:
        products = Product.objects.all()
    return render(request, 'my_products.html', {'products': products})

# User Registration View
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
    else:
        form = UserRegistrationForm()
    
    return render(request, "accounts/register.html", {"form": form})

# User Login View
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Ensure user has a profile
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)  # Create a profile if missing
            login(request, user)
            return redirect("profile_update")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "accounts/login.html")


# User Logout View
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Product Listing View
def product_list(request):
    category_id = request.GET.get("category")
    categories = Category.objects.all()

    if category_id:
        product = Product.objects.filter(category_id=category_id)
    else:
        product = Product.objects.all()

    return render(request, "index.html", {"products": product, "categories": categories})

# Cart Views
@login_required
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.add(product)
    messages.success(request, f"{product.name} added to cart!")
    return redirect("cart_detail")

@login_required
def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=pk)
    cart.remove(product)
    messages.success(request, f"{product.name} removed from cart!")
    return redirect("cart_detail")

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})


# Checkout View
@login_required
def checkout(request):
    cart = Cart(request)

    if not cart.cart:  # Ensure cart is not empty before proceeding
        messages.error(request, "Your cart is empty!")
        return redirect("cart_detail")

    order = Order.objects.create(user=request.user, total_price=cart.get_total_price())

    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            quantity=item["quantity"],
            price=item["price"]
        )

    cart.clear()
    messages.success(request, "Order placed successfully!")
    return render(request, "cart/checkout_success.html", {"order": order})

# Search View
def search_view(request):
    query = request.POST.get("search", "")
    
    if query:
        results = Product.objects.filter(name__icontains=query)
    else:
        results = Product.objects.none()

    return render(request, "searching.html", {"postblog": results, "query": query})

def product_details(request, pk):
    detail = get_object_or_404(Product, id=pk)
    return render(request,'product_detail.html', {'datas':detail})