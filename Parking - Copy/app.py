from flask import *
import os
import pymysql
from datetime import datetime

flask_app = Flask(__name__)
flask_app.secret_key = 'parking'
global uname, details

@flask_app.route('/UpdateResidentDetailsAction', methods=['GET', 'POST'])
def UpdateResidentDetailsAction():
    if request.method == 'POST':
        global details
        floor = request.form['t1']
        door = request.form['t2']
        name = request.form['t3']
        contact = request.form['t4']
        email = request.form['t5']
        aadhar = request.form['t6']
        resident_id = request.form['rid']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addresident where resident_id='"+resident_id+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addresident(resident_id,floor_no,door_no,resident_name,contact_no,email,aadhar_card,status) VALUES('"+str(resident_id)+"','"+floor+"','"+door+"','"+name+"','"+contact+"','"+email+"','"+aadhar+"','Current Resident')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Resident detail updated with id "+str(resident_id)
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in updating resident details"
            return render_template('AdminPage.html', output=data) 


@flask_app.route('/DeleteAdminResident', methods=['GET', 'POST'])
def DeleteAdminResident():
    if request.method == 'GET':
        rid = request.args.get('rid')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addresident where resident_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        data = "Error in deleting details"
        if db_cursor.rowcount == 1:
            data = 'Resident Details Deleted'
        return render_template('AdminPage.html', output=data)

@flask_app.route('/UpdateAdminResident', methods=['GET', 'POST'])
def UpdateAdminResident():
    if request.method == 'GET':
        rid = request.args.get('rid')
        font = '<font size="" color="black">'
        details = '<form name ="f1" method="post" action="/UpdateResidentDetailsAction" onsubmit="return validate(this);"><table align="center" width=30%>'
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addresident where resident_id='"+rid+"'")
            rows = cursor.fetchall()
            for row in rows:
                details += '<tr><td><font size="" color="black">Resident ID</b></td><td><input name="rid" type="text" size="15" value="'+str(row[0])+'" readonly></td></tr>'
                details += '<tr><td><font size="" color="black">Floor No</b></td><td><input name="t1" type="text" size="15" value="'+row[1]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Door&nbsp;No</b></td><td><input name="t2" type="text" size="15" value="'+row[2]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Resident&nbsp;Name</b></td><td><input name="t3" type="Text" size="15" value="'+row[3]+'"></td></td>'
                details += '<tr><td><font size="" color="black">Contact&nbsp;No</b></td><td><input name="t4" type="Text" size="15" value="'+row[4]+'"></td></td></tr>'
                details += '<tr><td><font size="" color="black">Email&nbsp;ID</b></td><td><input type="text" name="t5" size=50 value="'+row[5]+'"/></td></tr>'
                details += '<tr><td><font size="" color="black">Aadhar No</b></td><td><input name="t6" type="Text" size="40" value="'+row[6]+'"></td></td></tr>'
        details += '<tr><td></td><td><input type="submit" value="Submit"></td></table>'        
        return render_template('UpdateResidentDetails.html', output=details)
    

@flask_app.route('/UpdateResidentDetails', methods=['GET', 'POST'])
def UpdateResidentDetails():
    if request.method == 'GET':
        metrics = ['Resident ID', 'Floor No', 'Door No', 'Resident Name', 'Contact No', 'Email ID', 'Aadhar Card', 'Status', 'Delete Record', 'Edit Record']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addresident")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+row[4]+"</font></td>"
                data += "<td>"+font+row[5]+"</font></td>"
                data += "<td>"+font+row[6]+"</font></td>"
                data += "<td>"+font+row[7]+"</font></td>"
                data+='<td><a href=\'DeleteAdminResident?rid='+str(row[0])+'\'><font size=3 color=black>Delete Details</font></a></td>'
                data+='<td><a href=\'UpdateAdminResident?rid='+str(row[0])+'\'><font size=3 color=black>Update Details</font></a></td></tr>'   
        return render_template('UpdateResidentDetails.html', output=data)

@flask_app.route('/AddResident', methods=['GET', 'POST'])
def AddResident():
    return render_template('AddResident.html', output='Manage Resident Details')

@flask_app.route('/ResidentModule', methods=['GET', 'POST'])
def ResidentModule():
    return render_template('ResidentModule.html', output='Manage Resident Details')

@flask_app.route('/AdminPage', methods=['GET', 'POST'])
def AdminPage():
    return render_template('AdminPage.html', output='')

