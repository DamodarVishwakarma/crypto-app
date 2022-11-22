from django.shortcuts import render
import requests
from tabulate import tabulate

def home(request):
    return render(request, 'home.html')
    

def currency(request):
    url = "https://api.swapzone.io/v1/exchange/currencies"
    headers = {
        'x-api-key': 'Gs7JK8J5x'
    }

    response = requests.request("GET", url, headers=headers).json()[0:30]
    
    return render(request, 'currency/currencies.html', context={'data':response})
    

   
