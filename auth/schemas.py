from app import ma
from marshmallow import fields, ValidationError, validates



def validate_fullname(value):
    if len(value) < 5:
        raise ValidationError('Full Name must be at least 5 characters long.')
    
def validate_mobile(value):
    if len(value) != 11:
        raise ValidationError('Mobile Number Must Be 11 character')
    if(value[0] != '0'):
        raise ValidationError('Mobile Number Must Be Start  by 0 character')

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password Must Be atleast 8 character')
    
def validate_code(value):
    if len(value) != 6:
        raise ValidationError('SMS Code Must Be exactly 6 character')
    

# ------------------------------------------------------------
class UserRegisterSchema(ma.Schema):
    full_name = fields.String(required=True, validate=validate_fullname)
    mobile = fields.String(required=True, validate=validate_mobile)
    password = fields.String(required=True, validate=validate_password)
    

user_register_schema = UserRegisterSchema()


# ----------------------------------------------------------------
class UserMobileSchema(ma.Schema):
    mobile = fields.String(required=True, validate=validate_mobile)
    

user_mobile_schema = UserMobileSchema()

# ------------------------------------------------------------------
class UserLoginSchema(ma.Schema):
    mobile = fields.String(required=True, validate=validate_mobile)
    password = fields.String(required=True, validate=validate_password)
    
    
user_login_schema = UserLoginSchema()


# ------------------------------------------------------------------
class UserLoginSmsSchema(ma.Schema):
    mobile = fields.String(required=True, validate=validate_mobile)
    code = fields.String(required=True, validate=validate_code)
    
    
user_login_sms_schema = UserLoginSmsSchema()

# ------------------------------------------------------------------
class UserSchema(ma.Schema):
    id = fields.Integer(load_only=True)
    full_name = fields.String()
    mobile = fields.String()
    email = fields.String(allow_none=True)
    avatar = fields.String()
    role = fields.Integer()
    gender = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
user_schema = UserSchema()
