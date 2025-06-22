import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from backend import db,User,Customer,Professional,Service,ServiceRequest
from datetime import datetime,date

import matplotlib.pyplot as plt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userdata.sqlite3'

db.init_app(app)
app.app_context().push()
db.create_all()





@app.route('/')
def home():
    return render_template('home.html')


# Admin related links and routes
#_________________________________

@app.route('/astats/<int:uid>')
def astats(uid):
    

    user1 = User.query.filter_by(isprofressional = 1,isblocklisted = 0).count()
    user2 = User.query.filter_by(isprofressional = 1,isblocklisted = 1).count()
    user3 = User.query.filter_by(isprofressional = 0,isblocklisted = 0,iscustomerctive = 0,isadmin = 0).count()
    data = {
        'labels': ['Proffesionals', 'Blocked professionals', 'Upcoming professionals'],
        'values': [user1,user2 ,user3 ]
    }
    
    # Pass data to the template
   
    

    serv1 = ServiceRequest.query.filter_by(status = 'closed').count()
    serv2 = ServiceRequest.query.filter_by(status = 'requested').count()
    serv3 = ServiceRequest.query.filter_by(status = 'accepted').count()
    serv4 = ServiceRequest.query.filter_by(status = 'rejected').count()
    data1 = {
        'labels': ['closed', 'requested', 'accepted','rejected'],
        'values': [serv1,serv2 ,serv3,serv4]
    }
    
    return render_template('/Admin/astats.html', uid=uid, chart_data=data,data1 = data1)
    
    


@app.route('/block/<int:uid>')
def block(uid):
    pro = Professional.query.all()
    cus = Customer.query.all()
    user = User.query.all()
    use = {us.username:{'block':us.isblocklisted,'id':us.id,'ap':us.isprofressional} for us in user}
    return render_template('./Admin/block.html',pro = pro,cus = cus,use = use,uid = uid)

@app.route('/block1/<int:uid>/<int:svid>')
def blockid(uid,svid):
    use = User.query.filter_by(id = svid).first()
    use.isblocklisted = 1
    db.session.commit()
    
    return redirect(f'/ahome/{uid}')

@app.route('/unblock/<int:uid>/<int:svid>')
def unblock(uid,svid):
    use = User.query.filter_by(id = svid).first()
    use.isblocklisted = 0
    db.session.commit()
    return redirect(f'/ahome/{uid}')

@app.route('/alogin')
def alogin():
    return render_template('alogin.html')

@app.route('/servive')
def service():
    return render_template('/Admin/serviceform.html')

@app.route('/ahome/<int:uid>')
def ahome(uid):
    data = Service.query.all()
    info = ServiceRequest.query.all()
    proinfo = Professional.query.all()
    proi = {pro.id:pro.fullname for pro in proinfo}
    ur = User.query.all()
    user = {u.username:{'prof':u.isprofressional,'block':u.isblocklisted} for u in ur}
    #info = Professional_data.query.all()
    return render_template('/Admin/adminhome.html',data = data,info = info,proinfo=proinfo,uid = uid,user = user,proi = proi)

@app.route('/addser/<int:uid>')
def addser(uid):
    return render_template('/Admin/serviceform.html',uid = uid)

@app.route('/addreq/<int:uid>',methods = ["POST"])
def addreq(uid):
    sname = request.form.get('sname')
    bp = request.form.get('baseprice')
    tr = request.form.get('timereq')
    des = request.form.get('description')
    serv = Service(name = sname,price = bp,timerequired = tr,discription = des)
    db.session.add(serv)
    db.session.commit()
    return redirect(f'/ahome/{uid}')



@app.route('/seredit/<int:uid>/<int:servid>')
def seredit(uid,servid):
    serv = Service.query.filter_by(id = servid).first()
    return render_template('/Admin/sedit.html',uid = uid,serv = serv, servid = servid)

