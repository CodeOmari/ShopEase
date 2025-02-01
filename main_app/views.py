from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main_app.app_forms import CustomerForm, LoginForm
from main_app.models import Customer, Transaction


# Create your views here.

# def test(request):
    # c1 = Customer(first_name='John', last_name='Doe', email='johndoe@x.com',
    #               dob = '2003-02-16', gender='male', weight=74)
    # c1.save()
    #
    # c2 = Customer(first_name='Annette', last_name='Sarah', email='sarahannette@ig.com',
    #               dob='1999-07-26', gender='female', weight=54)
    # c2.save()
    #
    # c3 = Customer(first_name='Mike', last_name='Austin', email='Mikeaust@gmail.com',
    #               dob='2002-11-06', gender='male', weight=63)
    # c3.save()
    #
    # c4 = Customer(first_name='Brandon', last_name='Davies', email='daviesBrand@htp.com',
    #               dob='1996-03-17', gender='male', weight=76)
    # c4.save()

    # customer_count = Customer.objects.count()  # number of customers in database
    # customer_one = Customer.objects.get(id=1)  # SELECT * FROM customers WHERE id=1
    # print(customer_one)
    # customer_two = Customer.objects.get(id=2)  # SELECT * FROM customers WHERE id=1
    # print(customer_two)
    # customer_three = Customer.objects.get(id=3)  # SELECT * FROM customers WHERE id=1
    # print(customer_three)
    # customer_four = Customer.objects.get(id=4)  # SELECT * FROM customers WHERE id=1
    # print(customer_four)
    #
    # t1 = Transaction(item_name = 'Gas Cooker', item_description = 'Grey coloured Armco gas cooker',
    #                  item_quantity = 1, amount = 14990, status = True, customer = customer_one)
    # t1.save()
    #
    # t2 = Transaction(item_name='Fridge', item_description='Grey coloured LG fridge',
    #                  item_quantity=1, amount=15290, status=True, customer = customer_two)
    # t2.save()
    #
    # t3 = Transaction(item_name='Television', item_description='33inch LG Flat Screen',
    #                  item_quantity=1, amount=45750, status=True, customer = customer_three)
    # t3.save() customer_count = Customer.objects.count()  # number of customers in database
    # customer_one = Customer.objects.get(id=1)  # SELECT * FROM customers WHERE id=1
    # print(customer_one)
    # customer_two = Customer.objects.get(id=2)  # SELECT * FROM customers WHERE id=1
    # print(customer_two)
    # customer_three = Customer.objects.get(id=3)  # SELECT * FROM customers WHERE id=1
    # print(customer_three)
    # customer_four = Customer.objects.get(id=4)  # SELECT * FROM customers WHERE id=1
    # print(customer_four)
    #
    # t1 = Transaction(item_name = 'Gas Cooker', item_description = 'Grey coloured Armco gas cooker',
    #                  item_quantity = 1, amount = 14990, status = True, customer = customer_one)
    # t1.save()
    #
    # t2 = Transaction(item_name='Fridge', item_description='Grey coloured LG fridge',
    #                  item_quantity=1, amount=15290, status=True, customer = customer_two)
    # t2.save()
    #
    # t3 = Transaction(item_name='Television', item_description='33inch LG Flat Screen',
    #                  item_quantity=1, amount=45750, status=True, customer = customer_three)
    # t3.save()
    #
    # t4 = Transaction(item_name='Watch', item_description='Black Casio watch',
    #                  item_quantity=4, amount=12000, status=True, customer = customer_four)
    # t4.save()
    #
    # return HttpResponse("Ok, Done!")
    # #
    # t4 = Transaction(item_name='Watch', item_description='Black Casio watch',
    #                  item_quantity=4, amount=12000, status=True, customer = customer_four)
    # t4.save()
    #
    # return HttpResponse("Ok, Done!")
@login_required
def customers(request):
    data = Customer.objects.all().order_by('id').values()
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, 'customers.html', {'data': paginated_data})

@login_required
def add_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} was added!")
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'add_customer.html', {"form": form})

@login_required
def transactions(request):
    item = Transaction.objects.all().order_by('id').values()
    paginator = Paginator(item, 10)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, 'transactions.html', {'item': paginated_data})

@login_required
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('customers')

@login_required
def customer_details(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    transactions = Transaction.objects.filter(customer=customer)
    return render(request, 'customer_details.html', {'customer': customer, 'transactions': transactions})

@login_required
def transaction_details(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'transaction_details.html', {'transaction': transaction})

@login_required
def search_customer(request):
    data = Customer.objects.all()
    search_term = request.GET.get('search')
    data = Customer.objects.filter(Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term)
                                   | Q(email__icontains=search_term))
    paginator = Paginator(data, 10)
    page_number = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger | EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, 'search_customer.html', {'data': paginated_data})

@login_required
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer {form.cleaned_data['first_name']} was updated!")
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'update_customer.html', {"form": form})


def login_user(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login_form.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('customers')
        messages.error(request, "Invalid username or password")
        return render(request, "login_form.html", {"form": form})

@login_required
def signout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account creation for {username} was successful!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

