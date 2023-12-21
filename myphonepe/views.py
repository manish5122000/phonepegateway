from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .payment import *
from .models import *
import hashlib
import base64
import string
import random
import json
import uuid
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
merchant_id = "YOUR_MERCHANT_ID"  
salt_key = "YOUR_SALT_KEY"  
salt_index = 1 
# env = Env.UAT # Change to Env.PROD when you go live

# phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)

# Create your views here.


def loginphone(request):
    next_url = request.GET.get('next', '')
    print(next_url)
    if request.method == 'POST':
        number = request.POST.get('phoneno')
        nexturl = request.POST.get('next')
        print(nexturl)
        print("post loginphone")
        print(number)
        profiledata = Profile.objects.filter(Phone_Number=number)
        print(profiledata)
        if(profiledata):
            for pro in profiledata:
                usernames = pro.user
                passw = pro.bio
            user = User.objects.filter(username=usernames)
            print(user)
            for users in user:
                ids = users.id
            if nexturl is not None:
                return redirect(f'/otps/{ids}/?next={nexturl}')
            return redirect('/otps/{}'.format(ids))
            
            new_user = authenticate(username=usernames, password=passw)
            if new_user:
                login(request, new_user)
                return redirect('home')
            else:
                return redirect('user_registration')
        else:
            passs = number+"Nakshtravani@"
            passs = str(passs)
            print(passs)
            user = User.objects.create(
                username=number
                # role='User',
                # password=passs,
            )
            v = user.set_password(passs)
            print(v)
            user.save()
            user = User.objects.get(username=number)
            # user.is_active = False
            user.passwo = passs

            createProfile = Profile.objects.create(user=user,Phone_Number=number,Role='User',bio=passs)
            user.save()
            # print(createProfile)
            # print(user.id)
            # print(user)
            # print("ghgjjhhgghgf")
            return redirect('/otps/{}'.format(user.id))
    if next_url is not None:
        return render(request,'loginphone.html',{"next":next_url})
    else:
        return render(request,'loginphone.html')
    
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            phone_no = request.POST.get('phone')
            name = request.POST.get('first_name')
            print(name)
            
            form.instance.username = name+f'{random.randrange(10000000)}'
            print(phone_no)
            usernames = form.instance.username
            password = form.cleaned_data['password1']
            print(form.instance.username)
            print(form.cleaned_data['password1'])
            # login(request, user)
            form.save()
            user = form.save()
            user.is_active = False
            check_profile = Profile.objects.filter(Phone_Number=phone_no).first()
            if(check_profile):
                print("yes")
                print(check_profile)
            otp = str(random.randint(1000 , 9999))
            print(otp)
            # userd = request.User
            createProfile = Profile.objects.create(user=user,Phone_Number=phone_no,Role='User',code=otp,bio=password)
            print(createProfile)

            print(user.id)
            context={'useer': usernames}
      
            return redirect('/otps/{}'.format(user.id))
          

    
def otpValidates(request, useer):
    pro = User.objects.get(id=useer)
    next_url = request.GET.get('next', '')
    print(next_url)
    print("otp validate")

    print(pro.username)
    
    # You can simplify this query using get() if you expect only one profile per user
    profileData = Profile.objects.filter(user=pro)
    for i in profileData:
        # print("hhhhhh")
        passw = i.bio
        valid = i.code
        no = i.Phone_Number
        print(i.code)
    # passw = profileData.bio
    # valid = profileData.code
    # no = profileData.Phone_Number
    no = "+91"+no
    print(no)

    # print(profileData.code)
    account_sid = settings.ACCOUNT_SID
    auth_token =  settings.AUTH_TOKEN
    verify_sid = settings.VARIFY_SID
    SecurityToken = Security.objects.all()
    for token in SecurityToken:
        account_sid = token.ACCOUNT_SID
        auth_token = token.AUTH_TOKEN
        verify_sid = token.VARIFY_SID
    verified_number =no
    # Initialize client outside of the if statements
    client = Client(account_sid, auth_token)
    print(client)
    if request.method == 'GET':
        print('in get')
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
        if next_url is not None:
            return render(request, 'otp.html', {'username': useer,'next':next_url})

        return render(request, 'otp.html', {'username': useer})

    if request.method == 'POST':
        name = request.POST.get('otp')
        next_url = request.POST.get('next')
        print(next_url)
        print(name)
        print(type(name))
        
        try:
            verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=no, code=name )
            print(verification_check.status)
            if verification_check.status == 'approved':
                print("valid otp")
                pro.is_active = True
                new_user = authenticate(username=pro.username, password=passw)

                if new_user:
                    login(request, new_user)
                    if next_url:
                        return redirect(next_url)
                    return redirect('home')
                else:
                    return redirect('user_registration')
            else:
                return redirect('user_registration')
        except TwilioRestException as e:
            # Handle Twilio API exception
            print(f"Twilio Error: {e}")
            return redirect('user_registration')
   
        
        