@app.route('/sedit/<int:uid>/<int:servid>',methods = ['POST'])
def sedit(uid,servid):
    bsp = request.form.get('bp')
    tr = request.form.get('tr')
    
    ser = Service.query.filter_by(id = servid).first()
    ser.price = int(bsp)
    ser.timerequired = int(tr)
    db.session.commit()
    return redirect(f'/ahome/{uid}')

@app.route('/serdel/<int:uid>/<int:servid>')
def serdel(uid,servid):
    ser = Service.query.get(servid)
    db.session.delete(ser)
    db.session.commit()
    return redirect(f'/ahome/{uid}')



@app.route('/asearch/<int:uid>')
def asearch(uid):
    return render_template('./Admin/asearch.html',uid = uid)

@app.route('/paccept/<int:uid>,<int:proid>')
def paccept(uid,proid):
    pro = Professional.query.filter_by(id = proid).first()
    use = User.query.filter_by(username = pro.username).first()
    use.isprofressional = 1
    db.session.commit()
    return redirect(f'/ahome/{uid}')

@app.route('/pdelete/<int:uid>,<int:proid>')
def pdelete(uid,proid):
    pro = Professional.query.get(proid)
    use = User.query.filter_by(username = pro.username).first()
    user = User.query.get(use.id)
    db.session.delete(user)
    db.session.commit()
    db.session.delete(pro)
    db.session.commit()
    return redirect(f'/ahome/{uid}')




@app.route('/aresult/<int:uid>' ,methods = ['POST'])
def aresult(uid):
    asel = request.form.get('select2')
    aser = request.form.get('search2')
    # return (f"{asel} {aser}")

    ser_req = ServiceRequest.query.all()
    ser = Service.query.all()
    Custo = Customer.query.all()
    profe = Professional.query.all()
    service = {se.id:se.name for se in ser}
    customer = {cust.id:cust.username for cust in Custo}
    profesional = {pro.id:pro.username for pro in profe}

    return render_template('./Admin/aresult.html',uid = uid,data = ser_req,
                           customer = customer,profesional = profesional,aser = aser,service = service)



# @app.route('/stats')
# def astat():
#     pass



#Customer related routes and links
#____________________________________
    

@app.route('/csign')
def csign():
    return render_template('csignup.html')

@app.route('/csignup' , methods = ['POST'])
def singup():
    email = request.form.get('email')
    password = request.form.get('password1')
    pass2 = request.form.get('password2')
    fullname = request.form.get('fullname')
    address = request.form.get('address')
    pin = request.form.get('pincode')
    phone = request.form.get('phone')
    Cust = Customer.query.filter_by(username = email).first()
    cust1 = Customer.query.filter_by(phone = phone).first()
    if (cust1 or Cust):
        flash("User or Phone number is already exist")
        return redirect('/alogin')



    users = User.query.all()
    for user in users:
        if (email==user.username):
            flash('user already exist','success')
            return redirect('/alogin')
        
    if(password != pass2):
        flash("Conform passward is incorrect so please login again","danger")
        return redirect('/csign')

    cust = Customer(username=email, password=password,fullname = fullname,phone = phone, address = address,pincode = pin)
    user = User(username = email, password = password,iscustomerctive = True)
    db.session.add(cust)
    db.session.add(user)
    db.session.commit()

    flash('Registration is successful!','success')
    return redirect('/alogin')

@app.route('/cstats/<int:uid>')
def cstats(uid):
     # Query counts for each service status
    serv1 = ServiceRequest.query.filter_by(status='closed').count()
    serv2 = ServiceRequest.query.filter_by(status='requested').count()
    serv3 = ServiceRequest.query.filter_by(status='accepted').count()
    
    # Prepare the data for Chart.js
    data = {
        'labels': ['Closed', 'Requested', 'Accepted'],
        'values': [serv1, serv2, serv3]
    }
    
    # Pass data to the template
    return render_template('/Customer/cstats.html', uid=uid, chart_data=data)


