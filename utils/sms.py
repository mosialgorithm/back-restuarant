# from melipayamak import Api

# def send_sms():
#     username = '09355739363'
#     password = 'PBAGM'
#     api = Api(username,password)
#     sms = api.sms()
#     # to = '09123456789'
#     to = '09133751410'
#     _from = ''
#     # text = 'تست وب سرویس ملی پیامک'
#     text = 'MosiWeb.ir'
#     # text = text
#     response = sms.send_by_base_number(to,_from,text)
#     print(response)
    
    
    
# import requests

# def send_sms(to, code):
#     data = {
#     'username': "09355739363",
#     # 'password': "PBAGM",
#     'password': "328bea4e-c255-4ff3-bf73-7c6850ee9b5e",
#     # 'to': "09121111111,09120000000",
#     'to': to,
#     # 'text': "تست",
#     # 'text': f'MosiWeb.ir</br>code: {code}',
#     'text': f'Mosiweb.ir</br>Code: {code}',
#     'from': "", 
#     'fromSupportOne': "", 
#     'fromSupportTwo': ""
#     }

#     url = 'https://rest.payamak-panel.com/api/SmartSMS/Send'

#     headers = {'content-type': 'application/x-www-form-urlencoded'}

#     requests.packages.urllib3.disable_warnings()
#     session = requests.Session()
#     session.verify = False
#     response = session.post(url, data=data, headers=headers)
#     print(response.text)



# ==================================== SMS.ir ========================================================
from sms_ir import SmsIr
sms_ir = SmsIr('dt7dYKQBHIaAKSwfUXwVArIZ3oZLjOBCivWaEPRSu8fEGHjC',30002108005279,)

# sms_ir.send_sms(number,message,linenumber,)
# sms_ir.send_sms('09133751410','hello mosii',30002108005279,)