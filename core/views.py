
from traceback import print_tb
import razorpay
from multiprocessing import context
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import CartItem, GameAccounts, ListedGames, CartOrder, PostImage
from .filters import PostFilter
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from .forms import GameAccountForm, ImageForm


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
class HomeView(View):
    def get(self, request, *args, **kwargs): 

        if request.user.is_authenticated:
            order_confirm = CartItem.objects.filter(user=request.user, ordered=False, payment_done=True)
            context = {
                'order_confirm':order_confirm
                
            }
        context = {
            'games':ListedGames.objects.all(),
             
        }    
        return render(request, 'core/home.html', context)

class GameView(View):
    def get(self, request, slug, *args, **kwargs):

        game = get_object_or_404(ListedGames, slug=slug)
        game_account = GameAccounts.objects.filter(game=game.id, ordered=False) 
        my_filter = PostFilter(request.GET, queryset=game_account)
        game_account = my_filter.qs
        
        try:
            cart_order = CartOrder.objects.get(
                user=request.user,
            )
            context = {
                'game':game,
                'game_account':game_account,
                'cart_accounts':cart_order,
                'my_filter':my_filter,
            } 
        except:
            cart_order = 0
            context = {
                'game':game,
                'game_account':game_account,
                'cart_accounts':cart_order,
            }    

        #my_list = []
        #for acc in cart_order.game_accounts.values():
        #    my_list.append(acc['game_account_id'])  
         
        return render(request, 'core/game.html', context)

class CartView(View):
    def get(self, request, *args, **kwargs):
        try:
            
            context = {
                'object': CartOrder.objects.get(user=self.request.user)
            }
            return render(request, 'core/cart.html', context)    
        except ObjectDoesNotExist:
            return redirect("/")   

def add_to_cart(request):
    if request.method == 'POST':
        acc_id = request.POST.get('acc_id')
        print('Hello')
        game_account = GameAccounts.objects.get(id=acc_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            game_account=game_account,
            #ordered=False,
            #payment_done=False
        )
    
        cart_order, created = CartOrder.objects.get_or_create(
            user=request.user
        )
        if cart_order.game_accounts.filter(game_account__id=game_account.id).exists():
            print('item already added to cart') 
            cart_order.game_accounts.remove(cart_item)
            cart_item.delete()
            resp = 'removed'
        else:
            cart_order.game_accounts.add(cart_item)
            resp = 'added'  
            print('item added to cart') 
        data = {
            'resp':cart_order.game_accounts.all().count()
        } 
        return JsonResponse(data, safe=False)
      
    return redirect('core:cart')    
             
           


def remove_from_cart(request):
    if request.method == 'GET':
        acc_id = request.GET.get('acc_id')
        game_account = GameAccounts.objects.get(id=acc_id)
        cart_item = CartItem.objects.get(
            user=request.user,
            game_account=game_account,
        )
    
        cart_order = CartOrder.objects.get(
            user=request.user
        )
        if cart_order.game_accounts.filter(game_account__id=game_account.id).exists():
            cart_order.game_accounts.remove(cart_item)  
            cart_item.delete()
            resp = 'removed'
            data = {
            'resp':cart_order.game_accounts.all().count()
            } 
            return JsonResponse(data, safe=False)
        else:
            print('item not in cart')
            return redirect('core:game', slug=game_account.game.slug)

class CheckoutView(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            game_account = GameAccounts.objects.get(pk=pk)

            currency = 'INR'
            amount = game_account.rate*100  # Rs. 200
 
            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = "paymenthandler/"
 
            # we need to pass these details to frontend.
            context = {}
            context['game_account'] = game_account
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url

            return render(request, "core/checkout.html", context)    
        except ObjectDoesNotExist:
            return redirect("core:home") 

class Me(View):
    def get(self, request, *args, **kwargs):

        context = {

        }
        return render(request, 'core/me.html', context)             

@csrf_exempt
def paymenthandler(request, pk):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            game_acc = GameAccounts.objects.get(pk=pk)
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            print(result)
            if result is not None:
                amount = game_acc.rate*100  # Rs. 200
                print(amount)

                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    print("Fucker")

                    cart_item = CartItem.objects.get(user=request.user, game_account=game_acc)
                    print(cart_item)
                    cart_item.payment_done=True
                    cart_item.save()

                    cart_item2 = CartItem.objects.filter(game_account=game_acc)
                    cart_item2.update(payment_done = True)
                    for item in cart_item2:
                        item.save()

                    game_acc.payment_done=True
                    game_acc.save()
 
                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:
 
                    # if there is an error while capturing payment.
                    print('1st failed')
                    return render(request, 'paymentfailed.html')
            else:
 
                # if signature verification fails.
                print('2nd failed')
                return render(request, 'paymentfailed.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest() 

def order_complete_confirm(request, pk):
    cart = CartOrder.objects.get(user=request.user)
    cart_item = CartItem.objects.get(pk=pk, user=request.user)
    game_acc = GameAccounts.objects.get(pk=cart_item.game_account.pk)

    cart.game_accounts.remove(cart_item)
    cart_item2 = CartItem.objects.filter(game_account=game_acc)
    cart_item2.update(ordered = True)
    for item in cart_item2:
        item.save()

    game_acc.ordered = True
    game_acc.save()
    return redirect('core:home')
    
                             

def cart_count(request):
    qs = CartOrder.objects.get(user=request.user)
    if qs:
        count =  qs.game_accounts.count()

    data={
        'count':count
    }
    return JsonResponse(data, safe=False)


class SellGameAcc(View):
    def get(self, request, *args, **kwargs):
        game_acc_form = GameAccountForm()
        image_form = ImageForm()

        context = {
            'game_acc_form':game_acc_form,
            'image_form':image_form

        }
        return render(request, 'core/sell.html', context)
    def post(self, request, *args, **kwargs):
        game_acc_form = GameAccountForm(request.POST)
        image_form = request.FILES.getlist('image')


        if game_acc_form.is_valid() and image_form is not None:
            form1 = game_acc_form.save(commit=False)
            form1.acc_owner = request.user
            form1.save() 
            for img in image_form:
                form2 = PostImage.objects.create(
                    game_account = GameAccounts.objects.get(id=form1.id),
                    images = img
                )
            return redirect('core:home')
   
        context = {
            'game_acc_form':game_acc_form,
            'image_form':image_form,

        }
        return render(request, 'core/sell.html', context)



       
        





        
    