@app.route('/chome/<int:uid>')
def customerhome(uid):
    data = Service.query.all()
    ser_req = ServiceRequest.query.all()
    use = User.query.filter_by(id = uid).first()
    cus = Customer.query.filter_by(username = use.username).first()
    profe = Professional.query.all()
    sname = {service.id:service.name for service in data}
    prof = {pro.id:{'name':pro.username,'phone':pro.phone} for pro in profe}
    ur = User.query.all()
    user = {u.username:{'prof':u.isprofressional,'block':u.isblocklisted} for u in ur}
    return render_template('/Customer/customerhome.html', data=data, uid=uid, cid=cus.id, serreq=ser_req, prof=prof, sname=sname,user = user)

@app.route('/close/<int:uid>/<int:serid>')
def serviceclose(uid,serid):
    
    ser_req = ServiceRequest.query.filter_by(id = serid).first()
    data = Service.query.filter_by(id = ser_req.service_id).first()
    profe = Professional.query.filter_by(id = ser_req.proffesional_id).first()
    

    return render_template('./Customer/ser_reqclose.html',uid = uid,data = data,ser_req = ser_req,profe = profe)

@app.route('/rating/<int:uid>/<int:serid>', methods = ['POST'])
def close(uid,serid):
    rate = request.form.get('Rating')
    remarks = request.form.get('remarks')
    cdate = datetime.now()
    ser_req = ServiceRequest.query.filter_by(id = serid).first()
    ser_req.dateofcomplete = cdate.date()    
    ser_req.rating = int(rate)
    prof = Professional.query.filter_by(id = ser_req.proffesional_id).first()
    if prof.rating:
        prof.rating = (prof.rating+int(rate))/2
    else:
        prof.rating = int(rate)
    ser_req.status = 'closed'
    if remarks:
        ser_req.remarks = remarks
    
    db.session.commit()
    return redirect(f'/chome/{uid}')


@app.route('/package/<int:serid>/<int:uid>')
def packageselection(serid,uid):
    ser = Professional.query.all()
    data1 = Service.query.filter_by(id = serid).first()
    ur = User.query.all()
    user = {u.username:{'prof':u.isprofressional,'block':u.isblocklisted} for u in ur}
    
            
    return render_template('/Customer/customerpackages.html', data = ser, service = data1.name, price = data1.price,uid = uid,serid = serid,user = user)

@app.route('/addserreq/<int:uid>/<int:serid>/<int:proid>')
def addserreq(uid,serid,proid):
    today = datetime.now()

    req_date = today.date()
    use = User.query.filter_by(id=uid).first()
    cus = Customer.query.filter_by(username = use.username).first()
    serreq = ServiceRequest(service_id = serid,customer_id = cus.id,proffesional_id = proid,dateofrequest = req_date,status = 'requested')
    db.session.add(serreq)
    db.session.commit()
    return redirect(f'/chome/{uid}')


@app.route('/csearch/<int:uid>')
def csearch(uid):
    return render_template('./Customer/csearch.html',uid = uid)

@app.route('/csearchresult/<int:uid>',methods = ['POST'])
def cresult(uid):
    sele = request.form.get('select')
    serc = request.form.get('search')
    service = False
    pincode = False
    
    if sele =='Pincode':
        serc = int(serc)
        pincode = True
    else:
        service = True
        
    data = Service.query.all()
    prof = Professional.query.all()
    sname = {serv.name:{'service_id':serv.id,'price':serv.price} for serv in data}
    return render_template('./Customer/cresult.html',uid = uid,service = service,pincode = pincode,serc = serc,data = data,sname = sname,prof = prof)


@app.route('/cedit/<int:uid>')
def cedit(uid):
    use = User.query.filter_by(id = uid).first()
    cus = Customer.query.filter_by(username = use.username).first()

    return render_template('./Customer/cedit.html',uid = uid,cus = cus)

