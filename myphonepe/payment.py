from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializer import *
import requests
from .models import *
import hashlib
import base64
import string
import random
import json
import uuid

def phonepegatewayr(request,amount):
    global merchantTransactionId
    global salt_key
    global merchant_id
    global baseurl
    baseurl = "https://api-preprod.phonepe.com/apis/pg-sandbox"

    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    merchant_user_id = "MUID123"
    mobileNumber = "7071845054"
    # merchanttransactionid = []
    salt_index = 1 

    try:
        merchant = merchant_id
        key = salt_key
        
        if merchant:
            print(merchant)
            if request.method == "POST":
                merchantTransactionId = str(uuid.uuid4())
                status = "Success"
                print("merchant tran id", merchantTransactionId)
                mtid = Payment_status_ID.objects.create(m_tid = merchantTransactionId, payment_status=status)
              
                mtid.save()
                serialize_mtid = PaymentStatusSerializer()
                print("Merchant Transaction ID Created", serialize_mtid)
            

            # mtid = merchantTransactionId.append[merchanttransactionid]

            baseurl = "https://api-preprod.phonepe.com/apis/pg-sandbox"
            data = {
                "merchantId": merchant_id,
                "merchantTransactionId": merchantTransactionId,
                "merchantUserId": merchant_user_id,
                "amount": amount * 100,
                "redirectUrl": baseurl+ "/pg/v1/status/" + merchant_id + "/" + merchantTransactionId,
                "redirectMode": "POST",
                "callbackUrl":  baseurl+ "/pg/v1/status/" + merchant_id + "/"+ merchantTransactionId,
                "mobileNumber": mobileNumber,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
            }

            print("data")
            print(data)

            payload_main = base64.b64encode(json.dumps(data).encode()).decode()
            print("payload")
            print(payload_main)

            payload = payload_main + "/pg/v1/pay" + key
            checksum = hashlib.sha256(payload.encode()).hexdigest()
            checksum = checksum + '###1'
            print("checksum")
            print(checksum)

            header = {
                "Content-Type": "application/json",
                "X-VERIFY": str(checksum),
                "accept": "application/json"
            }

            url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"
            payload_data = {
                "request": payload_main
            }
            datas=json.dumps(payload_data)
            print("datas")
            print(datas)
            # response = requests.post(url, data=json.dumps(payload_data), headers=header)
            response = requests.request("POST", url, data=datas, headers=header)

            print(response.text,response.status_code)
            if response.status_code == 200:
                response_data = response.json()
                print("res_data", response_data)
                # check_status()
                print("responce")
                print(response)
                # decode = json.loads(response_data.decode('utf-8'))
                # print("decode", decode)
                url = response_data['data']['instrumentResponse']['redirectInfo']['url']
                # if url['data'] == 'success':
           
                print(url)
                return HttpResponse(url)
                # return HttpResponse(f"Redirecting to PhonePe: <a href='{url}'>{url}</a>")
            else:
               
                return HttpResponse(f"HTTP Error: {response.status_code}<br>{response.text}", status=500)
        else:
            return HttpResponse("Payment secret not found", status=500)
    except Exception as e:

        return HttpResponse(f"Error: {str(e)}", status=500)
    

def statuscheck(request,merchantTransactionId):
    merchant_t_id = merchantTransactionId
    # merchant =merchant_id
    baseurl = "https://api-preprod.phonepe.com/apis/pg-sandbox"
    mer = Payment_status_ID.objects.first()
    # key = salt_key
    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    merchant_user_id = "MUID123"
    mobileNumber = "7071845054"

    s_payload_main = base64.b64encode(json.dumps(merchantTransactionId).encode()).decode()
    print("payload")
    print(s_payload_main)

    s_payload = f"{baseurl} + /pg/v1/pay/ + {merchant_id}/ + {merchantTransactionId} + {salt_key}"
    checksum = hashlib.sha256(s_payload.encode()).hexdigest()
    s_checksum = checksum + '###1'
    print("s checksum")
    print(s_checksum)

    if request.method == "GET":
        s_url = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{merchant_t_id}"

        headers = {
                "Content-Type": "application/json",
                "X-VERIFY": str(checksum),
                "X-MERCHANT-ID":merchant_id,
                "accept": "application/json"
            }
    
        s_datas=json.dumps(s_payload_main)
        print("sss datas")
        print(s_datas)
        response = requests.post(s_url, json=s_payload_main, headers=headers)
        print(response.text,response.status_code)
        res = response.json(request)
        print(res)
        # if response.data['success'] == true:

