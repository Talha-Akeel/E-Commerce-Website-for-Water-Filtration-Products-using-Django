from django.shortcuts import render, redirect
from .models import Banner,ProductCategory,Product,CartOrder,CartOrderItems,UserAddressBook
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from .forms import AddressBookForm

# Create your views here.

@login_required(login_url='login')
def home(request):
    data=Product.objects.filter(is_featured=True).order_by('-id')
    banners= Banner.objects.all().order_by('-id')
    return render(request,'home.html',{'data':data,'banners':banners})

@login_required(login_url='login')
def product_list(request):
    data=Product.objects.all().order_by('-id')
    # minMaxPrice = Product.objects.aggregate(Min('price'),Max('price'))
    return render(request,'product-list.html',{'data':data})
    # 'minMaxPrice':minMaxPrice

@login_required(login_url='login')
def product_page(request):
    data=ProductCategory.objects.all().order_by('-id')
    return render(request,'product-page.html',{'data':data})

@login_required(login_url='login')
def search(request):
    q=request.GET['q']
    data=Product.objects.filter(product_name__icontains=q).order_by('-id')
    return render(request,'search.html',{'data':data})

# Product List according to Category.
@login_required(login_url='login')
def product_category_list(request,cat_id):
    product_category=ProductCategory.objects.get(id=cat_id)
    data=Product.objects.filter(product_category=product_category).order_by('-id')
    return render(request,'product-category-list.html',{'data':data})

# Product Details page
@login_required(login_url='login')
def product_detail(request,slug,id):
    product=Product.objects.get(id=id)
    return render(request,"product-detail.html",{'data':product})

# filter data
@login_required(login_url='login')
def filter_data(request):
    categories=request.GET.getlist('product_category[]')
    # minMaxPrice = Product.objects.aggregate(Min('price'),Max('price'))
    minPrice=request.GET['minPrice']
    maxPrice=request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts=allProducts.filter(price__gte=minPrice)
    allProducts=allProducts.filter(price__lte=maxPrice)
    if len(categories)>0:
        allProducts=allProducts.filter(product_category__id__in=categories).distinct()

    t=render_to_string('ajax/product-list-ajax.html',{'data':allProducts})
    return JsonResponse({'data':t})


# Add to Cart
@login_required(login_url='login')
def add_to_cart(request):
    # del request.session['cartData']
    cart_product = {}
    cart_product[str(request.GET['id'])] = {
        'productName':request.GET['productName'],
        'productImage':request.GET['productImage'],
        'qty':request.GET['qty'],
        'productPrice':request.GET['productPrice'],
    }
    if 'cartData' in request.session:
        if str(request.GET['id']) in request.session['cartData']:
            cart_data=request.session['cartData']
            cart_data[str(request.GET['id'])]['qty']=int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartData'] = cart_data
        else:
            cart_data = request.session['cartData']
            cart_data.update(cart_product)
            request.session['cartData'] = cart_data
    else:
        request.session['cartData']=cart_product
    return JsonResponse({'data':request.session['cartData'],'totalItems':len(request.session['cartData'])})


# Cart Page
@login_required(login_url='login')
def cart_page(request):
	total_amount=0
	if 'cartData' in request.session:
		for p_id,item in request.session['cartData'].items():
			total_amount+=int(item['qty'])*float(item['productPrice'])
		return render(request, 'cart-page.html',{'cart_data':request.session['cartData'],'totalItems':len(request.session['cartData']),'total_amount':total_amount})
	else:
		return render(request, 'cart-page.html',{'cart_data':'','totalItems':0,'total_amount':total_amount})

# Delete from Cart
@login_required(login_url='login')
def delete_from_cart(request):
    p_id = str(request.GET['id'])
    if 'cartData' in request.session:
        if p_id in request.session['cartData']:
            cart_data = request.session['cartData']
            del request.session['cartData'][p_id]
            request.session['cartData'] = cart_data

    total_amount = 0

    for p_id,item in request.session['cartData'].items():
        total_amount += int(item['qty']) * float(item['productPrice'])

    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartData'],'totalItems':len(request.session['cartData']),'total_amount':total_amount})
    return JsonResponse({'data':t,'totalItems':len(request.session['cartData'])})