@flask_app.route('/AdminProfileUpdate', methods=['GET', 'POST'])
def AdminProfileUpdate():
    global details
    if request.method == 'GET':
        arr = details.split(",")
        data = '<tr><td><font size="" color="black">Username</b></td>'
        data += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+arr[0]+'" readonly></td></tr>'
        data += '<tr><td><font size="" color="black">Password</b></td><td><input name="t2" type="password" size="30" value="'+arr[1]+'"></td></tr>'
        data += '<tr><td><font size="" color="black">Mobile&nbsp;No</b></td><td><input name="t3" type="Text" size="15" value="'+arr[2]+'"></td></td></tr>'
        data += '<tr><td><font size="" color="black">Email&nbsp;ID</b></td><td><input type="text" name="t5" style="font-family: Comic Sans MS" size=50  value="'+arr[3]+'"/></td></tr>'
        data += '<tr><td><font size="" color="black">Address</b></td><td><input name="t6" type="Text" size="70" value="'+arr[4]+'"></td></td></tr>'    
        return render_template('AdminProfileUpdate.html', output=data)

@flask_app.route('/SearchResidentAdmin', methods=['GET', 'POST'])
def SearchResidentAdmin():
    return render_template('SearchResidentAdmin.html', output='Search Resident Details')

@flask_app.route('/SearchResidentAdminAction', methods=['GET', 'POST'])
def SearchResidentAdminAction():
    if request.method == 'POST':
        query = request.form['t1']
        column = request.form['t2']
        metrics = ['Resident ID', 'Floor No', 'Door No', 'Resident Name', 'Contact No', 'Email ID', 'Aadhar Card', 'Status']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addresident where "+column+" like '%"+query+"%'")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+row[4]+"</font></td>"
                data += "<td>"+font+row[5]+"</font></td>"
                data += "<td>"+font+row[6]+"</font></td>"
                data += "<td>"+font+row[7]+"</font></td></tr>"                 
        return render_template('UpdateResidentDetails.html', output=data)



@flask_app.route('/Register', methods=['GET', 'POST'])
def Register():
    return render_template('Register.html', output='')

@flask_app.route('/AdminLogin', methods=['GET', 'POST'])
def AdminLogin():
    return render_template('AdminLogin.html', output='')

@flask_app.route('/ResidentLogin', methods=['GET', 'POST'])
def ResidentLogin():
    return render_template('ResidentLogin.html', output='')

@flask_app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', output='')

@flask_app.route('/Logout')
def LogoutPage():
    return render_template('index.html', output='')

def isUserExists(table, username, password):
    is_user_exists = False
    global details
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select * from "+table+" where username='"+username+"' and password='"+password+"'")
        rows = cursor.fetchall()
        for row in rows:
            details = row[0]+","+row[1]+","+row[2]+","+row[3]+","+row[4]
            is_user_exists = True
    return is_user_exists

@flask_app.route('/AdminLoginAction', methods=['GET', 'POST'])
def AdminLoginAction():
    global uname
    global details
    if request.method == 'POST' and 't1' in request.form and 't2' in request.form:
        user = request.form['t1']
        password = request.form['t2']
        status = isUserExists("admin", user, password)
        if status == True:
            uname = user
            return render_template('AdminPage.html', output='You logged in as '+uname)
        else:
            return render_template('AdminLogin.html', output="Invalid login details")
        
@flask_app.route('/AddResidentAction', methods=['GET', 'POST'])
def AddResidentAction():
    if request.method == 'POST':
        global details
        floor = request.form['t1']
        door = request.form['t2']
        name = request.form['t3']
        contact = request.form['t4']
        email = request.form['t5']
        aadhar = request.form['t6']
        resident_id = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(resident_id) from addresident")
            rows = cursor.fetchall()
            for row in rows:
                resident_id = row[0]
        if resident_id == None:
            resident_id = 1
        else:
            resident_id = resident_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addresident(resident_id,floor_no,door_no,resident_name,contact_no,email,aadhar_card,status) VALUES('"+str(resident_id)+"','"+floor+"','"+door+"','"+name+"','"+contact+"','"+email+"','"+aadhar+"','Current Resident')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Resident detail added with id "+str(resident_id)
            return render_template('AddResident.html', output=data)
        else:
            data = "Error in adding resident details"
            return render_template('AddResident.html', output=data)  
        
@flask_app.route('/AdminProfileUpdateAction', methods=['GET', 'POST'])
def AdminProfileUpdateAction():
    if request.method == 'POST':
        global details
        uname = request.form['t1']
        password = request.form['t2']
        mobile_no = request.form['t3']
        email = request.form['t5']
        address = request.form['t6']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "update admin set password='"+password+"', contact_no='"+mobile_no+"', email='"+email+"', address='"+address+"' where username='"+uname+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        if db_cursor.rowcount == 1:
            data = "Profile updated"
            details = uname+","+password+","+mobile_no+","+email+","+address
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in updating profile"
            return render_template('AdminPage.html', output=data)   

