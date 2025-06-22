from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User_role(db.Model):

#     id = db.Column(db.Integer,primary_key = True)
#     username = db.Column(db.String,unique = True,nullable = False)
#     password = db.Column(db.String,unique = False,nullable = False)

#     Iscustomerctive = db.Column(db.Boolean,nullable = False,default = True)
#     Isprofessional = db.Column(db.Boolean,nullable = False,default = False)
#     Isadmin = db.Column(db.Boolean,nullable = False,default = False)

#     Isblocklisted = db.Column(db.Boolean,nullable = False, default = False)

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,unique = False,nullable = False)
    fullname = db.Column(db.String,unique = False,nullable = False)
    phone = db.Column(db.Integer,unique = True,nullable = False)
    address = db.Column(db.String,unique = False,nullable = False)
    pincode = db.Column(db.Integer,unique = False,nullable = False)
    ser_req = db.relationship('ServiceRequest',backref = 'Customer',lazy = True)

class Professional(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,unique = False,nullable = False)
    phone = db.Column(db.Integer,unique = True,nullable = False)
    fullname = db.Column(db.String,unique = False,nullable = False)
    sev_name = db.Column(db.String,unique = False,nullable = False)
    specality = db.Column(db.String,unique = False,nullable = False)
    Experience = db.Column(db.Integer,unique = False,nullable = True)
    address = db.Column(db.String,unique = False,nullable = False)
    pincode = db.Column(db.Integer,unique = False,nullable = False)
    rating = db.Column(db.Integer,unique = False,default = 0)
    
    
    ser_req = db.relationship('ServiceRequest',backref = 'Professional',lazy = True)


    

class Service(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String,unique = True,nullable = False)
    price = db.Column(db.Integer,nullable = False,unique = False)
    timerequired = db.Column(db.Integer,nullable = False,unique = False)
    discription = db.Column(db.String,unique = False,nullable = False)
    ser_req = db.relationship('ServiceRequest',backref = 'Service',lazy = True)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)

    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,unique = False,nullable = False)

    isadmin = db.Column(db.Boolean,nullable = False,default = False)
    iscustomerctive = db.Column(db.Boolean,nullable = False,default = False)
    isprofressional = db.Column(db.Boolean,nullable = False,default = False)
    isblocklisted = db.Column(db.Boolean,nullable = False, default = False)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    service_id = db.Column(db.Integer,db.ForeignKey('service.id'),nullable = False)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable = False)
    proffesional_id = db.Column(db.Integer,db.ForeignKey('professional.id'),nullable = False)
    dateofrequest = db.Column(db.Date,nullable = False)
    dateofcomplete = db.Column(db.Date,nullable = True)
    status = db.Column(db.String,nullable = False)
    rating = db.Column(db.Integer,unique = False,default = 0)
    remarks = db.Column(db.String,nullable = True)