from app1 import app
from backend import db,User,Customer,Professional,Service

# Admin = [
#     ('Admin@gmail.com','435',True,False,False,False)
# ]

# service = [
#     ('Cleaning',10,'different types of cleanings',1),
#     ('Cars repair',20,'car parts repair',2),
#     ('Ac' , 30,'AC works',3),
#     ('Electronic',40,'electronic repairs',4),
# ]

# for s in service:
#     a = Service(name = s[0],price = s[1],timerequired = s[3],discription = s[2])
#     db.session.add(a)
#     db.session.commit()

pro = [
    ('a','a','a',1,'Cleaning','Home cleaning',1,'a',1),
    ('b','b','b',2,'Cars repair','Mirror replacement',2,'b',2),
    ('c','c','c',3,'Cleaning','kitchen cleaning',3,'c',3),
    ('d','d','d',4,'Ac','Heating issue',4,'d',4),
    ('e','e','e',5,'Electronic','mobile issues',5,'e',5),
    ('f','f','f',6,'Ac','Water leackage',6,'f',6)
]

for p in pro:
    
    a = Professional(username = p[0],password = p[1],fullname = p[2],sev_name = p[4],phone = p[3],specality = p[5],Experience = p[6],address = p[7],pincode = p[8])
    
    db.session.add(a)
    db.session.commit()

for u in pro:
    a = User(username = u[0],password = u[1],iscustomerctive = 0,isprofressional = 0,isadmin = 0,isblocklisted = 0)
    db.session.add(a)
    db.session.commit()



# for A in Admin:
#     c = User(username = A[0],password = A[1],isadmin =A[2],iscustomerctive = A[3],isprofressional = A[4],isblocklisted = A[5])
#     db.session.add(c)
#     db.session.commit()



