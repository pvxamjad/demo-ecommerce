from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session

        # get request 
        self.request = request

        # get the current session if it in the session
        cart = self.session.get('session_key')

        # if user is new , no session , create new 
        if 'session_key' not in request.session :
            cart = self.session['session_key'] = {}

        # make sure cart available on all pages of the site
        self.cart = cart


    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # logic

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True 

        # deal with logged in user 
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # the cart look to be in {'4':2} convert it to {"4":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # sve the cary into profile model 
            current_user.update(old_cart=str(carty))

 
    def add(self, product,quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # logic

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)


        self.session.modified = True 

        # deal with logged in user 
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # the cart look to be in {'4':2} convert it to {"4":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # sve the cary into profile model 
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)

    def get_pods(self):
        # get ids from cart
        product_ids = self.cart.keys()

        # use ids to lookup in  Db 
        products = Product.objects.filter(id__in=product_ids)

        # return those looked up products 
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # get the cart 
        ourcart = self.cart

        # update dictionary 
        ourcart[product_id] = product_qty

        self.session.modified = True

         # deal with logged in user 
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # the cart look to be in {'4':2} convert it to {"4":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # sve the cary into profile model 
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
    

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart :
            del self.cart[product_id]

        self.session.modified = True

         # deal with logged in user 
        if self.request.user.is_authenticated:
            # get the current user profile 
            current_user = Profile.objects.filter(user__id=self.request.user.id)

            # the cart look to be in {'4':2} convert it to {"4":2}
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            # sve the cary into profile model 
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # get product ids 
        product_ids = self.cart.keys()

        # lookup those keys in our products DB models
        products = Product.objects.filter(id__in=product_ids)

        quantities = self.cart

        # start conting at 0 
        total = 0

        for key, value in quantities.items() :
            # convert key into int 
            key = int(key)
            for product in products :
                if product.id == key:
                    if product.is_sale :
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
                    

        return total 