def check_status(request):
    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    merchant_user_id = "MUID123"
    mobileNumber = "7071845054"


    try:
        merchant = merchant_id
        key = salt_key
        if merchant:
            print(merchant)
            mer_id = Payment_status_ID.objects.all("m_tid")
            if mer_id == "m_tid" :
                print(mer_id)

            # if mer_id == phonepegatewayr(data['"merchantTransactionId'])

            
            # merid = phonepegatewayr(request, merchantTransactionId)

            success_data = {
                "success": True,
                "code": "PAYMENT_SUCCESS",
                "message": "Your request has been successfully completed.",
                "data": {
                    "merchantId": merchant_id,
                    "merchantTransactionId": mer_id,
                    "transactionId": "T2111221437456190170379",
                    "amount": phonepegatewayr(request),
                    "state": "COMPLETED",
                    "responseCode": "SUCCESS",
                    "paymentInstrument": {
                    "type": "UPI",
                    "utr": "206378866112"
                    }
                }
            }
            print("succss ddata")
            print(success_data)
            

            payload_main = base64.b64encode(json.dumps(success_data).encode()).decode()
            print("payload")
            print(payload_main)

            payload = payload_main + "/pg/v1/pay" + key
            checksum = hashlib.sha256(payload.encode()).hexdigest()
            checksum = checksum + '###1'
            print("checksum")
            print(checksum)
            print("again checksum")

            header = {
                "Content-Type": "application/json",
                "X-VERIFY": str(checksum),
                "accept": "application/json"
            }

            url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{merchantTransactionId}"

            payload_data = {
                "request": payload_main
            }

            datas=json.dumps(payload_data)
            print("status datas")
            print(datas)
            response = requests.request("POST", url, data=datas, headers=header)

            print(response.text,response.status_code)
            if response.status_code == 200:
                respo = json.loads(request.body.decode('utf-8'))
                response_data = response.json(respo)
                response_data = json.loads(request.body.decode('utf-8'))
                if response_data["code"] == "PAYMENT_SUCCESS":
                    res = response_data["data"]
                    for dt in res:
                        if dt["responseCode"] == "responseCode" & dt["state"] == "COMPLETED":
                            print ("Your Payment Has been Completed")

                        else:
                            return HttpResponse("payment failed")
                            
                    
                print("responce")
                print(response)
                url = response_data['data']['instrumentResponse']['redirectInfo']['url']
           
                print(url)
                return HttpResponse("Success payment")
    except Exception as e:

        return HttpResponse(f"Error: {str(e)}", status=500)



def check_status(request,amount):
    print('check status function')
    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    merchant_user_id = "MUID123"
    mobileNumber = "7071845054"

    try:
        # Assuming Payment_status_ID has a field named 'm_tid'
        # mer_id = Payment_status_ID.objects.values_list("m_tid", flat=True).first()
        
        if merchant_id:
            print(merchant_id)
            merchantTransactionId = str(uuid.uuid4())
            print(merchantTransactionId)
            merchant_transac_id = merchantTransactionId

        success_data = {
            "success": True,
            "code": "PAYMENT_SUCCESS",
            "message": "Your request has been successfully completed.",
            "data": {
                "merchantId": merchant_id,
                "merchantTransactionId": merchantTransactionId,
                "transactionId": "T2111221437456190170379",
                "amount": amount*100,  # You need to define phonepegatewayr function
                "state": "COMPLETED",
                "responseCode": "SUCCESS",
                "paymentInstrument": {
                    "type": "UPI",
                    "utr": "206378866112"
                }
            }
        }
        print("data")
        print(success_data)

        payload_main = base64.b64encode(json.dumps(success_data).encode()).decode()
        print("payload")
        print(payload_main)

        payload = payload_main + "/pg/v1/status/" + merchant_id + '/' + merchant_transac_id + '/' + salt_key
        checksum = hashlib.sha256(payload.encode()).hexdigest()
        checksum = checksum + '###1'
        print("checksum")
        print(checksum)

        header = {
            "Content-Type": "application/json",
            "X-VERIFY": str(checksum),
            "accept": "application/json"
        }

        url = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{merchant_transac_id}"
        
        payload_data = {
            "request": payload_main
        }

        datas = json.dumps(payload_data)
        print("status datas")
        print(datas)
        response = requests.request("POST", url, data=datas, headers=header)

        print(response.text, response.status_code)
        if response.status_code == 200:
            response_data = response.json()
            red = response_data.loads(request.body.decode('utf-8'))
            if response_data["code"] == "PAYMENT_SUCCESS":
                res = response_data["data"]
                for dt in res:
                    if dt["responseCode"] == "responseCode" and dt["state"] == "COMPLETED":
                        print("Your Payment Has been Completed")
                        if response.status_code == 400:
                            print("done")
                        else:
                            return HttpResponse("Payment failed")
                
                print("response")
                print(response)
                url = response_data['data']['instrumentResponse']['redirectInfo']['url']
                print(url)
                return HttpResponse("Success payment")
        # return HttpResponse("failed")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    




