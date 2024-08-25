from django.shortcuts import render, redirect, get_object_or_404
from myapp.form import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def Home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "index.html", {"products": products})

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration has been successful, you can log in now")
            return redirect('login')
    return render(request, "register.html", {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('login')
        return render(request, "login.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
    return redirect('home')

def cart_page(request):
    if request.user.is_authenticated:
        Cart=cart.objects.filter(user=request.user)
        return render (request,"products/cart.html",{'Cart':Cart})
    else:
        return redirect("/")

def delete_cart(request,cid):
    cartitem=cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")
    
    
@csrf_exempt
def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            product_qty = data['product_qty']
            product_id = data['pid']
            product = Product.objects.get(id=product_id)

            if product:
                cart_item = cart.objects.filter(user=request.user, product=product)
                if cart_item.exists():
                    return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product.quantity >= product_qty:
                        cart.objects.create(user=request.user, product=product, product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock is not Available'}, status=200)
            else:
                return JsonResponse({'status': 'Product Not Found'}, status=404)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=401)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)

def collections(request):
    Category = category.objects.filter(status=0)
    return render(request, "collections.html", {"Category": Category})

def itemView(request, Name):
    if category.objects.filter(Name=Name, status=0).exists():
        Products = Product.objects.filter(category__Name=Name)
        return render(request, "products/index.html", {"Products": Products, "category": Name})
    else:
        messages.warning(request, "No such category found")
        return redirect("collections")

def Product_details(request, CName, PName):
    if category.objects.filter(Name=CName, status=0).exists():
        product = get_object_or_404(Product, Name=PName, status=0)
        return render(request, "products/product_details.html", {"product": product})
    else:
        messages.error(request, "No such category found")
        return redirect("collections")
