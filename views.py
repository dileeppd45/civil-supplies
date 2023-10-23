from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from . import views





def login(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        cursor = connection.cursor()
        cursor.execute("select * from login where admin_id= '" + userid + "' AND password = '" + password + "'")
        admin = cursor.fetchone()
        if admin == None:
            cursor.execute("select * from ration_shop where idration_shop = '" + userid + "' AND password = '" + password + "' and status ='approved'  ")
            ration = cursor.fetchone()
            if ration == None:
                    return HttpResponse("<script>alert('Invalid User or not approved yet..');window.location='../login';</script>")
            else:
                request.session['ratid'] = userid
                return redirect('ration_home')

        else:
            request.session['adminid'] = userid
            return redirect('admin_home')
    return render(request, "login.html")



def register(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    return render(request, 'register_view_district.html',{'district':district})

def choose_district(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from taluk where iddistrict = '" + str(id) + "' ")
    taluk = cursor.fetchall()
    return render(request, 'register_view_taluk.html', {'taluk': taluk})

def register_shop(request,id):
    return render(request, 'register_shop.html', {'id':id })

def shop_register(request):
    if request.method == "POST":
        id = request.POST['id']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['psw']
        cursor = connection.cursor()
        cursor.execute("insert into ration_shop values (null,'" + str(address) + "','" + str(phone) + "', '" + str(email) + "', '" + str(password)+"', 'pending', '"+str(id)+"') ")
        return redirect("login")


def admin_home(request):
    return render(request, 'admin_home.html')

def ration_home(request):
    return render(request, 'ration_home.html')

def view_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    return render(request, 'view_district.html',{'district':district})

def view_taluk(request, id):
    cursor = connection.cursor()
    request.session['distid'] = id
    cursor.execute("select * from taluk where iddistrict = '"+str(id)+"' ")
    taluk= cursor.fetchall()
    return render(request, 'view_taluk.html', {'taluk':taluk})

def view_ration_pending(request, id):
    distid = request.session['distid']
    request.session['talukid'] = id
    cursor = connection.cursor()
    cursor.execute("select ration_shop.*, taluk.name from ration_shop join taluk where ration_shop.taluk_id = taluk.idtaluk and status = 'pending' and ration_shop.taluk_id ='"+str(id)+"' ")
    ration = cursor.fetchall()
    return render(request, 'view_ration_pending.html', {'ration': ration, 'back':distid})

def approve_ration(request,id):
    tid = request.session['talukid']
    cursor = connection.cursor()
    cursor.execute("update ration_shop set status ='approved' where idration_shop ='"+str(id)+"' ")
    return redirect('view_ration_pending', id=int(tid))

def view_ration(request, id):
    distid = request.session['distid']
    request.session['talukid'] = id
    cursor = connection.cursor()
    cursor.execute("select ration_shop.*, taluk.name from ration_shop join taluk where ration_shop.taluk_id = taluk.idtaluk and status = 'approved' and ration_shop.taluk_id ='"+str(id)+"' ")
    ration = cursor.fetchall()
    return render(request, 'view_ration_approved.html', {'ration': ration, 'back':distid})


def add_taluk(request, id):
    return render(request, 'add_taluk.html',{'id':id})


def taluk_add(request):
    if request.method == "POST":
        iddistrict = request.POST['id']
        name = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("insert into taluk values (null,'" + str(iddistrict) + "','" + str(name) + "') ")
        return redirect("view_taluk", id=int(iddistrict))


def view_user_requests(request):
    id = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute(" select user_register.*,card_type.name  from user_register join card_type where idration_shop = '"+str(id)+"' and status = 'requested' and user_register.idcard_type = card_type.idcard_type")
    data = cursor.fetchall()
    return render(request, 'view_user_request.html', {'data':data})

def ration_view_users(request):
    id = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute(" select user_register.*, card_type.name from user_register join card_type  where user_register.idration_shop = '" + str(id) + "' and user_register.status = 'approved' and user_register.idcard_type = card_type.idcard_type")
    data = cursor.fetchall()
    return render(request, 'ration_view_users.html', {'data': data})

def approve_user(request, id):
    cursor = connection.cursor()
    cursor.execute(" update user_register set status ='approved' where user_id ='"+str(id)+"' ")
    return redirect('view_user_requests')


def add_card_items(request):
    cursor = connection.cursor()
    cursor.execute(" select * from card_type ")
    data=cursor.fetchall()
    return render(request,'add_card_items.html', {'data':data})


def card_items_add(request):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        card_type=request.POST['card_type']
        prise = request.POST['prise']
        cursor = connection.cursor()
        cursor.execute("insert into card_items values (null,'" + str(name) + "','" + str(quantity) + "','no need','" + str(card_type) + "', '"+str(prise)+"') ")
        return redirect("add_card_items")

def view_card_items(request):
    cursor = connection.cursor()
    '''cursor.execute("select idcard_type from card_type ")
    types = cursor.fetchall()
    types = list(types)'''
    cursor.execute("select card_items.*, card_type.name from card_items join card_type where card_items.idcard_type = card_type.idcard_type  and card_type.name = 'APL'")
    apl = cursor.fetchall()
    cursor.execute("select card_items.*, card_type.name from card_items join card_type where card_items.idcard_type = card_type.idcard_type  and card_type.name = 'BPL'")
    bpl = cursor.fetchall()
    return render(request, 'view_card_items.html', {'apl': apl, 'bpl': bpl})

def ration_card_items(request):
    cursor = connection.cursor()
    cursor.execute("select card_items.*, card_type.name from card_items join card_type where card_items.idcard_type = card_type.idcard_type  and card_type.name = 'APL'")
    apl = cursor.fetchall()
    cursor.execute("select card_items.*, card_type.name from card_items join card_type where card_items.idcard_type = card_type.idcard_type  and card_type.name = 'BPL'")
    bpl = cursor.fetchall()
    return render(request, "view_ration_details.html", {'apl': apl, 'bpl': bpl})

def edit_card_item(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from card_items where idcard_items ='"+str(id)+"' ")
    data = cursor.fetchone()
    cursor.execute(" select * from card_type ")
    data1 = cursor.fetchall()
    return render(request, 'edit_card_item.html',{'item':data, 'card_type':data1})

def card_item_edit(request):
    if request.method == "POST":
        name = request.POST['name']
        quantity = request.POST['quantity']
        card_type=request.POST['card_type']
        prise = request.POST['prise']
        cursor = connection.cursor()
        cursor.execute("update card_items  set  item_name ='"+str(name)+"' , item_quantity ='"+str(quantity)+"', idcard_type ='"+str(card_type)+"', prise ='"+str(prise)+"' where idcard_item ='"+str(id)+" '")
        return redirect("view_card_items")



def delete_card_item(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from card_items where idcard_items ='" + str(id) + "' ")
    return redirect("view_card_items")

def order_requests(request):
    ratid = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute("select consume_details.*, user_register.name from consume_details join user_register where consume_details.status = 'requested' and consume_details.idration_shop ='"+str(ratid)+"' and consume_details.user_id = user_register.user_id")
    data = cursor.fetchall()
    return render(request,'order_requests.html',{'data':data})

def proceed_items(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from consume_details where idconsume_details ='"+str(id)+"' ")
    data = cursor.fetchone()
    data = list(data)
    userid = data[1]
    cursor.execute("select idcard_type from user_register where user_id ='"+str(userid)+"' ")
    card = cursor.fetchone()
    card = list(card)
    card = card[0]
    cursor.execute("select name from card_type where idcard_type = '"+str(card)+"' ")
    cardname = cursor.fetchone()
    card_name = list(cardname)
    cardname = card_name[0]
    cursor.execute("select card_items.*, card_type.name from card_items join card_type where card_items.idcard_type = card_type.idcard_type  and card_type.name = '"+str(cardname)+"' ")
    card_items = cursor.fetchall()
    cursor.execute("select available_items.*, card_items.item_name from available_items join card_items where card_items.idcard_items = available_items.item_id and available_items.id_consume = '"+str(id)+"' ")
    available =cursor.fetchall()
    return render(request, 'proceed_items.html',{'user':userid, 'card': card_items, 'cardname': cardname,'consumeid': id, 'available':available})

def send_items(request):
    if request.method == "POST":
        userid = request.POST['user']
        consid =request.POST['consumeid']
        iditem = request.POST['iditem']
        quantity = int(request.POST['rquantity'])
        prise = int(request.POST['rprise'])
        q = int(request.POST['quantity'])
        pperq = float(prise/quantity)
        amount = pperq * q
        cursor = connection.cursor()
        cursor.execute("select * from available_items where id_consume='"+str(consid)+"' and item_id = '"+str(iditem)+"' and user_id = '"+str(userid)+"' and status ='pending'")
        data =cursor.fetchone()

        if data ==None:
            cursor.execute("insert into available_items values(null, '"+str(iditem)+"', '"+str(q)+"', '"+str(amount)+"', '"+str(consid)+"', '"+str(userid)+"', 'pending' )")
        else:
            cursor.execute("update available_items set quantity = '"+str(q)+"', price ='"+str(amount)+"' where item_id ='"+str(iditem)+"' and id_consume = '"+str(consid)+"' and user_id ='"+str(userid)+"' ")
        return redirect("proceed_items", id =int(consid))

def delete_available_item(request,id):
    cursor = connection.cursor()
    cursor.execute("select id_consume from available_items where id_available_items = '"+str(id)+"' ")
    consid=cursor.fetchone()
    consid = list(consid)
    consid = consid[0]
    cursor.execute(" delete from available_items where id_available_items = '"+str(id)+"' ")
    return redirect("proceed_items", id=int(consid))


def provide(reauest, id):

    cursor = connection.cursor()
    cursor.execute("select * from  available_items  where id_consume ='"+str(id)+"' and status ='pending' ")

    cursor.execute("update available_items set status = 'provided' where id_consume ='"+str(id)+"' ")
    cursor.execute("update consume_details set status = 'approved' where idconsume_details = '"+str(id)+"' ")
    return redirect("ration_home")

def purchase_requests(request):
    ratid = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute("select available_items.user_id from available_items join consume_details where  available_items.status = 'selected'  and consume_details.idration_shop = '"+str(ratid)+"' and consume_details.status ='approved' ")
    data=cursor.fetchall()
    data= set(data)

    l=[]
    for i in data:
        a=i[0]
        l.append(a)
    print(l)


    return render(request, 'purchase_requests.html', {'l':l})


def make_bill(request, id):
    ratid = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute("delete from available_items where user_id ='" + str(id) + "' and status = 'provided'")
    cursor.execute("select available_items.*, card_items.item_name from available_items join consume_details join card_items where  card_items.idcard_items = available_items.item_id and available_items.status = 'selected'  and consume_details.idration_shop = '" + str(ratid) + "' and consume_details.status ='approved' and consume_details.user_id ='"+str(id)+"' and available_items.user_id ='"+str(id)+"' ")
    data0 = cursor.fetchall()
    data= list(data0)
    print(data)
    total_amount = 0
    for i in data:
        consid=i[4]
        total_amount=float(i[3])+total_amount
    print(total_amount)
    return render(request,'make_bill.html', {'ta':total_amount,'data':data0,'user':id,'consid':consid})




def remove_available_item(request,id):
    cursor = connection.cursor()
    cursor.execute("select user_id from available_items where id_available_items = '"+str(id)+"' ")
    user=cursor.fetchone()
    user = list(user)
    user = user[0]
    cursor.execute(" delete from available_items where id_available_items = '"+str(id)+"' ")
    cursor.execute("select user_id from available_items where id_available_items = '" + str(id) + "' ")
    user0 = cursor.fetchone()
    if user0 == None:
        return redirect("ration_home")
    return redirect("make_bill",id =str(user))

def cancel_purchase(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from available_items where id_consume = '"+str(id)+"' ")
    cursor.execute("delete from consume_details where idconsume_details ='"+str(id)+"' ")
    return redirect('ration_home')


def make_purchase(request, consid,ta,user):
    ratid = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute("delete from available_items where id_consume ='"+str(consid)+"' and status = 'provided'")
    cursor.execute("update available_items set status = 'purchased' where id_consume ='"+str(consid)+"' ")
    cursor.execute("delete from consume_details where idconsume_details ='"+str(consid)+"' ")
    cursor.execute("insert into user_purchase values(null, '"+str(user)+"','"+str(ta)+"',curdate(),'"+str(ratid)+"','"+str(consid)+"')")
    return redirect('purchase_requests')

def view_bills(request):
    ratid = request.session['ratid']
    cursor = connection.cursor()
    cursor.execute("select * from user_purchase where id_ration_shop = '"+str(ratid)+"' ")
    data=cursor.fetchall()
    return render (request, 'view_bills.html',{'data':data})


def bill_details(request,id):
    cursor = connection.cursor()
    cursor.execute("select available_items.*, card_items.item_name from available_items join  card_items where  card_items.idcard_items = available_items.item_id and available_items.status = 'purchased' and available_items.id_consume = '"+str(id)+"' ")
    data0 = cursor.fetchall()
    data = list(data0)
    print(data)
    total_amount = 0
    for i in data:
        user = i[5]
        consid = i[4]
        total_amount = float(i[3]) + total_amount
    print(total_amount)
    return render(request, 'bill_details.html', {'ta': total_amount, 'data': data0, 'user': user, 'consid':  id})




def view_complaints(request):
    cursor = connection.cursor()
    cursor.execute("select * from  complaints where status = 'pending'")
    data = cursor.fetchall()
    cursor.execute("select * from complaints where status !='pending' ")
    data1 =cursor.fetchall()
    return render(request, 'view_complaints.html',{'data':data,'data1':data1})

def send_reply(request):
    if request.method == "POST":
        reply = request.POST['reply']
        compid =request.POST['compid']
        cursor = connection.cursor()
        cursor.execute("update complaints set reply = '"+str(reply)+"',status ='replied' where idcomplaints ='"+str(compid)+"'")
    return redirect('view_complaints')

def admin_view_bills(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from user_purchase where id_ration_shop = '" + str(id) + "' ")
    data = cursor.fetchall()
    return render(request, 'admin_view_bills.html', {'data': data})

def admin_bill_details(request, id):
    cursor = connection.cursor()
    cursor.execute("select available_items.*, card_items.item_name from available_items join  card_items where  card_items.idcard_items = available_items.item_id and available_items.status = 'purchased' and available_items.id_consume = '" + str(id) + "' ")
    data0 = cursor.fetchall()
    data = list(data0)
    print(data)
    total_amount = 0
    for i in data:
        user = i[5]
        total_amount = float(i[3]) + total_amount
    print(total_amount)
    return render(request, 'admin_bill_details.html', {'ta': total_amount, 'data': data0, 'user': user, 'consid': id})
























