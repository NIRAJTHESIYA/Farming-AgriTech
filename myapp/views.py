from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,category,products,cart
from .forms import UserRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Sum
import json
from django.http import JsonResponse
# Create your views here.

def index(request):
    Category = category.objects.all()

    context = {
        'Category':Category,

    }
    return render(request,'index.html',context)

def Poduct(request,id):
    user = request.user
    if request.method == "GET":

        product_id = request.GET.get('product_id')

        if product_id is not None:
            print(product_id)
            product = products.objects.get(id=product_id)

            if cart.objects.filter(productid=product).exists():
                messages.success(request, 'This Product already added in cart')
                return redirect("addtocart")
            else:
                Cart = cart(
                    user=request.user.id,
                    productid=product
                )
                Cart.save()
                messages.success(request, 'product are successfully added in cart')
                return redirect("addtocart")



    cat_details = category.objects.get(id=id)
    Category = category.objects.all()
    print(Category)
    prod = products.objects.filter(categoryid__id = id)

    context = {
        'prod':prod,
        'cat_details':cat_details,
        'Category':Category,
    }
    return render(request,'product.html',context)

def pdetails(request,id):
    user = request.user
    Product = products.objects.get(id=id)
    if request.method == "GET":

        product_id = request.GET.get('product_id')

        if product_id is not None:
            print(product_id)
            product = products.objects.get(id=product_id)

            if cart.objects.filter(productid=product).exists():
                messages.success(request, 'This Product already added in cart')
                return redirect("addtocart")
            else:
                Cart = cart(
                    user=user,
                    productid=product,

                )
                Cart.save()
                messages.success(request, 'product are successfully added in cart')
                return redirect("addtocart")


    Category = category.objects.all()
    context = {
        'Product': Product,
        'Category': Category,
    }

    return render(request, 'pdetails.html',context)


def aboutus(request):
    Category = category.objects.all()

    context = {
        'Category': Category,

    }
    return render(request, 'aboutus.html', context)

    return render(request,'aboutus.html')

def contactus(request):
    Category = category.objects.all()

    context = {
        'Category': Category,

    }
    return render(request, 'contactus.html', context)

    return render(request,'contactus.html')

def faq(request):
    Category = category.objects.all()

    context = {
        'Category': Category,

    }
    return render(request, 'faq.html', context)

def gallery(request):
    Category = category.objects.all()

    context = {
        'Category': Category,

    }
    return render(request,'gallery.html',context)

def checkout1(request):
    Category = category.objects.all()
    cartData = cart.objects.filter(user=request.user.id)
    grandTotal = 0


    for i in cartData:
        grandTotal = grandTotal + (i.qty * i.productid.productprice)

    context = {
        'Category': Category,
        'cartData':cartData,
        'grandTotal':grandTotal
    }
    return render(request,'checkout1.html',context)

def add_to_cart(request):
    user = request.user
    delete_product = request.GET.get('delete_prod')
    if delete_product is not None:
        delete_prod = cart.objects.get(id = delete_product)
        delete_prod.delete()
        return redirect('addtocart')
    clear_cart = request.GET.get('clearcart')
    if clear_cart is not None:
       dCart = cart.objects.all()
       dCart.delete()
       return redirect('addtocart')
    Cart = None

    Cart = cart.objects.filter(user=request.user.id)
    Category = category.objects.all()

    context = {
        'Category': Category,
        'Cart':Cart,

    }
    return render(request, 'addtocart.html', context)

def order(request):
    Category = category.objects.all()

    context = {
        'Category': Category,

    }
    return render(request,'order.html',context)
'''
def profile(request):
    return render(request,'profile.html')
'''


class UserRegistrationView(View):
    def get(self, request):
       form = UserRegistrationForm()
       Category = category.objects.all()

       context = {
           'Category': Category,
           'form':form,

       }
       return render(request, 'registration.html',context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'You are successfully registered !')
            form.save()
        return render(request, 'registration.html',
         {'form': form})

def forgotpw(request):
    return render(request,'forgotpw.html')

def resetpw(request):
    return render(request,'resetpw.html')



def more(request):
    return render(request,'more.html')

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',{'form':form,'active':'btn-success'})
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            contactno = form.cleaned_data['contactno']
            reg = Customer(user=usr,name=name,email=email,city=city,address=address,contactno=contactno)
            reg.save()
            messages.success(request,'congratulations!! profile updated successfully')
        return render(request,'profile.html',{'form':form,'active':'btn-success'})

def address(request):
    Category = category.objects.all()
    add = Customer.objects.filter(user = request.user)

    context = {
        'add':add,
        'active':'btn-success',
        'Category':Category,
    }
    return render(request, 'address.html',context)

def updateCart(request):
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        if(cart.objects.filter(user=request.user.id, productid=prod_id)):
            prod_qty = int(request.POST.get('product_qty'))
            usercart=cart.objects.get(productid=prod_id,user=request.user.id)
            usercart.qty = prod_qty
            usercart.save()
            return JsonResponse({'status':"Quantity update..."})
    return redirect('index')