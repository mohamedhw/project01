from django.urls import path
# from .api import *
from .views import (
    Home,
    detail_view,
    add_to_cart, 
    CheckoutView, 
    remove_from_cart, 
    ShirtView, 
    SportsView, 
    OutWearView,
    search_item,
    OrderView,
    remove_one_item_from_cart,
    payment_view,
    stripe_config,
    create_checkout_session,
    payment_success,
    payment_cancel,
    save_button,
    saved_posts,
    SaleView,
    NewView,
)


app_name="store"

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('<int:pk>/', detail_view, name="detail"),
    path('<int:pk>/add_to_cart/', add_to_cart, name='add_to_cart'),
    path('<int:pk>/rm-item/', remove_from_cart, name="remove_item"),
    path('shirt/', ShirtView.as_view(), name='shirt'),
    path('sport/', SportsView.as_view(), name='sport'),
    path('outwear/', OutWearView.as_view(), name='outwear'),
    path('sale/', SaleView.as_view(), name='sale'),
    path('new/', NewView.as_view(), name='new'),
    path('search/', search_item, name="search"),
    path('order/', OrderView.as_view(), name="order"),
    path('<int:pk>/remove-one', remove_one_item_from_cart, name="remove_one_item"),
    path('cart/', CheckoutView.as_view(), name='checkout'),
    path('wish/<int:pk>/', save_button, name='save' ),
    path('wishl/', saved_posts, name='wishlist'),
    #stripe
    path('config/', stripe_config),
    path('create-checkout-session/', create_checkout_session), # new
    path('success/', payment_success),
    path('cancel/', payment_cancel),

    # api urls
#    path('<int:pk>/item-detail-api/', item_detail_api, name="item_detail_api"),
#    path("item-list-api/", ApiItemList.as_view(), name="item_list_api")
]