# Update the Cart
@login_required(login_url='login')
def update_cart(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartData' in request.session:
        if p_id in request.session['cartData']:
            cart_data = request.session['cartData']
            cart_data[str(request.GET['id'])]['qty']=p_qty
            request.session['cartData'] = cart_data

    total_amount = 0

    for p_id,item in request.session['cartData'].items():
        total_amount += int(item['qty']) * float(item['productPrice'])

    t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartData'],'totalItems':len(request.session['cartData']),'total_amount':total_amount})
    return JsonResponse({'data':t,'totalItems':len(request.session['cartData'])})

# signup
def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmPassword = request.POST.get("confirmPassword")

        if password != confirmPassword:
             return HttpResponse("Your Password and Confirm Password are not same.")
        else:
            my_user = User.objects.create_user(username,email,password)
            my_user.save()
            return redirect("login")
        
    return render(request,'signup.html')

# Login
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
             login(request, user)
             return redirect("home")
        else:
             return HttpResponse("Username and Password is incorrect.")
    return render(request,'login.html')

# Logout
def logout_page(request):
     logout(request)
     return redirect('login')

# Checkout
@login_required(login_url='login')
def checkout(request):
    total_amount=0
    totalAmount=0
    if 'cartData' in request.session:
        for p_id,item in request.session['cartData'].items():
            totalAmount+=int(item['qty'])*float(item['productPrice'])
        # Order
        order=CartOrder.objects.create(
             user=request.user,
             total_amount=totalAmount,
        )
        # End
        for p_id,item in request.session['cartData'].items():
            total_amount+=int(item['qty'])*float(item['productPrice'])
            # Order Items
            items=CartOrderItems.objects.create(
                 order=order,
                 invoice_no='INV-'+str(order.id),
                 item=item['productName'],
                 image=item['productImage'],
                 quantity=item['qty'],
                 price=item['productPrice'],
                 total=float(item['qty'])*float(item['productPrice']),
            )
            # End

        # process payment
        host = request.get_host()
        paypal_dict = {
                'business': settings.PAYPAL_RECEIVER_EMAIL,
                'amount': total_amount,
                'item_name': 'OrderNo-'+str(order.id),
                'invoice': 'INV-'+str(order.id),
                'currency_code': 'USD',
                'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
                'return_url': 'http://{}{}'.format(host,reverse('payment-done')),
                'cancel_return': 'http://{}{}'.format(host,reverse('payment-cancelled')),
            }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address=UserAddressBook.objects.filter(user=request.user,status=True).first()
        return render(request, 'checkout.html',{'cart_data':request.session['cartData'],'totalItems':len(request.session['cartData']),'total_amount':total_amount,'form':form,'address':address})
        # Clear cart after successful payment
        # del request.session['cartData']

        # Ensure a response is returned even with empty cart
        # return render(request, 'checkout.html', {'cart_data': {}, 'totalItems': 0, 'total_amount': 0, 'form': form})
    

    
@csrf_exempt
def payment_done(request):

    # Clear cart after successful payment
    del request.session['cartData']

    returnData=request.POST
    return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_cancelled(request):
	return render(request, 'payment-fail.html')


# User Dashboard
def my_dashboard(request):
     return render(request,"user/dashboard.html")
# My Orders
def my_orders(request):
     orders=CartOrder.objects.filter(user=request.user).order_by("-id")
     return render(request,"user/orders.html",{"orders":orders})
# Order Detail
def my_order_items(request,id):
     order=CartOrder.objects.get(pk=id)
     orderItems=CartOrderItems.objects.filter(order=order).order_by("-id")
     return render(request,"user/order-items.html",{"orderItems":orderItems})

# My Address Book
def my_address_book(request):
     addBook=UserAddressBook.objects.filter().order_by("-id")
     return render(request,"user/address.html",{"addBook":addBook})

# Save Address Book
def save_address(request):
     msg=None
     if request.method == "POST":
          form=AddressBookForm(request.POST)
          if form.is_valid():
               saveForm=form.save(commit=False)
               saveForm.user = request.user
               saveForm.save()
               msg="Data has been saved"
     form=AddressBookForm
     return render(request,"user/add-address.html",{"form":form,'msg':msg})


# Activate Address
@login_required(login_url='login')
def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool':True})