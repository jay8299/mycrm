from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import *
# Create your views here.




@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            #print("valid",form)
            username = form.cleaned_data.get('username')

            messages.success(request, "Account created succesfully for "+username)
            return redirect('login')
    print(form)
    context = {'form':form}
    return render(request,'register.html',context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    customer = request.user.customer
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':total_orders,
               'orders_delivered':orders_delivered, 'orders_pending':orders_pending, 'customer':customer}
    return render(request,'user.html',context)






@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Username or Password is Incorrect")
    context={}
    return render(request,'login.html',context)




def logoutUser(request):
    logout(request)
    return redirect("login")




@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    orders_delivered = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()

    context = {'customers':customers, 'orders': orders, 'total_orders': total_orders,
               'orders_delivered':orders_delivered, 'orders_pending':orders_pending}
    return render(request, 'home.html', context)




@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()

    return render(request, 'product.html', {'products': products})




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()
    orders_count = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {'customer':customer, 'orders':orders, 'ordercount':orders_count, 'myfilter':myfilter}
    return render(request, 'customer.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form, 'customer':customer}
    return render(request, 'order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        form.save()
        return redirect('/')

    context = {'form':form, 'customer':order.customer}
    return render(request, 'order_form.html', context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request,'delete.html',context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['customer','admin'])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'account.html', context)

