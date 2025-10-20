from app import db
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import UserModel
from datetime import datetime



# category model
class ProductCategoryModel(db.Model):
    __tablename__ = 'product_categories'
    
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False, unique=True)
    description = Column(String(200), nullable=True)
    image = Column(String(125), default='/static/images/product/product.png')
    manager_id = Column(Integer(), ForeignKey('users.id'))
    products = db.relationship('ProductModel', backref='category', lazy=True)
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    
    def __repr__(self):
        return self.title
    
    def manager(self):
        return UserModel.query.get_or_404(self.manager_id).full_name
    
    
# product model   
class ProductModel(db.Model):
    __tablename__ = 'products'
    
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False, unique=True)
    image = Column(String(125), default='/static/images/product/product.png')
    price = Column(Integer(), nulldable=False)
    category_id = Column(Integer(), ForeignKey('product_categories.id'))
    created_at = Column(DateTime(), default=datetime.now())
    updated_at = Column(DateTime(), default=datetime.now())
    
    def __repr__(self):
        return self.title
    
    def category(self):
        return ProductCategoryModel.query.get_or_404(self.category_id).title
    