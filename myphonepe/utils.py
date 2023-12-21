import uuid  
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest

unique_transaction_id = str(uuid.uuid4())[:-2]
s2s_callback_url = "https://www.merchant.com/callback"  
amount = 100  
id_assigned_to_user_by_merchant = 'YOUR_USER_ID'  
pay_page_request = PgPayRequest.pay_page_pay_request_builder(merchant_transaction_id=unique_transaction_id,  
                                                             amount=amount,  
                                                             merchant_user_id=id_assigned_to_user_by_merchant,  
                                                             callback_url=s2s_callback_url)  
pay_page_response = phonepe_client.pay(pay_page_request)  
pay_page_url = pay_page_response.data.instrument_response.redirect_info.url
