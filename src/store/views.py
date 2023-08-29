from ast import Delete
from unicodedata import category
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import Item, OrderItem, Order, BillingAddress
from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ItemFilter
from django.contrib import messages
from .forms import CheckoutForm
from django.db.models import Q
import stripe
from django.conf import settings #n
from django.http.response import JsonResponse #n
from django.views.decorators.csrf import csrf_exempt #n


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)



def payment_success(request):
    order = Order.objects.get(user=request.user, ordered = False)
    for order_item in order.items.all():
        order_item.ordered = True
        order_item.save()
    order.ordered = True
    order.save()

    return redirect("store:home")

def payment_cancel(request):
    return render(request, "cancel.html")

@csrf_exempt
def create_checkout_session(request):

    domain_url = 'http://localhost:8000'
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user
    order = Order.objects.get(user=user, ordered=False)
    total = order.get_total()
    try:
        checkout_session = stripe.checkout.Session.create(

            success_url= 'http://localhost:8000/success/',
            
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': total*100,
                    'product_data': {
                        'name': 'Cart Total',
                        'description': 'the total of the item in your cart',
                        # 'images': ['https://example.com/t-shirt.png'],
                        },
                },
                'quantity': 1,
            }],
            # cancel_url=YOUR_DOMAIN + '/cancel/'
        )
        return JsonResponse({'sessionId': checkout_session['id']})
    except Exception as e:
        return JsonResponse({'error': str(e)})


class Home(ListView):
    model = Item
    paginate_by = 8
    template_name = "home-page.html"


@login_required
def saved_posts(request):
    user = request.user
    posts = user.wish.all()
    context = {
        'posts': posts,
    }
    return render(request, "saved_posts.html", context)


@login_required
def save_button(request, pk):
    if request.POST.get('action') == 'post':
        data = {}
        post = Item.objects.get(pk=pk)
        if request.user in post.wish.all():
            post.wish.remove(request.user)
        else:
            post.wish.add(request.user)
    return JsonResponse({'data': data})


class ShirtView(ListView):
    paginate_by = 8
    template_name = "shirt-list.html"

    def get_queryset(self):
        self.item = Item.objects.filter(category='shirt')
        return self.item


class SportsView(ListView):
    paginate_by = 8
    template_name = "sports-list.html"

    def get_queryset(self):
        self.item = Item.objects.filter(category='sport')
        return self.item


class OutWearView(ListView):
    paginate_by = 8
    template_name = "outwear-list.html"

    def get_queryset(self):
        self.item = Item.objects.filter(category='outwears')
        return self.item


class SaleView(ListView):
    paginate_by = 8
    template_name = "sale-list.html"

    def get_queryset(self):
        self.item = Item.objects.filter(label='sale')
        return self.item

class NewView(ListView):
    paginate_by = 8
    template_name = "new-list.html"

    def get_queryset(self):
        self.item = Item.objects.filter(label='new')
        print(self.item)
        return self.item

def detail_view(request, pk):
    user = request.user
    item = Item.objects.get(pk=pk)
    related = Item.objects.filter(category=item.category).exclude(pk=item.pk)[:3]
    related_items_count = related.count()
    if related_items_count < 3:
        additional_items_needed = 3 - related_items_count
        additional_items = Item.objects.exclude(
            Q(category=item.category) | Q(pk=item.pk)
        )[:additional_items_needed]
        related = list(related) + list(additional_items)
    post = ""
    if user.is_authenticated:
        posts = user.wish.all()
        post = item in posts
    context = {
        'item': item,
        'post': post,
        'related': related,
    }
    return render(request, "product-page.html", context)

class CheckoutView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            order = Order.objects.get(user=request.user, ordered=False)
            form = CheckoutForm()
            context = {
                "form": form,
                "object": order,
            }
            return render(self.request, 'checkout-page.html', context)
        else:
            return redirect("users:login")
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                address = form.cleaned_data.get('address')
                address2 = form.cleaned_data.get('address2')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                # payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                user = self.request.user,
                address = address,
                address2 = address2,
                country = country,
                zip = zip,
                )
                billing_address.save()
                order.billing_address=billing_address
                order.save()
                return redirect("store:home")
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any order !")
            return redirect("store:home")

        # return redirect("store:checkout")
        
def payment_view(request):
    order = Order.objects.get(user=request.user, ordered=False)
    
    context = {
        "order": order
    }

    return render(request, "payment.html", context)


class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered = False)
            context = {
                'object': order,
            }
            return render(self.request, "order.html", context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any order !")
            return redirect("store:home")

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item quantity updated successfully!")
        else:
            order.items.add(order_item)
            messages.info(request, "Item added to your cart successfully!")
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)
        messages.info(request, "Item added to your cart successfully!")
    return redirect("store:order")


@login_required
def remove_from_cart(request, pk):

    item = get_object_or_404(Item, pk=pk)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]

            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "this item was removed form the cart!")
        else:
            messages.info(request, "no order item")
            return redirect("store:order")
    else:
        messages.info(request, "no order item")
        return redirect("store:order ")
    return redirect("store:order")

@login_required
def remove_one_item_from_cart(request, pk):

    item = get_object_or_404(Item, pk=pk)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False,
            )[0]

            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

            else:
                order.items.remove(order_item)
                order.save()
        else:
            return redirect("store:order")
    else:
        return redirect("store:order")
            
    messages.info(request, "Item quantity updated successfully !")
    return redirect("store:order")


def search_item(request):
    
    query = request.GET.get("q")
    qs = Item.objects.search(query=query)
    context = {
        "qs": qs
    }

    return render(request, 'search.html', context)