def index(request):

    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    salt_index = 1 

    url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"

    headers = {
        "accept": "text/plain",
        
        'Content-Type' : "application/json" 
    }

    json_data = {
        "merchantId": merchant_id,
        "merchantTransactionId": "MT7850590068188104",
        "merchantUserId": "MUID123",
        "amount": 10000,
        "redirectUrl": "https://webhook.site/redirect-url",
        "redirectMode": "REDIRECT",
        "callbackUrl": "https://webhook.site/callback-url",
        "mobileNumber": "9999999999",
        "paymentInstrument": {
            "type": "PAY_PAGE"
        }
    }
    
    response = requests.post(url, json=json_data, headers=headers)
    
    print(response.text)

    return render(request, 'home.html')



def phonepegateway(request,amount):
    merchant_id = "PGTESTPAYUAT"  
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"  
    merchant_user_id = "MUID123"
    mobileNumber = "7071845054"
    Amount = amount
    salt_index = 1 

    try:
        # payment_secret = PaymentSecret.objects.first()  
        # payment_secret = True
        # merchant = payment_secret.merchantid
        merchant = merchant_id
        key = salt_key
        if merchant:
            print(merchant)
            merchantTransactionId = str(uuid.uuid4())
            print("merchant tran id", merchantTransactionId)
            # userss = request.user
            # prof = Profile.objects.get(user=userss)
            # if(prof and prof.Phone_Number):
            #     userId = prof.Phone_Number
            # else:
            #     userId = userss
            # print(prof.Phone_Number)
            baseurl = "https://api-preprod.phonepe.com/apis/pg-sandbox"
            data = {
                "merchantId": merchant_id,
                "merchantTransactionId": merchantTransactionId,
                "merchantUserId": merchant_user_id,
                "amount": Amount * 100,
                "redirectUrl": baseurl+"paymentsuccess/",
                "redirectMode": "POST",
                "callbackUrl": baseurl+"paymentsuccess/",
                "mobileNumber": mobileNumber,
                "paymentInstrument": {
                    "type": "PAY_PAGE"
                }
            }

            print("data")
            print(data)
            # Convert the payload to JSON and encode as Base64
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
                print("responce")
                print(response)
                url = response_data['data']['instrumentResponse']['redirectInfo']['url']
                # Redirect to the obtained URL
                print(url)
      
                
                return redirect(url,permanent=True)

                # return HttpResponse(f"Redirecting to PhonePe: <a href='{url}'>{url}</a>")
            else:
                # Handle the error here
                return HttpResponse(f"HTTP Error: {response.status_code}<br>{response.text}", status=500)
        else:
            return HttpResponse("Payment secret not found", status=500)
    except Exception as e:
        # Handle other exceptions
        return HttpResponse(f"Error: {str(e)}", status=500)



class PhonePayView(APIView):
    def post(self,request):
        print(request)
        data = json.loads(request.body.decode('utf-8'))
        amount = data['amount']
        res = phonepegatewayr(request,amount)
        print('amount')
        print(res)
        print("Request Body:", data)
        print(res)
        return res
    def get(self,request):
        pass

class callback_status(APIView):
    def post(self,request):
        print(request)
    def get(self,request):
        pass



class PhonePayCheckStatusView(APIView):
    print("manish maurya")
    def post(self, request):
        print("kjhfkdf")
        try:
            data = json.loads(request.body.decode('utf-8'))
            amount = data['amount']
            res = statuscheck(request,amount)
            print('amount')
            print(res)
            print("Request Body:", data)
            print(res)
            return HttpResponse(res)
        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Invalid JSON format in the request body"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # def post(self,request):
    #     print(request)
    #     data = json.loads(request.body.decode('utf-8'))
    #     amount = data['amount']
    #     res = check_payment_status(request)
    #     print('amount')
    #     print(res)
    #     print("Request Body:", data)
    #     print(res)
    #     return HttpResponse(res)
    def get(self,request):
        pass

# class check_status(APIView):
#     def post(self,request):
#         print(request)
#         datas = json.loads(request.body.decode('utf-8'))
#         merchant_id = phonepegatewayr(request,merchant_id)
#         merchanttransactionid = phonepegatewayr(request, merchanttransactionid)

#         url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/{merchantId}/{merchantTransactionId}"

        
#     def get(self,request):
#         pass