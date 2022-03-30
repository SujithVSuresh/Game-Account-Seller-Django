from cgi import test
from django.urls import path
from .views import HomeView, GameView, add_to_cart, remove_from_cart, CartView, cart_count, CheckoutView, paymenthandler, order_complete_confirm, Me, SellGameAcc



app_name='core'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('game/<slug>/', GameView.as_view(), name='game'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart-count/', cart_count, name='cart-count'),
    path('remove-from-cart/', remove_from_cart, name='remove-from-cart'),
    path('payment/<int:pk>/', CheckoutView.as_view(), name='checkout'),
    path('payment/<int:pk>/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('order/<int:pk>/confirm/', order_complete_confirm, name='order_confirm'),
    path('me/', Me.as_view(), name='me'),
    path('sell/', SellGameAcc.as_view(), name='sell'),
]