@app.route('/modify/<int:uid>/<int:cid>', methods = ['POST'])
def modify(uid,cid):
    cust = Customer.query.filter_by(id = cid).first()
    use = User.query.filter_by(id = uid).first()

    password = request.form.get('bp')
    phone = request.form.get('tr')

    cust.password = password
    use.password = password
    cust.phone = phone
    db.session.commit()
    return redirect(f'/chome/{uid}')

#professional related links and routes
#________________________________________

@app.route('/login', methods = ['POST'])
def login():
    username = request.form.get('uname')
    password = request.form.get('password')

    user = User.query.filter_by(username = username, password=password).first()
    
    if user:

        admin = User.query.filter_by(username = username, password=password, isadmin = 1).first()
        cactive = User.query.filter_by(username = username, password=password,iscustomerctive = 1,isblocklisted = 0).first()
        pactive = User.query.filter_by(username = username, password=password,isprofressional = 1,isblocklisted = 0).first()
        if admin:
            session['uid'] = admin.id
            return redirect(f'/ahome/{admin.id}')
        
        elif cactive:
            session['uid'] = user.id
            return redirect(f'/chome/{user.id}')
        
        elif pactive:
            session['uid'] = user.id
            return redirect(f'/phome/{user.id}')
            
        
    else:
        flash('Please register first','danger')
        return redirect(url_for('home'))

@app.route('/pstats/<int:uid>')
def pstats(uid):
    use = User.query.filter_by(id = uid).first()
    pro = Professional.query.filter_by(username = use.username).first()
    serv1 = ServiceRequest.query.filter_by(status = 'closed',proffesional_id = pro.id).count()
    serv2 = ServiceRequest.query.filter_by(status = 'requested',proffesional_id = pro.id).count()
    serv3 = ServiceRequest.query.filter_by(status = 'accepted',proffesional_id = pro.id).count()
    serv4 = ServiceRequest.query.filter_by(status = 'rejected',proffesional_id = pro.id).count()
    
    data1 = {
        'labels': ['closed', 'requested', 'accepted','rejected'],
        'values': [serv1,serv2,serv3,serv4]
    }
    
    if pro.rating>0:
        r5 = ServiceRequest.query.filter_by(proffesional_id = pro.id,status = 'closed',rating = 5).count()
        r4 = ServiceRequest.query.filter_by(proffesional_id = pro.id,status = 'closed',rating = 4).count()
        r3 = ServiceRequest.query.filter_by(proffesional_id = pro.id,status = 'closed',rating = 3).count()
        r2 = ServiceRequest.query.filter_by(proffesional_id = pro.id,status = 'closed',rating = 2).count()
        r1 = ServiceRequest.query.filter_by(proffesional_id = pro.id,status = 'closed',rating = 1).count()
        data2 = {
        'labels': ['rated 1','rated 2','rated 3','rated 4','rated 5'],
        'values': [r1,r2,r3,r4,r5]
    }
        
    else:
        data2 = {
            'labels':['No one rate yet'],
            'values':[0]
        }
    return render_template('/Professional/pstats.html',uid = uid,data1 = data1,data2 = data2)


@app.route('/psign')
def psign():
    sdata = Service.query.all()
    return render_template('psignup.html', data = sdata)

@app.route('/psignup',methods = ['POST'])
def psignup():
    
    email = request.form.get('email')
    password = request.form.get('password')
    pass2 = request.form.get('password1')
    fullname = request.form.get('fname')
    address = request.form.get('address')
    service = request.form.get('selection')
    Experience = request.form.get('experience')
    specality = request.form.get('specality')
    pin = request.form.get('pincode')
    # file = request.files.get('document')
    phone = request.form.get('phone')
    file = request.files.get('document')
    
    
    
    
    users = User.query.all()
    for user in users:
        if (email==user.username):
            flash('user already exist','success')
            return redirect('/alogin')
        
    if(password != pass2):
        flash("Conform passward is incorrect so please login again","danger")
        return redirect(url_for('psign'))
    
    

    cust1 = Professional(username=email, password=password,fullname = fullname,phone = phone,sev_name = service,specality = specality,
                        Experience = Experience, address = address,pincode = pin)
    user1 = User(username = email, password = password,isprofressional = False)
    
    db.session.add(cust1)
    db.session.add(user1)
    db.session.commit()
    filename=f'{email}.txt'
    file.save(os.path.join('./static/professionalfiles', filename))
    return redirect('/alogin')



