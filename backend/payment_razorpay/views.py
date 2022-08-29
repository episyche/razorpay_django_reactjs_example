from unicodedata import name
from django.shortcuts import render
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


razorpay_client = razorpay.Client(auth=("*** Key Id *****", "***** Key Secret *****"))

@csrf_exempt
def new_order(request):
    if request.method == "POST":

        print("", request.POST['price'])
        amount = int(request.POST['price'])
        product_name = request.POST['product_name']

        new_order_response = razorpay_client.order.create({
                        "amount": amount*100,
                        "currency": "INR",
                        "payment_capture": "1"
                      })

        response_data = {
                "callback_url": "http://127.0.0.1:8000/payment/callback",
                "razorpay_key": "****** Key Id *******",
                "order": new_order_response,
                "product_name": product_name
        }

        print(response_data)

        return JsonResponse(response_data)


@csrf_exempt
def order_callback(request):
    if request.method == "POST":
        if "razorpay_signature" in request.POST:
            payment_verification = razorpay_client.utility.verify_payment_signature(request.POST)
            if payment_verification:
                return JsonResponse({"res":"success"})
                # Logic to perform is payment is successful
            else:
                return JsonResponse({"res":"failed"})
                # Logic to perform is payment is unsuccessful

