

import requests
from flask import Flask, render_template, url_for, jsonify, request, redirect, session, flash, Response, make_response
from datetime import datetime
from flask_mail import Mail, Message
from cv2 import cv2
import base64
from flask_mysqldb import MySQL

import os

from imageio.core.functions import si
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'attendancesystem'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'chintandarji0712@gmail.com'
app.config['MAIL_PASSWORD'] = '********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)
mysql = MySQL(app)







#courseid=''

import csv
from datetime import datetime
#from app import courseid
import cv2
import face_recognition
import os
import numpy as np
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
ds_factor=0.6
filename=''

class VideoCamera(object):
    #courseid=''
    def __init__(self):

        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    path = 'E:/flask_demo/static/images'
    images = []

    classNames = []
    myList = os.listdir(path)
    # print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)



    def get_frame(self):
        success, image = self.video.read()
        image=cv2.resize(image,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        face_rects=face_cascade.detectMultiScale(gray,1.3,5)

        imgS = cv2.resize(image, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(VideoCamera.encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(VideoCamera.encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = VideoCamera.classNames[matchIndex].upper()
                print(name)
                for (x,y,w,h) in face_rects:
                    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
                    cv2.putText(image, name, (x + 6, (y+h) - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    break
                markAttendance(name)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

#obj=VideoCamera()
#courseid=fgetcourseid()
def markAttendance(name):
    #csv.DictWriter(result.csv, )
    global filename
    print(filename)
    with open('C:/xampp/htdocs/attendance/'+filename, 'r+') as f:
        dataList = f.readlines()
        nameList = []

        for line in dataList:
            entry = line.split(',')
            nameList.append(entry[0])
            print(nameList)
        if name not in nameList:
            now = datetime.now()
            dt = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dt}')







@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/login",methods=["GET","POST"])
def login():
    return render_template('login.html')

@app.route("/forgetpassword",methods=["GET","POST"])
def forgetpassword():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['m_email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  password FROM logindata WHERE username=%s ",
                    (username,))
        mypassword= cur.fetchone()


        cur = mysql.connection.cursor()
        cur.execute("SELECT  emailid FROM studentdetails WHERE username=%s ",
                    (username,))
        myemail = cur.fetchone()
        m1=myemail[0]

        print(myemail[0])
        print(email)


        if email==m1:
            msg = Message('Hello', sender='chintandarji0712@gmail.com', recipients=[m1])
            msg.body = "Hello"+str(username)+"your password is"+str(mypassword[0])
            mail.send(msg)
            return redirect(url_for('login'))
        else:
            return 'please Enter Valid Email and Username'








@app.route("/user",methods=["GET","POST"])
def user():

    if request.method=="POST":
        username=request.form['username']
        password=request.form['password']
        role=request.form['role']
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM logindata WHERE username=%s AND password=%s AND role=%s",(username,password,role))
        data = cur.fetchone()
        cur.close()
        if data:
            session['loggedin'] = True
            session['username']=username
            session['role']=role
            session['password']=password
            return redirect(url_for('show'))

        else:
            return 'invalid username/password try again'
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username',None)
    session.pop('role',None)
    return redirect(url_for('login'))
@app.route('/show')
def show():
    if 'loggedin' in session:
        role=session.get('role')
        if role=='student':
            username = session.get('username')
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM studentdetails WHERE username=%s ",
                        (username,))
            data = cur.fetchone()

            cur.close()


            return render_template('student.html',username=session.get('username'),data=data)
        elif role=='faculty':
            username = session.get('username')
            cur = mysql.connection.cursor()
            cur.execute("SELECT  * FROM facultydetails WHERE username=%s ",
                        (username,))
            data = cur.fetchone()

            cur.close()
            cur = mysql.connection.cursor()
            cur.execute("SELECT courseid FROM coursedetails WHERE facultyname=%s ",
                        (username,))
            data1 = cur.fetchall()
            cur.close()

            return render_template('faculty.html', username=session.get('username'),data=data,data1=data1)
        elif role=='admin':
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM studentdetails")
                data = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM facultydetails")
                fdata = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT  * FROM coursedetails")
                fdata1 = cur.fetchall()
                cur.close()
                cur = mysql.connection.cursor()
                cur.execute("SELECT username FROM facultydetails")
                fdata2 = cur.fetchall()
                cur.close()

                return render_template('admin.html', username=session.get('username'),students=data,facultys=fdata,coursedetail=fdata1,fdata2=fdata2)
            #return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))



@app.route('/studentupdate', methods=["GET","POST"])
def studentupdate():
    if 'loggedin' in session:
        if session.get('role')=='student':
            if request.method == 'POST':

                emailid = request.form['emailid']
                batch = request.form['batch']
                dob=request.form['dob']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE studentdetails
                       SET emailid=%s, batch=%s, dob=%s 
                       WHERE username=%s
                    """, (emailid, batch,dob,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as student'
    else:
        return 'please first login'

@app.route('/studentchangepassword', methods=["GET","POST"])
def studentchangepassword():
    if 'loggedin' in session:
        if session.get('role')=='student':
            if request.method == 'POST':

                password=request.form['password']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as student'
    else:
        return 'please first login'

@app.route('/facultyupdate', methods=["GET","POST"])
def facultyupdate():
    if 'loggedin' in session:
        role=session.get('role')
        if role=='faculty':
            if request.method == 'POST':
                email = request.form['email']
                phno=request.form['phno']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE facultydetails
                       SET email=%s, ph_no=%s
                       WHERE username=%s
                    """, (email, phno,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as faculty'
@app.route('/facultychangepassword', methods=["GET","POST"])
def facultychangepassword():
    if 'loggedin' in session:
        if session.get('role')=='faculty':
            if request.method == 'POST':

                password=request.form['password']
                username = session.get('username')
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as faculty'
    else:
        return 'please first login'


@app.route('/update',methods=['POST','GET'])
def update():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                batch = request.form['batch']
                emailid = request.form['emailid']
                dob= request.form['dob']
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE studentdetails
                       SET  batch=%s,
                       emailid=%s, dob=%s
                       WHERE username=%s
                    """, (batch,emailid,dob,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as a admin'




@app.route('/fupdate',methods=['POST','GET'])
def fupdate():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                ph_no= request.form['ph_no']
                cur = mysql.connection.cursor()
                cur.execute("""
                       UPDATE facultydetails
                       SET  email=%s,
                         ph_no=%s
                       WHERE username=%s
                    """, (email,ph_no,username))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as a admin'

@app.route('/insert',methods=['POST','GET'])
def insert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                batch = request.form['batch']
                emailid = request.form['emailid']
                dob = request.form['dob']
                img=request.files['img']


                img.save(os.path.join('./static/images',img.filename))
                os.rename('E:/flask_demo/static/images/'+img.filename, 'E:/flask_demo/static/images/'+username +'.jpg')
                password=request.form['password']
                role='student'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into studentdetails (username,batch, emailid, dob) VALUES (%s, %s, %s,%s)
                    """, (username,batch, emailid, dob))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                cur.execute("""
                                       insert into logindata (username,password,role) VALUES (%s, %s, %s)
                                    """, (username, password,role))
                mysql.connection.commit()

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'

@app.route('/finsert',methods=['POST','GET'])
def finsert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                phno = request.form['phno']
                password=request.form['password']
                role='faculty'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into facultydetails (username,email,ph_no) VALUES (%s, %s, %s)
                    """, (username,email, phno))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                cur = mysql.connection.cursor()
                cur.execute("""
                                       insert into logindata (username,password,role) VALUES (%s, %s, %s)
                                    """, (username, password,role))
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'


@app.route('/cinsert',methods=['POST','GET'])
def cinsert():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                courseid = request.form['courseid']
                faculty = request.form['faculty']
                #print(courseid)
                #role='faculty'
                cur = mysql.connection.cursor()
                cur.execute("""
                       insert into coursedetails (courseid,facultyname) VALUES (%s, %s)
                    """, (courseid,faculty,))
                mysql.connection.commit()

                flash("Data Updated Successfully")

                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'

@app.route('/cupdate',methods=['POST','GET'])
def cupdate():
    if 'loggedin' in session:
        if session.get('role')=='admin':
            if request.method == 'POST':
                courseid=request.form['courseid']
                facultyname=request.form['facultyname']
                cur = mysql.connection.cursor()
                cur.execute("""
                                       UPDATE coursedetails
                                       SET  facultyname=%s
                                         
                                       WHERE courseid=%s
                                    """, (facultyname, courseid))
                flash("Data Updated Successfully")
                mysql.connection.commit()
                return redirect(url_for('show'))
            else:
                return 'form bhari ne aavo'
        else:
            return 'please login as admin'




@app.route('/delete/<string:username>', methods=['GET'])
def delete(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM studentdetails WHERE username=%s", (username,))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM logindata WHERE username=%s", (username,))
            mysql.connection.commit()
            os.remove('E:/flask_demo/static/images/'+username+'.jpg')

            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/fdelete/<string:username>', methods=['GET'])
def fdelete(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM facultydetails WHERE username=%s", (username,))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/cdelete/<string:coursename>', methods=['GET'])
def cdelete(coursename):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            flash("Record Has Been Deleted Successfully")
            cur = mysql.connection.cursor()
            cur.execute("DELETE FROM coursedetails WHERE courseid=%s", (coursename,))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'


@app.route('/resetpassword/<string:username>', methods=['GET'])
def resetpassword(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            password='123'
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password, username))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/fresetpassword/<string:username>', methods=['GET'])
def fresetpassword(username):
    if 'loggedin' in session:
        if session.get('role')=='admin':
            password='123'
            cur = mysql.connection.cursor()
            cur.execute("""UPDATE logindata
                       SET password=%s
                       WHERE username=%s
                    """, (password, username))
            mysql.connection.commit()
            return redirect(url_for('show'))
        else:
            return 'form bhari ne aavo'
    else:
        return 'please login as admin'

@app.route('/viewattendance',methods=['POST'])
def viewattendance():

    if 'loggedin' in session:

        if session.get('role')=='faculty':
            if request.method == 'POST':
                cid=request.form['cid']
                vdate=request.form['date']
                d1 = datetime.strptime(vdate, '%Y-%m-%d')
                mydate=d1.strftime('%b-%d-%Y')
                global fname
                fname=cid+'_'+mydate+'.csv'
                global myurl
                myurl='http://localhost/attendance/'+fname
                print(myurl)
                req = requests.get(myurl)
                url_content = req.content
                csv_file = open(fname, 'wb')
                print(type(csv_file))
                csv_file.write(url_content)
                csv_file.close()
                return redirect(myurl)

@app.route('/takeattendance', methods=['POST'])
def takeattendance():

    if 'loggedin' in session:

        if session.get('role')=='faculty':
            if request.method == 'POST':
                global courseid
                courseid = request.form['courseid']

                return render_template('index.html')
        else:
            return 'only faculty can take attendance'

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    if 'loggedin' in session:
        if session.get('role')=='faculty':


            today = datetime.today()

            d3 = today.strftime("%m/%d/%y")
            d4 = today.strftime("%b-%d-%Y")
            now = datetime.now()
            dt_string = now.strftime("%H-%M-%S")
            x = str(datetime.today())
            global filename
            filename = courseid + '_' + d4 + '.csv'
            # filename.replace(" ", "")

            with open('C:/xampp/htdocs/attendance/' + filename, 'w') as f:
                pass

            return Response(gen(VideoCamera()),
                            mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
