import requests
from tabulate import tabulate

url = "https://api.swapzone.io/v1/exchange/currencies"

headers = {
	'x-api-key': 'Gs7JK8J5x'
}

response = requests.request("GET", url, headers=headers).json()[0:30]
print(tabulate(response, headers))
    


