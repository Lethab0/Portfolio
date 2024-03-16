from django.shortcuts import render, redirect
from django.http import HttpResponse , JsonResponse
import math , random
import json
import random


    #data = ['love', 'hate']
    #return render(request, 'index.html', {'initial_data': data})
asset1 = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
asset2 = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
asset3= [400, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]

def index(request):
    for i in range(len(asset1)-1):
        asset1[i] = asset1[i+1]
    asset1[-1] = random.randrange(500,2500)
    love = 1
    test = json.dumps(love)
    return render(request, 'js.html', {"asset1":asset1, "test":test})
    
def Jason(request):
    for i in range(len(asset1)-1):
        asset1[i] = asset1[i+1]
    asset1[-1] = random.randrange(500,2500)
    love = 1
    test = json.dumps(love)
    return JsonResponse({"asset1": asset1, "asset2": asset2, "asset3": asset3})









#https://pypi.org/project/websocket_client/
#import websocket



#def on_message(ws, message):
#    print(message)

#def on_error(ws, error):
#    print(error)

#def on_close(ws):
#    print("### closed ###")

#def on_open(ws):
#    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')


#if __name__ == "__main__":
#    websocket.enableTrace(True)
#    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=cmvtd2hr01qkcvkf94mgcmvtd2hr01qkcvkf94n0",
#                              on_message = on_message,
#                              on_error = on_error,
#                              on_close = on_close)
#    ws.on_open = on_open
#    ws.run_forever()






#test_data = [random.randint(1, 100) for _ in range(10)]
    #data = json.dumps(test_data)



"""'[
                           [
                             {"meta":"6/01/2019 9:00 PM","value":"1200"},
                             {"meta":"6/02/2019 9:00 PM","value":"800"},
                             {"meta":"6/03/2019 9:00 PM","value":"900"},
                             {"meta":"6/04/2019 9:00 PM","value":"1600"},
                             {"meta":"6/05/2019 9:00 PM","value":"1700"},
                             {"meta":"6/06/2019 9:00 PM","value":"1400"},
                             {"meta":"6/07/2019 9:00 PM","value":"1500"},
                             {"meta":"6/08/2019 9:00 PM","value":"1350"},
                             {"meta":"6/09/2019 9:00 PM","value":"1200"},
                             {"meta":"6/10/2019 9:00 PM","value":"1100"},
                             {"meta":"6/11/2019 9:00 PM","value":"700"},
                             {"meta":"6/12/2019 9:00 PM","value":"800"},
                             {"meta":"6/13/2019 9:00 PM","value":"2100"},
                             {"meta":"6/14/2019 9:00 PM","value":"1900"},
                             {"meta":"6/15/2019 9:00 PM","value":"1800"},
                             {"meta":"6/16/2019 9:00 PM","value":"2100"},
                             {"meta":"6/17/2019 9:00 PM","value":"1800"},
                             {"meta":"6/18/2019 9:00 PM","value":"1600"},
                             {"meta":"6/19/2019 9:00 PM","value":"1200"},
                             {"meta":"6/20/2019 9:00 PM","value":"1400"},
                             {"meta":"6/21/2019 9:00 PM","value":"1500"},
                             {"meta":"6/22/2019 9:00 PM","value":"1700"},
                             {"meta":"6/23/2019 9:00 PM","value":"1600"},
                             {"meta":"6/24/2019 9:00 PM","value":"1800"},
                             {"meta":"6/25/2019 9:00 PM","value":"1850"},
                             {"meta":"6/26/2019 9:00 PM","value":"1900"},
                             {"meta":"6/27/2019 9:00 PM","value":"1950"},
                             {"meta":"6/28/2019 9:00 PM","value":"2100"},
                             {"meta":"6/29/2019 9:00 PM","value":"2200"},
                             {"meta":"6/30/2019 9:00 PM","value":"2300"}
                           ]
                         ]'  """