def check_payment_status(request):
    print('Check payment status function')
    global mfg
    merchant_id = "PGTESTPAYUAT"
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    merchant_user_id = "MUID123"
    mobile_number = "7071845054"
    amount = ""

    try:
        if merchant_id:
            print(merchant_id)
            # mer_tid = Payment_status_ID.objects.first()
            # mfg = mer_tid
            # print("hgvjshgfjhsdjsdhfjsdhgfjhsdgfj")
            # print(mer_tid.m_tid)
            # mfg = ""
            # for mtd in mer_tid:
            #     mfg = mtd.m_tid

            # print("merchant id ", mfg)
            
            payment_status_instance = Payment_status_ID.objects.first()  # Replace 'pk' with the actual primary key or use other filters
            # You can replace 'pk=1' with appropriate filtering based on your model structure

            # Assuming you have a serializer to serialize the data
            # Replace 'YourModelSerializer' with the actual serializer for Payment_status_ID
            serializer = PaymentStatusSerializer(payment_status_instance)
         

            # merchant_transaction_id = str(uuid.uuid4())
            print(serializer)
            # print(merchant_transaction_id)

            # Assuming you have a function named 'phonepegatewayr' to get the amount
            amount = phonepegatewayr(request,amount)

            success_data = {
                "success": True,
                "code": "PAYMENT_SUCCESS",
                "message": "Your request has been successfully completed.",
                "data": {
                    "merchantId": merchant_id,
                    "merchantTransactionId": serializer,
                    "transactionId": "T2206202020325589144911",
                    "amount": amount,
                    "state": "COMPLETED",
                    "responseCode": "SUCCESS",
                    "paymentInstrument": {
                    "type": "NETBANKING",
                    "pgTransactionId": "1856982900",
                    "pgServiceTransactionId": "PG2207281811271263274380",
                    "bankTransactionId": None,
                    "bankId": "SBIN"
                    }
                }
                }

            print("data")
            print(success_data)

            payload_main = base64.b64encode(json.dumps(success_data).encode()).decode()
            print("payload")
            print(payload_main)

            payload = payload_main + "/pg/v1/pay" + merchant_id + serializer 
            checksum = hashlib.sha256(payload.encode()).hexdigest()
            checksum = checksum + '###'
            print("checksum")
            print(checksum)

            header = {
                "Content-Type": "application/json",
                "X-VERIFY": str(checksum),
                "accept": "application/json"
            }

            url = f"https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchant_id}/{serializer}"
            print("url status ")
            print(url)

            payload_data = {
                "request": payload_main
            }

            datas = json.dumps(payload_data)
            print("status datas")
            # print(datas)
            # url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchantId}/{merchantTransactionId}"
        
        
            headers = {
                "accept": "text/plain",
                "Content-Type" : "application/json" 
            }
            
            response = requests.post(url, json=success_data, headers=headers)
            
            print(response.text)

            # response = requests.request("GET", url, data=datas, headers=header)
            print("respinse all data ")
            print(response)


            print(response.text, response.status_code)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data["code"] == "PAYMENT_SUCCESS":
                    res = response_data["data"]
                    for dt in res:
                        if dt["responseCode"] == "SUCCESS" and dt["state"] == "COMPLETED":
                            print("Your Payment Has been Completed")
                            return HttpResponse("Success payment")
                    print("Payment failed")
                    return HttpResponse("Payment failed")

            print("Response code is not 200")
            return HttpResponse("Failed")

        print("Merchant ID is not provided")
        return HttpResponse("Failed")

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def checkpaystatus(request):
        url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/MT7850590068188104"
        success_data = {
                "success": True,
                "code": "PAYMENT_SUCCESS",
                "message": "Your request has been successfully completed.",
                "data": {
                    "merchantId": "PGTESTPAYUAT",
                    "merchantTransactionId": "MT7850590068188104",
                    "transactionId": "T2111221437456190170379",
                    "amount": 77664,
                    "state": "COMPLETED",
                    "responseCode": "SUCCESS",
                    "paymentInstrument": {
                        "type": "UPI",
                        "utr": "206378866112"
                    }
                }
         }
        
        headers = {
            "accept": "text/plain",         
            "Content-Type" : "application/json" 
        }
        
        response = requests.post(url, json=success_data, headers=headers)
        print(response)
        print(response.json())
        return HttpResponse(response.json())