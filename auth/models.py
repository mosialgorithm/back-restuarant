from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
# from persiantools.jdatetime import JalaliDateTime


class UserModel(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=True, unique=True)
    mobile = Column(String(11), nullable=True, unique=True)
    mobile_code = Column(String(6), nullable=True)
    mobile_code_expired = Column(DateTime())
    full_name = Column(String(128), nullable=True)
    avatar = Column(String(125), default='/static/images/users/avatar/avatar.png')
    username = Column(String(128), nullable=True, unique=True)
    password = Column(String(500), nullable=True)
    role = Column(Integer(), nullable=False, default=4)
    gender = Column(Boolean(), default=True)
    email_token = Column(String(150), nullable=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    # logs = db.relationship('UserLogModel', backref='user')

    def __repr__(self):
        return f'{self.id} :: {self.mobile}'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def is_superuser(self):
        return self.role == 0
    
    def is_admin(self):
        return self.role <= 1
    
    def is_staff(self):
        return self.role == 2
    
    def sex(self):
        return 'male' if self.gender==True else 'female'
    
