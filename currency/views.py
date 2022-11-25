from django.shortcuts import render, get_object_or_404
import requests
from currency.models import Wallet
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User

def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin or request.user.is_superuser:
            users = User.objects.filter(is_user=True)
            return render(request, 'accounts/user.html', context={'users':users})
    
    return render(request, 'home.html')
    

def currency(request):
    url = "https://mineable-coins.p.rapidapi.com/coins"

    headers = {
    "X-RapidAPI-Key": "b62ddcb981msh084da402605eb27p165870jsnef596d9bf856",
    "X-RapidAPI-Host": "mineable-coins.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers).json()[:20]
    return render(request, 'currency/currencies.html', context={'data':response})

def wallet(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    return render(request, 'currency/wallet.html', context={'wallet':wallet})



def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'payments/pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        amount = int(request.POST['amount'])
        user = authenticate(request, username=username, password=password)
        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'payments/pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'payments/redirect.html', context=paytm_params)



@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'payments/callback.html', context=received_data)
        return render(request, 'payments/callback.html', context=received_data)