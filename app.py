from flask import Flask, render_template, request
import pymysql
from datetime import datetime

flask_app = Flask(__name__)
flask_app.secret_key = 'parking'

global uname, details

# ================= ADMIN RESIDENT MODULE =================

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

        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
        cur = conn.cursor()

        cur.execute("delete from addresident where resident_id='"+resident_id+"'")
        conn.commit()

        cur.execute("INSERT INTO addresident VALUES('"+resident_id+"','"+floor+"','"+door+"','"+name+"','"+contact+"','"+email+"','"+aadhar+"','Current Resident')")
        conn.commit()

        if cur.rowcount == 1:
            return render_template('AdminPage.html', output="Resident updated")
        return render_template('AdminPage.html', output="Error updating resident")


@flask_app.route('/DeleteAdminResident')
def DeleteAdminResident():
    rid = request.args.get('rid')
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()
    cur.execute("delete from addresident where resident_id='"+rid+"'")
    conn.commit()
    return render_template('AdminPage.html', output="Deleted Resident")


@flask_app.route('/UpdateAdminResident')
def UpdateAdminResident():
    rid = request.args.get('rid')

    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()
    cur.execute("select * from addresident where resident_id='"+rid+"'")
    row = cur.fetchone()

    details = f"""
    <form method="post" action="/UpdateResidentDetailsAction">
    <input name="rid" value="{row[0]}" readonly><br>
    <input name="t1" value="{row[1]}"><br>
    <input name="t2" value="{row[2]}"><br>
    <input name="t3" value="{row[3]}"><br>
    <input name="t4" value="{row[4]}"><br>
    <input name="t5" value="{row[5]}"><br>
    <input name="t6" value="{row[6]}"><br>
    <input type="submit">
    </form>
    """
    return render_template('UpdateResidentDetails.html', output=details)


@flask_app.route('/UpdateResidentDetails')
def UpdateResidentDetails():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()
    cur.execute("select * from addresident")
    rows = cur.fetchall()

    data = "<table border=1>"
    for r in rows:
        data += f"<tr><td>{r}</td></tr>"
    data += "</table>"

    return render_template('UpdateResidentDetails.html', output=data)


@flask_app.route('/AddResident')
def AddResident():
    return render_template('AddResident.html')


@flask_app.route('/AdminPage')
def AdminPage():
    return render_template('AdminPage.html')


# ================= LOGIN =================

def isUserExists(table, username, password):
    global details
    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()

    cur.execute("select * from "+table+" where username='"+username+"' and password='"+password+"'")
    row = cur.fetchone()

    if row:
        details = ",".join(map(str, row))
        return True
    return False


@flask_app.route('/AdminLoginAction', methods=['POST'])
def AdminLoginAction():
    global uname
    user = request.form['t1']
    password = request.form['t2']

    if isUserExists("admin", user, password):
        uname = user
        return render_template('AdminPage.html', output="Welcome Admin")
    return render_template('AdminLogin.html', output="Invalid Login")


# ================= ADD RESIDENT =================

@flask_app.route('/AddResidentAction', methods=['POST'])
def AddResidentAction():
    floor = request.form['t1']
    door = request.form['t2']
    name = request.form['t3']
    contact = request.form['t4']
    email = request.form['t5']
    aadhar = request.form['t6']

    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()

    cur.execute("select max(resident_id) from addresident")
    row = cur.fetchone()

    rid = 1 if row[0] is None else int(row[0]) + 1

    cur.execute("INSERT INTO addresident VALUES('"+str(rid)+"','"+floor+"','"+door+"','"+name+"','"+contact+"','"+email+"','"+aadhar+"','Current Resident')")
    conn.commit()

    return render_template('AddResident.html', output="Resident Added")


# ================= VEHICLE MODULE (SAMPLE) =================

@flask_app.route('/AddVehicle')
def AddVehicle():
    return render_template('AddVehicle.html')


@flask_app.route('/AddVehicleAction', methods=['POST'])
def AddVehicleAction():
    rid = request.form['t1']
    vno = request.form['t2']
    vname = request.form['t3']
    vmodel = request.form['t4']

    conn = pymysql.connect(host='127.0.0.1', user='root', password='root', database='parking')
    cur = conn.cursor()

    cur.execute("select max(vehicle_id) from addvehicle")
    row = cur.fetchone()

    vid = 1 if row[0] is None else int(row[0]) + 1

    cur.execute("INSERT INTO addvehicle VALUES('"+str(vid)+"','"+rid+"','"+vno+"','"+vname+"','"+vmodel+"')")
    conn.commit()

    return render_template('AddVehicle.html', output="Vehicle Added")


# ================= MAIN =================

if __name__ == '__main__':
    flask_app.run(host='localhost', port=7000, debug=True)
