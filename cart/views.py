from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages




def cart_summary(request):
    # get the cart
    cart = Cart(request)
    cart_products = cart.get_pods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request,'cart.html',{'cart_products':cart_products,'quantities':quantities,'totals':totals})

def cart_add(request):
    # get the cart 
    cart = Cart(request)

    # test for post
    if request.POST.get('action') == 'post':
        # get stuff 
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))


        # lookup product in DB 
        product = get_object_or_404(Product ,id=product_id)

        # save to session 
        cart.add(product=product,quantity=product_qty) 

        cart_quantity = cart.__len__()

        # return response 
        # response = JsonResponse({'Product name: ':product.name})
        response = JsonResponse({'qty':cart_quantity})
        messages.success(request, ("Item added to cart..."))
        return response
    



def cart_delete(request):
    # get the cart 
    cart = Cart(request)

    # test for post
    if request.POST.get('action') == 'post':
        # get stuff 
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
        messages.success(request, ("Item removed from cart...."))

        return response

def cart_update(request):
    # get the cart 
    cart = Cart(request)

    # test for post
    if request.POST.get('action') == 'post':
        # get stuff 
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id,quantity=product_qty)

        response = JsonResponse({'qty':product_qty})
        messages.success(request, ("Quantity cahanged in cart...."))

        return response
        # return redirect('cart_summary')