from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import sessions
from store.models import Product,Profile
import datetime


def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser : 
        # get the order 
        orders = Order.objects.get(id=pk)
        # get the order items 
        items = OrderItem.objects.filter(order=pk)

        if request.POST :
            status = request.POST['shipping_status']
            # check if true or false 
            if status == 'true' :
                # get the order 

                
                now = datetime.datetime.now()

                order = Order.objects.filter(id=pk)
                # update the status 
                order.update(shipped=True,shipped_date=now)
                messages.success(request, f"{orders.id} moved to Shipped")
                return redirect('not_shipped_dash')
            else:
                # get the order 
                order = Order.objects.filter(id=pk)
                # update the status 
                order.update(shipped=False)
                messages.success(request, f"{orders.id} moved to Not Shipped")
                return redirect('shipped_dash')

        return render(request,'payment/orders.html',{"orders":orders,"items":items})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser :
        orders = Order.objects.filter(shipped=True)
        if request.POST :
            status = request.POST['shipping_status']
            num = request.POST['num']
            # get the order 
            order = Order.objects.filter(pk=num)

            # update the status 
            order.update(shipped=False)

            messages.success(request, f"{num} moved to Not Shipped")
            return redirect('shipped_dash')

        return render(request,'payment/shipped_dash.html',{"orders":orders})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser :
        orders = Order.objects.filter(shipped=False)
        if request.POST :
            status = request.POST['shipping_status']
            num = request.POST['num']
            # get the order 
            order = Order.objects.filter(pk=num)

            # grab the time 
            now = datetime.datetime.now()

            # update the status 
            order.update(shipped=True,shipped_date=now)

            messages.success(request, f"{num} moved to Shipped")
            return redirect('not_shipped_dash')

        return render(request,'payment/not_shipped_dash.html',{"orders":orders})
    else:
        messages.success(request, "Access denied")
        return redirect('home')


def proccess_order(request):
    if request.POST :


        # getting cart info just for totals,quantity and order
        cart = Cart(request)
        cart_products = cart.get_pods
        quantities = cart.get_quants
        totals = cart.cart_total()


        # get biiling info from  the last page 
        payment_form = PaymentForm(request.POST or None)


        # Get shiipping session data 
        my_shipping = request.session.get('my_shipping')


        # gather order info 
        full_name = my_shipping['shipping_first_name'] + ' ' + my_shipping['shipping_last_name']
        email = my_shipping['shipping_email']
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_pincode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals

    
        if request.user.is_authenticated :
            # checking logged in
            user = request.user
            # create order 
            create_order = Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            # add order items 
            # get the order id 
            order_id = create_order.pk


            # get the product stuff
            for product in cart_products() :
                 # get product id 
                product_id = product.id
                # product price 
                if product.is_sale :
                    price = product.sale_price
                else:
                    price = product.price

                # get the quantity 
                for key , value in quantities().items() :
                    if int(key) == product.id:
                        # create order item 
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
                        create_order_item.save()

                # delete the cart after pay 
                for key in list(request.session.keys()) :
                    if key == 'session_key':
                        # delete the key 
                        del request.session['session_key']

                # removing cart details from database
                # first we need to fetch the user 
                current_user = Profile.objects.filter(user__id=request.user.id)
                # removing cart by setting empty string 
                current_user.update(old_cart="")

            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            # as a guest proccess 
            # create order 
            # there is no need for user 
            create_order = Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            create_order.save()

            # add order items 
            # get the order id 
            order_id = create_order.pk


            # get the product stuff
            for product in cart_products() :
                 # get product id 
                product_id = product.id
                # product price 
                if product.is_sale :
                    price = product.sale_price
                else:
                    price = product.price

                # get the quantity 
                for key , value in quantities().items() :
                    if int(key) == product.id:
                        # create order item 
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()


                # delete the cart after pay 
                for key in list(request.session.keys()) :
                    if key == 'session_key':
                        # delete the key 
                        del request.session['session_key']

                
            


            messages.success(request, "Order Placed")
            return redirect('home')

    else:
        messages.success(request, "Access denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_pods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # create a seesion with billing info 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping 

        # check see if user is logged in 
        if request.user.is_authenticated :
            # display the card form 
            billing_form = PaymentForm()

            return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form_info':request.POST,"billing_form":billing_form})
        else:
            # not logged in as a guest 
             # display the card form 
            billing_form = PaymentForm()
            return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form_info':request.POST,"billing_form":billing_form})

        return render(request,'payment/billing_info.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form_info':request.POST})
        
    else:
        messages.success(request, "Access denied")
        return redirect('home')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_pods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated :
        # shipping user details 
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        # shipping form details
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)


        return render(request,'payment/checkout.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form':shipping_form})
    else:
        # for guest purchase 
        shipping_form = ShippingForm(request.POST or None)

        return render(request,'payment/checkout.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals,'shipping_form':shipping_form})

  
def payment_success(request):
    return render(request,'payment/payment_success.html')