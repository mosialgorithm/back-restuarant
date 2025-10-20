import requests
import random
import datetime
from flask import render_template, url_for, redirect, request, jsonify
from . import auth
from .schemas import user_register_schema, user_mobile_schema, user_login_schema, user_schema, user_login_sms_schema
from .models import UserModel
from flask_login import login_user, logout_user, current_user
from utils.sms import sms_ir



# ---------------------------------------------------------------------
# register methods
@auth.route('/register', methods=['POST', 'GET'])
def register_view():
    if request.method == 'POST':
        try:
            user_data = user_register_schema.load(request.get_json())
            new_user = UserModel()
            new_user.full_name = user_data['full_name']
            new_user.mobile = user_data['mobile']
            new_user.set_password(user_data['password'])
            new_user.save()
            return jsonify({
                'status': 'success',
                'message': 'user is created successfully',
                'data': ''
            })
        except Exception as ex:
            return jsonify({
                'status': 'error',
                'message': f'{ex}',
                'data': ''
            })
    
    return render_template('auth/register.html')



# end register method

# ---------------------------------------------------------------------
# login methods
@auth.route('/login', methods=['POST', 'GET'])
def login_view():
    if request.method == 'POST':            
        user_data = request.get_json()
        if user_data['mobile'] is None or user_data['password'] is None:
            return jsonify({
                'status': 'error',
                'message': 'mobile and password is not correct',
                'data': {}
            })
        user_data = user_login_schema.load(request.get_json())
        # print(user_data)
        user = UserModel.query.filter_by(mobile=user_data['mobile']).first()
        if user and user.check_password(user_data['password']):
            login_user(user)
            response = user_schema.dump(user)
            return jsonify({
                'status': 'success',
                'message': 'user is logged successfully',
                'data': response
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'user is not logged, please try again',
                'data': {}
            })
            
    return render_template('auth/login.html')


@auth.route('/send-sms', methods=['POST'])
def send_sms():
    if request.method == 'POST':
        user_data = request.get_json()
        mobile_number = user_data['mobile']
        if mobile_number is None or len(mobile_number) != 11 :
            return jsonify({
            'status': 'error',
            'message': 'mobile number is incorrect, please enter correct mobile number',
            'data': {}
            })
        # code = random.randint(0, 999999)
        # print(code)
        try:
            # data = {'bodyId': 364559, 'to': mobile_number, 'args': [code]}
            data = {'to': mobile_number}
            response = requests.post('https://console.melipayamak.com/api/send/otp/c2f1414c32fa4c8e861c46c5acf764c3', json=data)
            result = response.json()
            code = result['code']
        except Exception as ex:
            return jsonify({
                'status': 'error',
                'message': f'{ex}',
                'data': {}
            })
        user = UserModel.query.filter_by(mobile=mobile_number).first()
        if user and code is not None:
            expired_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
            user.mobile_code = code
            user.mobile_code_expired = expired_time
            user.update()
        else:
            new_user = UserModel()
            new_user.mobile = mobile_number
            new_user.mobile_code = code
            new_user.mobile_code_expired = expired_time
            new_user.save()
        return jsonify({
            'status': 'success',
            'message': 'code is generate and send to mobile',
            'data': {}
        })

@auth.route('/login-by-sms', methods=['POST', 'GET'])
def login_by_sms_view():
    if request.method == 'POST':
        try:
            user_data = user_login_sms_schema.load(request.get_json())
        except Exception as ex:
            return jsonify({
                'status': 'error',
                'message': f'Error : {ex}',
                'data': {}
            })
        user = UserModel.query.filter_by(mobile=user_data['mobile']).first()
        if (user.mobile_code_expired < datetime.datetime.now()) :
            print('time is expired')
            return jsonify({
                'status': 'error_expire',
                'message': 'time is expired',
                'data': {}
            })
        elif user.mobile_code != user_data['code']:
            return jsonify({
                'status': 'error',
                'message': 'code is incorrect',
                'data': {}
            })
        else:
            person = user_schema.dump(user)
            user.mobile_code = None
            user.mobile_code_expired = None
            user.update()
            login_user(user)
            print('use is logged')
            return jsonify({
                'status': 'success',
                'message': 'user is logged successfully',
                'data': person
            })
            
    return render_template('auth/login-by-sms.html')


@auth.route('/check-mobile', methods=['POST'])
def check_mobile():
    try:
        user_data = user_mobile_schema.load(request.get_json())
        exist_mobile = UserModel.query.filter_by(mobile = user_data['mobile']).first()
        if exist_mobile:
            return jsonify({
                'status': 'success',
                'message': 'mobile number exists ',
                'data': ''
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'mobile number is not exists ',
                'data': ''
            })
    except Exception as ex:
        return jsonify({
            'status': 'error',
            'message': f'{ex}',
            'data': ''
        })
# end login methods


# --------------------------------------------------------------------
@auth.route('/whoami')
def whoami():
    user = user_schema.dump(current_user)
    return jsonify({
        'status': 'success',
        'message': 'current user information',
        'data': user
    })



# ---------------------------------------------------------------------------
@auth.route('/logout')
def logout_view():
    # full_name = current_user.full_name
    logout_user()
    return jsonify({
        'status': 'success',
        'message': 'user is logged out successfully',
        'data': {}
    })

