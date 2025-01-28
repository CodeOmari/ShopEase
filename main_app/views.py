from django.http import HttpResponse
from django.shortcuts import render

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

def customers(request):
    data = Customer.objects.all()
    return render(request, 'customers.html', {'customers': data})


def add_customer(request):
    return render(request, 'add_customer.html')


def transactions(request):
    return render(request, 'transactions.html')