@app.route('/ppedit/<int:uid>')
def ppedit(uid):
    use = User.query.filter_by(id = uid).first()
    pos = Professional.query.filter_by(username = use.username).first()

    return render_template('./Professional/pedit.html',uid = uid,pos = pos)

@app.route('/pmodify/<int:uid>/<int:pid>', methods = ['POST'])
def pmodify(uid,pid):
    cust = Professional.query.filter_by(id = pid).first()
    use = User.query.filter_by(id = uid).first()
    password = request.form.get('bp')
    ph = request.form.get('tr')
    exp = request.form.get('exp')
    prof = Professional.query.filter_by(phone = ph).first()
    
    if prof:
        flash('This phone number is already exist','Danger')
        return redirect(f'/phome/{uid}')
    
    cust.password = password
    use.password = password
    cust.phone = ph
    cust.Experience = exp
    db.session.commit()
    return redirect(f'/phome/{uid}')






@app.route('/phome/<int:uid>')
def phome(uid):
    today = datetime.now()
    req_date = today.date()
    # data = Service.query.all()
    ser_req = ServiceRequest.query.all()
    use = User.query.filter_by(id = uid).first()
    prof = Professional.query.filter_by(username = use.username).first()
    custo = Customer.query.all()
    proa = Professional.query.all()
    proi = {pro.id:pro.username for pro in proa}
    custdet = {cust.id:{'name':cust.username,'phone':cust.phone,'location':cust.address,'pincode':cust.pincode} for cust in custo}
    return render_template('/Professional/prohome.html',uid = uid,date = req_date,ser_req = ser_req,proid = prof.id,custdet = custdet,proi = proi)

@app.route('/psearch/<int:uid>')
def psearch(uid):
    return render_template('./Professional/psearch.html',uid = uid)

@app.route('/paccept/<int:uid>/<int:serid>')
def accept(uid,serid):
    ser_req = ServiceRequest.query.filter_by(id = serid).first()
    ser_req.status = 'accepted'
    db.session.commit()
    return redirect(f'/phome/{uid}')


@app.route('/preject/<int:uid>/<int:serid>')
def reject(uid,serid):
    ser_req = ServiceRequest.query.filter_by(id = serid).first()
    ser_req.status = 'rejected'
    db.session.commit()
    return redirect(f'/phome/{uid}')




@app.route('/presult/<int:uid>',methods = ['POST'])
def presult(uid):
    psel = request.form.get('select1')
    pser = request.form.get('search1')
    lis = pser.split('/')
    pin = False
    dat = False
    loc = False
    if psel == "Date":
        dat = True
        pser = date(int(lis[-1]),int(lis[-2]),int(lis[0]))
    elif psel == 'Pincode':
        pin = True
        pser = int(pser)
    else:
        loc = True

    use = User.query.filter_by(id = uid).first()
    prof = Professional.query.filter_by(username = use.username).first()

    ser_req = ServiceRequest.query.all()
    customer = Customer.query.all()
    cust = {cust.id:{'cname':cust.username,'loc':cust.address,'pin':cust.pincode} for cust in customer}
    return render_template('./Professional/presult.html',uid = uid,cust=cust,pser = pser,
                           data = ser_req,loc = loc,pin = pin,dat = dat,proid = prof.id)
    

# @app.route('/pstats')
# def pstats():
#     pass

@app.route('/logout')
def logout():
    
    
    session.pop('uid', None)
    
    return redirect(url_for('home'))






    



 


if __name__ == '__main__':    
    app.run(debug = True)


