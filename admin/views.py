import os
from app import app
from flask import render_template, request, jsonify
from . import admin
from flask_login import logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from auth.schemas import user_schema
from .schemas import category_schema


@admin.route('/')
@login_required
def index_view():
    return render_template('admin/index.html')

# ================================ User Management ============================================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    if request.method == 'POST':
        file = request.files.get('avatar_file')
        if file and allowed_file(file.filename):
            filename = file.filename
            print(file, filename)
            os.makedirs(app.config['UPLOAD_AVATAR'], exist_ok=True)
            location = os.path.join(app.config['UPLOAD_AVATAR'], filename)
            try:
                file.save(location)
                # current_user.avatar = location
                current_user.avatar = f'/static/uploads/users/avatar/{filename}'
                current_user.update()
                return jsonify({
                    'status': 'success',
                    'message': 'file is uploaded successfully',
                    'data': {}
                })
            except Exception as ex:
                return jsonify({
                    'status': 'error',
                    'message': f'Error {ex} is happened',
                    'data': {}
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'no file is chosen for upload !! ,please try again',
                'data': {}
            })

@admin.route('/update-user', methods=['POST'])
@login_required
def update_user():
    if request.method == 'POST':
        user_data = user_schema.load(request.get_json())
        current_user.full_name = user_data['full_name']
        current_user.email = user_data['email']
        current_user.role = int(user_data['role'])
        current_user.gender = user_data['gender']
        try:
            current_user.update()
            user_update = user_schema.dump(current_user)
            return jsonify({
                'status': 'success',
                'message': 'user is updated successfully',
                'data': user_update
            })
        except Exception as ex:
            return jsonify({
                'status': 'error',
                'message': f'Error {ex} is happened',
                'data': {}
            })
    else:
        return jsonify({
            'status': 'error',
            'message': 'request is not POST, please try again',
            'data': {}
        })
        
# ================================ END User Management ===========================================

# ================================ Product Management ============================================
@admin.route('/category', methods=['POST', 'GET'])
@login_required
def category():
    if request.method == 'POST':
        user_data = category_schema.load(request.get_json())
        print(user_data)
    
    return render_template('category/index.html')

@admin.route('/product', methods=['POST', 'GET'])
@login_required
def product():
    
    return render_template('product/index.html')

# ================================ END Product Management ========================================