from django.shortcuts import render, redirect
from store.models import Cart, Item, Order, Store
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

# Create your views here.
def home(request, category=None):
    search = request.GET.get('search')
    cart = None

    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        try:
            items = Item.objects.all()
            user_store = Store.objects.get(owner=request.user)
            items = items.exclude(id__in=user_store.items.all())
        except Store.DoesNotExist:
            items = Item.objects.all()
    else:
        items = Item.objects.all()

    if category:
        items = items.filter(category=category)
        category = True

    if search:
        items = items.filter(Q(name__icontains=search))

    return render(request, 'home.html',{'items':items,'category': category,'search': search,'cart': cart})

def login_view(request):
    if not request.user.is_authenticated:
        if request.method != "POST":
            return render(request, 'login.html')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, ("Username or password not recognized. Please try again or register."))
                return redirect('login')
    else:
        return redirect('home')

def register_view(request):
    if not request.user.is_authenticated:
        if request.method != "POST":
            return render(request, 'register.html')
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            repeat_password = request.POST.get('repeat_password')

            if username and email and password and repeat_password:
                if password != repeat_password:
                    messages.error(request,("Passwords do not match. Please try again."))
                    context = {
                        'username': username,
                        'email': email,
                    }
                    return render(request, 'register.html', context=context)
                
                try:
                    user = User.objects.get(username=username)
                    messages.error(request,("Username is already taken. Please try again."))
                    context = {
                        'username': username,
                        'email': email,
                    }
                    return render(request, 'register.html', context=context)

                except:
                    user = User.objects.create_user(
                        username = username,
                        email = email,
                        password = password
                    )

                    login(request, user)
                    return redirect('home')
    else:
        return redirect('home')

def logout_view(request):
    logout(request)
    return redirect('home')

def create_item(request):
    if request.user.is_authenticated:  
        if request.method != "POST":
            return render(request, 'create_item.html')
        else:
            name = request.POST.get('name')
            image = request.FILES.get('image')
            category = request.POST.get('category')
            size = request.POST.get('size')
            price = request.POST.get('price')
            description = request.POST.get('description')

            new_item = Item(
                name=name,
                image=image,
                category=category,
                size=size,
                price=price,
                description=description
            )
            new_item.save()
            store = Store.objects.get(owner=request.user)
            store.items.add(new_item)

            return redirect('store_view', username=store.owner)
    else:
        return render(request, 'not_auth.html')

def delete_item(request, id):
    item = Item.objects.get(id=id)
    store = Store.objects.get(items=item)

    if request.method == "POST" and request.user == store.owner:
        item.delete()
        return redirect('store_view', username=store.owner)
    else:
        return redirect('home')

def create_store(request):
    if request.user.is_authenticated:  
        if request.method != "POST":
            return render(request, 'create_store.html')
        else:
            name = request.POST.get('name')
            owner = request.user

            store = Store(
                name = name,
                owner = owner
            )
            store.save()
            
            return redirect('store_view', username=owner)
    else:
        return render(request, 'not_auth.html')
    
def store_view(request, username):
    user = User.objects.get(username=username)
    cart = None
    
    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user)

    try:
        store = Store.objects.get(owner=user)
        items = store.items.all()
    except:
        store = False
        items = False

    return render(request, 'store_view.html', {'store': store,'items': items,'cart': cart})

def item_view(request, id):
    item = Item.objects.get(id=id)
    store = Store.objects.get(items__id=item.id)

    return render(request, 'item_view.html',{'item': item, 'store': store})

def cart(request):
    if request.user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        orders = Order.objects.filter(user=request.user)
        cart_items = cart.items.all()
        ordered_items = []

        for order in orders:
            ordered_items.extend(order.items.all())

        total_price = sum(item.price for item in cart_items)
        
        return render(request, 'cart.html',{'cart_items': cart_items,'total_price': total_price,'ordered_items': ordered_items})
    else:
        return render(request, 'not_auth.html')

def add_to_cart(request, id):
    if request.user.is_authenticated:
        item = Item.objects.get(id=id)
        cart, cart_created = Cart.objects.get_or_create(user=request.user)
        url = request.META.get('HTTP_REFERER', '/')

        if item.status == 'available':
            item.status = 'in_cart'
            cart.items.add(item)
        else:
            item.status = 'available'
            cart.items.remove(item)

        item.save()
        cart.save()

        return redirect(url)
    else:
        return render(request, 'not_auth.html')

def order(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            cart = Cart.objects.get(user=request.user)
            order = Order.objects.create(user=request.user)
            
            for item in cart.items.all():
                item.status = 'sold'
                item.save()
                order.items.add(item)

            cart.items.clear()

            order.save()
            cart.save()
            
            return redirect('cart')
        else:
            return redirect('home')
    else:
        return render(request, 'not_auth.html')