@flask_app.route('/AddVehicle', methods=['GET', 'POST'])
def AddVehicle():
    data = '<tr><td><font size="" color="black">Resident&nbsp;ID</b></td><td><select name="t1">'
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select resident_id from addresident")
        rows = cursor.fetchall()
        for row in rows:
            data += '<option value="'+str(row[0])+'">'+str(row[0])+"</option>"
    data += "</select></td></tr>"        
    return render_template('AddVehicle.html', rid=data)

@flask_app.route('/VehicleModule', methods=['GET', 'POST'])
def VehicleModule():
    return render_template('VehicleModule.html', output='Manage Resident Details')

        
@flask_app.route('/AddVehicleAction', methods=['GET', 'POST'])
def AddVehicleAction():
    if request.method == 'POST':
        resident_id = request.form['t1']
        vehicle_no = request.form['t2']
        vehicle_name = request.form['t3']
        vehicle_model = request.form['t4']
        vehicle_id = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(vehicle_id) from addvehicle")
            rows = cursor.fetchall()
            for row in rows:
                vehicle_id = row[0]
        if vehicle_id == None:
            vehicle_id = 1
        else:
            vehicle_id = vehicle_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addvehicle(vehicle_id,resident_id,vehicle_no,vehicle_name,vehicle_model) VALUES('"+str(vehicle_id)+"','"+str(resident_id)+"','"+vehicle_no+"','"+vehicle_name+"','"+vehicle_model+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Vehicle detail added with id "+str(vehicle_id)
            return render_template('AddVehicle.html', output=data)
        else:
            data = "Error in adding vehicle details"
            return render_template('AddVehicle.html', output=data)  

@flask_app.route('/UpdateVehicleDetails', methods=['GET', 'POST'])
def UpdateVehicleDetails():
    if request.method == 'GET':
        metrics = ['Vehicle ID', 'Resident ID', 'Vehicle No', 'Vehicle Name', 'Vehicle Model', 'Delete Record', 'Edit Record']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addvehicle")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+row[4]+"</font></td>"
                data+='<td><a href=\'DeleteAdminVehicle?vid='+str(row[0])+'\'><font size=3 color=black>Delete Details</font></a></td>'
                data+='<td><a href=\'UpdateAdminVehicle?vid='+str(row[0])+'\'><font size=3 color=black>Update Details</font></a></td></tr>'   
        return render_template('UpdateVehicleDetails.html', output=data)

@flask_app.route('/UpdateAdminVehicleAction', methods=['GET', 'POST'])
def UpdateAdminVehicleAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        vehicle_no = request.form['t2']
        name = request.form['t3']
        model = request.form['t4']
        vid = request.form['vid']
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addvehicle where vehicle_id='"+vid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addvehicle(vehicle_id,resident_id,vehicle_no,vehicle_name,vehicle_model) VALUES('"+str(vid)+"','"+str(rid)+"','"+vehicle_no+"','"+name+"','"+model+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Vehicle detail updated with id "+str(vid)
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in updating vehicle details"
            return render_template('AdminPage.html', output=data) 


@flask_app.route('/DeleteAdminVehicle', methods=['GET', 'POST'])
def DeleteAdminVehicle():
    if request.method == 'GET':
        rid = request.args.get('vid')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addvehicle where vehicle_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        data = "Error in deleting details"
        if db_cursor.rowcount == 1:
            data = 'Vehicle Details Deleted'
        return render_template('AdminPage.html', output=data)

@flask_app.route('/UpdateAdminVehicle', methods=['GET', 'POST'])
def UpdateAdminVehicle():
    if request.method == 'GET':
        rid = request.args.get('vid')
        font = '<font size="" color="black">'
        details = '<form name ="f1" method="post" action="/UpdateAdminVehicleAction" onsubmit="return validate(this);"><table align="center" width=30%>'
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addvehicle where vehicle_id='"+rid+"'")
            rows = cursor.fetchall()
            for row in rows:
                details += '<tr><td><font size="" color="black">Vehicle ID</b></td><td><input name="vid" type="text" size="15" value="'+str(row[0])+'" readonly></td></tr>'
                details += '<tr><td><font size="" color="black">Resident ID</b></td><td><input name="t1" type="text" size="15" value="'+row[1]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;No</b></td><td><input name="t2" type="text" size="15" value="'+row[2]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;Name</b></td><td><input name="t3" type="Text" size="15" value="'+row[3]+'"></td></td>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;Model</b></td><td><input name="t4" type="Text" size="15" value="'+row[4]+'"></td></td></tr>'
                
        details += '<tr><td></td><td><input type="submit" value="Submit"></td></table>'        
        return render_template('UpdateVehicleDetails.html', output=details)
    
@flask_app.route('/SearchVehicleAdmin', methods=['GET', 'POST'])
def SearchVehicleAdmin():
    return render_template('SearchVehicleAdmin.html', output='Search Resident Details')

@flask_app.route('/SearchVehicleAdminAction', methods=['GET', 'POST'])
def SearchVehicleAdminAction():
    if request.method == 'POST':
        query = request.form['t1']
        column = request.form['t2']
        metrics = ['Vehicle ID', 'Resident ID', 'Vehicle No', 'Vehicle Name', 'Vehicle Model']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addvehicle where "+column+" like '%"+query+"%'")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+row[4]+"</font></td></tr>"                 
        return render_template('UpdateVehicleDetails.html', output=data)
    

#==========================================================vehicle details

def isParkingExists(slot):
    is_parking_exists = False
    global details
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select parking_slot from parkingslot where parking_slot='"+str(slot)+"'")
        rows = cursor.fetchall()
        for row in rows:
            is_parking_exists = True
    return is_parking_exists

def isVehicleAllocated(vehicle):
    is_parking_exists = False
    global details
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select vehicle_no from parkingslot where vehicle_no='"+str(vehicle)+"'")
        rows = cursor.fetchall()
        for row in rows:
            is_parking_exists = True
    return is_parking_exists

@flask_app.route('/AddParking', methods=['GET', 'POST'])
def AddParking():
    data = '<tr><td><font size="" color="black">Resident&nbsp;ID&nbsp;Vehicle&nbsp;No</b></td><td><select name="t1">'
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select resident_id, vehicle_no from addvehicle")
        rows = cursor.fetchall()
        for row in rows:
            if isVehicleAllocated(row[1]) == False:
                data += '<option value="'+str(row[0])+" - "+row[1]+'">'+str(row[0])+" - "+row[1]+"</option>"
    data += "</select></td></tr>"
    data += '<tr><td><font size="" color="black">Parking Slot</b></td><td><select name="t2">'
    for i in range(1,100):
        if isParkingExists(str(i)) == False:
            data += '<option value="'+str(i)+'">'+str(i)+"</option>"
    data += "</select></td></tr>"    
    return render_template('AddParking.html', rid=data)

@flask_app.route('/ParkingModule', methods=['GET', 'POST'])
def ParkingModule():
    return render_template('ParkingModule.html', output='Manage Resident Details')    

@flask_app.route('/AddParkingAction', methods=['GET', 'POST'])
def AddParkingAction():
    if request.method == 'POST':
        vehicle = request.form['t1']
        slot = request.form['t2']
        amount = request.form['t3']
        ptype = request.form['t4']
        arr = vehicle.split("-")
        resident_id = arr[0].strip()
        vehicle_no = arr[1].strip()
        parking_slot = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(parking_id) from parkingslot")
            rows = cursor.fetchall()
            for row in rows:
                parking_slot = row[0]
        if parking_slot == None:
            parking_slot = 1
        else:
            parking_slot = parking_slot + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO parkingslot(parking_id,resident_id,vehicle_no,parking_slot,parking_amount,parking_type) VALUES('"+str(parking_slot)+"','"+str(resident_id)+"','"+vehicle_no+"','"+slot+"','"+amount+"','"+ptype+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Parking slot detail added with id "+str(parking_slot)
            return render_template('AddParking.html', output=data)
        else:
            data = "Error in adding parking details"
            return render_template('AddParking.html', output=data)

@flask_app.route('/UpdateParkingDetails', methods=['GET', 'POST'])
def UpdateParkingDetails():
    if request.method == 'GET':
        metrics = ['Parking ID', 'Resident ID', 'Vehicle No', 'Parking Slot', 'Parking Amount', 'Parking Type', 'Delete Record', 'Edit Record']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from parkingslot")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+str(row[4])+"</font></td>"
                data += "<td>"+font+str(row[5])+"</font></td>"
                data+='<td><a href=\'DeleteAdminParking?vid='+str(row[0])+'\'><font size=3 color=black>Delete Details</font></a></td>'
                data+='<td><a href=\'UpdateAdminParking?vid='+str(row[0])+'\'><font size=3 color=black>Update Details</font></a></td></tr>'   
        return render_template('UpdateParkingDetails.html', output=data)

@flask_app.route('/UpdateAdminParkingAction', methods=['GET', 'POST'])
def UpdateAdminParkingAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        vehicle_no = request.form['t2']
        slot = request.form['t3']
        amount = request.form['t4']
        ptype = request.form['t5']
        pid = request.form['pid']
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from parkingslot where parking_id='"+pid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO parkingslot(parking_id, resident_id, vehicle_no, parking_slot, parking_amount,parking_type) VALUES('"+str(pid)+"','"+str(rid)+"','"+vehicle_no+"','"+slot+"','"+amount+"','"+ptype+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Parking detail updated with id "+str(pid)
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in updating parking details"
            return render_template('AdminPage.html', output=data) 


@flask_app.route('/DeleteAdminParking', methods=['GET', 'POST'])
def DeleteAdminParking():
    if request.method == 'GET':
        rid = request.args.get('vid')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from parkingslot where parking_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        data = "Error in deleting details"
        if db_cursor.rowcount == 1:
            data = 'Parking Details Deleted'
        return render_template('AdminPage.html', output=data)

@flask_app.route('/UpdateAdminParking', methods=['GET', 'POST'])
def UpdateAdminParking():
    if request.method == 'GET':
        rid = request.args.get('vid')
        font = '<font size="" color="black">'
        details = '<form name ="f1" method="post" action="/UpdateAdminParkingAction" onsubmit="return validate(this);"><table align="center" width=30%>'
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from parkingslot where parking_id='"+rid+"'")
            rows = cursor.fetchall()
            for row in rows:
                details += '<tr><td><font size="" color="black">Parking ID</b></td><td><input name="pid" type="text" size="15" value="'+str(row[0])+'" readonly></td></tr>'
                details += '<tr><td><font size="" color="black">Resident ID</b></td><td><input name="t1" type="text" size="15" value="'+row[1]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;No</b></td><td><input name="t2" type="text" size="15" value="'+row[2]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Parking&nbsp;Slot</b></td><td><input name="t3" type="Text" size="15" value="'+row[3]+'"></td></td>'
                details += '<tr><td><font size="" color="black">Parking&nbsp;Amount</b></td><td><input name="t4" type="Text" size="15" value="'+str(row[4])+'"></td></td></tr>'
                details += '<tr><td><font size="" color="black">Parking&nbsp;Type</b></td><td><input name="t5" type="Text" size="15" value="'+str(row[5])+'"></td></td></tr>'
        details += '<tr><td></td><td><input type="submit" value="Submit"></td></table>'        
        return render_template('UpdateParkingDetails.html', output=details)        

@flask_app.route('/SearchParkingAdmin', methods=['GET', 'POST'])
def SearchParkingAdmin():
    return render_template('SearchParkingAdmin.html', output='Search Resident Details')

@flask_app.route('/SearchParkingAdminAction', methods=['GET', 'POST'])
def SearchParkingAdminAction():
    if request.method == 'POST':
        query = request.form['t1']
        column = request.form['t2']
        metrics = ['Parking ID', 'Resident ID', 'Vehicle No', 'Parking Slot', 'Parking Amount']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from parkingslot where "+column+" like '%"+query+"%'")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+str(row[4])+"</font></td></tr>"                 
        return render_template('UpdateParkingDetails.html', output=data)
    
@flask_app.route('/Complaints', methods=['GET', 'POST'])
def Complaints():
    if request.method == 'GET':
        metrics = ['Resident ID', 'Complaint Details', 'Date']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from complaints")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"                
        return render_template('AdminPage.html', output=data)

@flask_app.route('/UpdateStatus', methods=['GET', 'POST'])
def UpdateStatus():
    data = '<tr><td><font size="" color="black">Resident&nbsp;ID</b></td><td><select name="t1">'
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select resident_id from addresident")
        rows = cursor.fetchall()
        for row in rows:
            data += '<option value="'+str(row[0])+'">'+str(row[0])+"</option>"
    data += "</select></td></tr>"
    return render_template('UpdateStatus.html', rid=data)

@flask_app.route('/UpdateStatusAction', methods=['GET', 'POST'])
def UpdateStatusAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        status = request.form['t2']
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "update addresident set status='"+status+"' where resident_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        if db_cursor.rowcount == 1:
            data = "Resident status changed to "+status
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in updating status"
            return render_template('AdminPage.html', output=data)
   

def checkPayment(pid, month, year):
    flag = False
    mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
    with mysql_connect:
        cursor = mysql_connect.cursor()
        cursor.execute("select * from paybill where parking_id='"+pid+"' and paid_month='"+month+"' and paid_year='"+year+"'")
        rows = cursor.fetchall()
        for row in rows:
            flag = True
            break
    return flag    

@flask_app.route('/PayBill', methods=['GET', 'POST'])
def PayBill():
    if request.method == 'GET':
        pid = request.args.get('pid')
        font = '<font size="" color="black">'
        details = '<tr><td><font size="" color="black">Parking ID</b></td><td><input name="t1" type="text" size="15" value="'+str(pid)+'" readonly></td></tr>'
        return render_template('PayBill.html', bill=details)    

@flask_app.route('/PayBillAction', methods=['GET', 'POST'])
def PayBillAction():
    if request.method == 'POST':
        pid = request.form['t1']
        amount = request.form['t2']
        tax = request.form['t3']
        mode = request.form['t4']
        card = request.form['t5']
        today = datetime.now()
        month = str(today.month)
        year = str(today.year)
        billing_no = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(billing_id) from paybill")
            rows = cursor.fetchall()
            for row in rows:
                billing_no = row[0]
        if billing_no == None:
            billing_no = 1
        else:
            billing_no = billing_no + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO paybill(billing_id,parking_id,paid_month,paid_year,amount,paid_date,payment_mode,card_details) VALUES('"+str(billing_no)+"','"+str(pid)+"','"+month+"','"+year+"','"+amount+"','"+str(today)+"','"+mode+"','"+card+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Payment Completed with Receipt ID : "+str(billing_no)+"<br/>Payment done for month : "+str(today)
            data += "<br/>Total Received Amount : "+str(int(amount) + int(tax))
            return render_template('AdminPage.html', output=data)
        else:
            data = "Error in adding payment details"
            return render_template('AdminPage.html', output=data)

@flask_app.route('/Charges', methods=['GET', 'POST'])
def Charges():
    if request.method == 'GET':
        today = datetime.now()
        month = str(today.month)
        year = str(today.year)
        metrics = ['Parking ID', 'Resident ID', 'Vehicle No', 'Parking Slot', 'Parking Amount', 'Parking Type', 'Pay Parking Amount']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from parkingslot")
            rows = cursor.fetchall()
            for row in rows:
                flag = checkPayment(str(row[0]), month, year)
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+str(row[4])+"</font></td>"
                data += "<td>"+font+str(row[5])+"</font></td>"
                if flag == False:
                    data+='<td><a href=\'PayBill?pid='+str(row[0])+'\'><font size=3 color=black>Click Here to Collect Bill</font></a></td></tr>'
                else:
                    data += "<td>"+font+"Payment Done</font></td>"
        return render_template('AdminPage.html', output=data)

################################################################# resident modules

@flask_app.route('/ResidentLoginAction', methods=['GET', 'POST'])
def ResidentLoginAction():
    global uname
    global details
    if request.method == 'POST':
        name = None
        user = request.form['t1']
        status = False
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select resident_id, resident_name from addresident where resident_id='"+str(user)+"'")
            rows = cursor.fetchall()
            for row in rows:
                name = row[1]
                status = True
                break
        if status == True:
            uname = user
            return render_template('ResidentScreen.html', output='You logged in as '+name)
        else:
            return render_template('ResidentLogin.html', output="Invalid login details")   

@flask_app.route('/ResidentProfileUpdate', methods=['GET', 'POST'])
def ResidentProfileUpdate():
    if request.method == 'GET':
        global uname
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addresident where resident_id='"+str(uname)+"'")
            rows = cursor.fetchall()
            for row in rows:
                data = '<tr><td><font size="" color="black">Resident&nbsp;ID</b></td>'
                data += '<td><input type="text" name="t1" style="font-family: Comic Sans MS" size="30" value="'+uname+'" readonly></td></tr>'
                data += '<tr><td><font size="" color="black">Floor&nbsp;No</b></td><td><input name="t2" type="text" size="30" value="'+row[1]+'" readonly></td></tr>'
                data += '<tr><td><font size="" color="black">Door&nbsp;No</b></td><td><input name="t3" type="Text" size="15" value="'+row[2]+'" readonly></td></td></tr>'
                data += '<tr><td><font size="" color="black">Resident&nbsp;Name</b></td><td><input type="text" name="t4" size=50  value="'+row[3]+'"/></td></tr>'
                data += '<tr><td><font size="" color="black">Contact&nbsp;No</b></td><td><input name="t5" type="Text" size="70" value="'+row[4]+'"></td></td></tr>'
                data += '<tr><td><font size="" color="black">Email&nbsp;ID</b></td><td><input name="t6" type="Text" size="70" value="'+row[5]+'"></td></td></tr>'
                data += '<tr><td><font size="" color="black">Aadhar&nbsp;No</b></td><td><input name="t7" type="Text" size="70" value="'+row[6]+'"></td></td></tr>' 
        return render_template('ResidentProfileUpdate.html', output=data)

@flask_app.route('/ResidentProfileUpdateAction', methods=['GET', 'POST'])
def ResidentProfileUpdateAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        floor = request.form['t2']
        door = request.form['t3']
        name = request.form['t4']
        contact = request.form['t5']
        email = request.form['t6']
        aadhar = request.form['t7']
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "update addresident set resident_name='"+name+"', contact_no='"+contact+"', email='"+email+"', aadhar_card='"+aadhar+"' where resident_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        print(db_cursor.rowcount, "Record updated")
        if db_cursor.rowcount == 1:
            data = "Profile updated"            
            return render_template('ResidentScreen.html', output=data)
        else:
            data = "Error in updating profile"
            return render_template('ResidentScreen.html', output=data)

@flask_app.route('/ResidentAddVehicle', methods=['GET', 'POST'])
def ResidentAddVehicle():
    data = '<tr><td><font size="" color="black">Resident&nbsp;ID</b></td><td><select name="t1">'
    data += '<option value="'+str(uname)+'">'+str(uname)+"</option>"
    data += "</select></td></tr>"        
    return render_template('ResidentAddVehicle.html', rid=data)

       
@flask_app.route('/ResidentAddVehicleAction', methods=['GET', 'POST'])
def ResidentAddVehicleAction():
    if request.method == 'POST':
        resident_id = request.form['t1']
        vehicle_no = request.form['t2']
        vehicle_name = request.form['t3']
        vehicle_model = request.form['t4']
        vehicle_id = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(vehicle_id) from addvehicle")
            rows = cursor.fetchall()
            for row in rows:
                vehicle_id = row[0]
        if vehicle_id == None:
            vehicle_id = 1
        else:
            vehicle_id = vehicle_id + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addvehicle(vehicle_id,resident_id,vehicle_no,vehicle_name,vehicle_model) VALUES('"+str(vehicle_id)+"','"+str(resident_id)+"','"+vehicle_no+"','"+vehicle_name+"','"+vehicle_model+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Vehicle detail added with id "+str(vehicle_id)
            return render_template('ResidentAddVehicle.html', output=data)
        else:
            data = "Error in adding vehicle details"
            return render_template('ResidentAddVehicle.html', output=data)  

@flask_app.route('/ResidentUpdateVehicle', methods=['GET', 'POST'])
def ResidentUpdateVehicle():
    if request.method == 'GET':
        global uname
        metrics = ['Vehicle ID', 'Resident ID', 'Vehicle No', 'Vehicle Name', 'Vehicle Model', 'Delete Record', 'Edit Record']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addvehicle where resident_id='"+uname+"'")
            rows = cursor.fetchall()
            for row in rows:
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+row[4]+"</font></td>"
                data+='<td><a href=\'DeleteResidentVehicle?vid='+str(row[0])+'\'><font size=3 color=black>Delete Details</font></a></td>'
                data+='<td><a href=\'UpdateResidentVehicle?vid='+str(row[0])+'\'><font size=3 color=black>Update Details</font></a></td></tr>'   
        return render_template('ResidentUpdateVehicle.html', output=data)

@flask_app.route('/UpdateResidentVehicleAction', methods=['GET', 'POST'])
def UpdateResidentVehicleAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        vehicle_no = request.form['t2']
        name = request.form['t3']
        model = request.form['t4']
        vid = request.form['vid']
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addvehicle where vehicle_id='"+vid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO addvehicle(vehicle_id,resident_id,vehicle_no,vehicle_name,vehicle_model) VALUES('"+str(vid)+"','"+str(rid)+"','"+vehicle_no+"','"+name+"','"+model+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Vehicle detail updated with id "+str(vid)
            return render_template('ResidentScreen.html', output=data)
        else:
            data = "Error in updating vehicle details"
            return render_template('ResidentScreen.html', output=data) 


@flask_app.route('/DeleteResidentVehicle', methods=['GET', 'POST'])
def DeleteResidentVehicle():
    if request.method == 'GET':
        rid = request.args.get('vid')
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "delete from addvehicle where vehicle_id='"+rid+"'" 
        db_cursor.execute(query)
        db_connection.commit()
        data = "Error in deleting details"
        if db_cursor.rowcount == 1:
            data = 'Vehicle Details Deleted'
        return render_template('ResidentScreen.html', output=data)

@flask_app.route('/UpdateResidentVehicle', methods=['GET', 'POST'])
def UpdateResidentVehicle():
    if request.method == 'GET':
        rid = request.args.get('vid')
        font = '<font size="" color="black">'
        details = '<form name ="f1" method="post" action="/UpdateResidentVehicleAction" onsubmit="return validate(this);"><table align="center" width=30%>'
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from addvehicle where vehicle_id='"+rid+"'")
            rows = cursor.fetchall()
            for row in rows:
                details += '<tr><td><font size="" color="black">Vehicle ID</b></td><td><input name="vid" type="text" size="15" value="'+str(row[0])+'" readonly></td></tr>'
                details += '<tr><td><font size="" color="black">Resident ID</b></td><td><input name="t1" type="text" size="15" value="'+row[1]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;No</b></td><td><input name="t2" type="text" size="15" value="'+row[2]+'"></td></tr>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;Name</b></td><td><input name="t3" type="Text" size="15" value="'+row[3]+'"></td></td>'
                details += '<tr><td><font size="" color="black">Vehicle&nbsp;Model</b></td><td><input name="t4" type="Text" size="15" value="'+row[4]+'"></td></td></tr>'
                
        details += '<tr><td></td><td><input type="submit" value="Submit"></td></table>'        
        return render_template('ResidentUpdateVehicle.html', output=details)

@flask_app.route('/ResidentComplaints', methods=['GET', 'POST'])
def ResidentComplaints():
    data = '<tr><td><font size="" color="black">Resident&nbsp;ID</b></td><td><select name="t1">'
    data += '<option value="'+str(uname)+'">'+str(uname)+"</option>"
    data += "</select></td></tr>"        
    return render_template('ResidentComplaints.html', rid=data)

@flask_app.route('/ResidentComplaintsAction', methods=['GET', 'POST'])
def ResidentComplaintsAction():
    if request.method == 'POST':
        global details
        rid = request.form['t1']
        complaint = request.form['t2']
        today = datetime.now()
        
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO complaints(resident_id,complaints,complaint_date) VALUES('"+str(rid)+"','"+str(complaint)+"','"+str(today)+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Your complaint sent to admin"
            return render_template('ResidentComplaints.html', output=data)
        else:
            data = "Error in adding complaint details"
            return render_template('ResidentComplaints.html', output=data)

#=====================================================resident charges
@flask_app.route('/ResidentPayBill', methods=['GET', 'POST'])
def ResidentPayBill():
    if request.method == 'GET':
        pid = request.args.get('pid')
        font = '<font size="" color="black">'
        details = '<tr><td><font size="" color="black">Parking ID</b></td><td><input name="t1" type="text" size="15" value="'+str(pid)+'" readonly></td></tr>'
        return render_template('ResidentPayBill.html', bill=details)    

@flask_app.route('/ResidentPayBillAction', methods=['GET', 'POST'])
def ResidentPayBillAction():
    if request.method == 'POST':
        pid = request.form['t1']
        amount = request.form['t2']
        tax = request.form['t3']
        mode = request.form['t4']
        card = request.form['t5']
        today = datetime.now()
        month = str(today.month)
        year = str(today.year)
        billing_no = 0
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select max(billing_id) from paybill")
            rows = cursor.fetchall()
            for row in rows:
                billing_no = row[0]
        if billing_no == None:
            billing_no = 1
        else:
            billing_no = billing_no + 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        db_cursor = db_connection.cursor()
        query = "INSERT INTO paybill(billing_id,parking_id,paid_month,paid_year,amount,paid_date,payment_mode,card_details) VALUES('"+str(billing_no)+"','"+str(pid)+"','"+month+"','"+year+"','"+amount+"','"+str(today)+"','"+mode+"','"+card+"')"
        db_cursor.execute(query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            data = "Payment Completed with Receipt ID : "+str(billing_no)+"<br/>Payment done for month : "+str(today)
            data += "<br/>Total Received Amount : "+str(int(amount) + int(tax))
            return render_template('ResidentScreen.html', output=data)
        else:
            data = "Error in adding payment details"
            return render_template('ResidentScreen.html', output=data)

@flask_app.route('/ResidentCharges', methods=['GET', 'POST'])
def ResidentCharges():
    if request.method == 'GET':
        global uname
        today = datetime.now()
        month = str(today.month)
        year = str(today.year)
        metrics = ['Parking ID', 'Resident ID', 'Vehicle No', 'Parking Slot', 'Parking Amount', 'Parking Type', 'Pay Parking Amount']
        data = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        data += "<tr>"
        for i in range(len(metrics)):
            data += "<th>"+font+metrics[i]+"</th>"
        mysql_connect = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'parking',charset='utf8')
        with mysql_connect:
            cursor = mysql_connect.cursor()
            cursor.execute("select * from parkingslot where resident_id='"+uname+"'")
            rows = cursor.fetchall()
            for row in rows:
                flag = checkPayment(str(row[0]), month, year)
                data += "<tr><td>"+font+str(row[0])+"</font></td>"
                data += "<td>"+font+row[1]+"</font></td>"
                data += "<td>"+font+row[2]+"</font></td>"
                data += "<td>"+font+row[3]+"</font></td>"
                data += "<td>"+font+str(row[4])+"</font></td>"
                data += "<td>"+font+str(row[5])+"</font></td>"
                if flag == False:
                    data+='<td><a href=\'ResidentPayBill?pid='+str(row[0])+'\'><font size=3 color=black>Click Here to Collect Bill</font></a></td></tr>'
                else:
                    data += "<td>"+font+"Payment Done</font></td>"
        return render_template('ResidentScreen.html', output=data)
        

if __name__ == '__main__':
    flask_app.run(host='localhost', port=7000)










