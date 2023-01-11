import os
import matplotlib.image as mpimg
from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
from flask import send_file
import pathlib
import numpy as np

from PIL import Image, ImageTk
import pandas as pd
import sqlite3
import MySQLdb
import OCRtextretrival as ocr
import subjective as sc

import matplotlib.pyplot as plt
import csv
from PIL import Image
import io
import random as r
import pyotp

# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# from torchvision import datasets, transforms, models
# import pickle
import time
import json
from werkzeug.utils import secure_filename
import sendMail as ms

UPLOAD_FOLDER = './input'
mydb = MySQLdb.connect(host='localhost',user='root',passwd='Ghanavi@1',db='onlineexam')
conn = mydb.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png'])
socketio = SocketIO(app)
otp="0000"
totp = pyotp.TOTP('base32secret3232')

def otpgen():
        otp=""
        for i in range(4):
                otp+=str(r.randint(1,9))
        print ("Your One Time Password is ")
        print (otp)
        return otp
@app.route('/')
def index():
        if not session.get('logged_in'):
                return render_template("login.html")
        else:
                cmd="SELECT qid FROM quest"
                print(cmd)
                results=[]
                conn.execute(cmd)
                data=conn.fetchall()
                
                for row in data:
                        print(row)
                        results.append(row[0])
                print("data",results)
                return render_template('home1.html',data=results)
@app.route('/forgetpasspage',methods=['POST'])
def fpass_page():
    return render_template("forgetpass.html")
@app.route('/fpass',methods=['POST'])
def fpass_in():
        global otp
        #complete login if name is not an empty string or doesnt corss with any names currently used across sessions
        if request.form['username'] != None and request.form['username'] != "" and request.form['email'] != None and request.form['email'] != "":
                cid=request.form['username']
                pin=request.form['email']
                cmd="SELECT rollno,email FROM student WHERE rollno='"+cid+"'"
                print(cmd)
                conn.execute(cmd)
                cursor=conn.fetchall()
                isRecordExist=0
                for row in cursor:
                        isRecordExist=1
                        
                if(isRecordExist==1):
                        email=row[1]
                        results=[]
                        results.append(cid)
                        results.append(pin)
                        print(otp)
                        otp=totp.now()
                        print(otp)
                        print("Email==",email)
                        msg="Your Otp Number Is " + otp
                        ms.process(email,"OTP",msg)
                        return render_template("otp1.html",results=results)
                else:
                        return render_template("forgetpass.html",message="Check Rollnumber and Email id")

        return redirect(url_for('index'))
@app.route('/fpass1',methods=['POST'])
def fpass_in1():
        global otp
        otpvalue=request.form['otp']
        print(otp)
        print(otpvalue)
        if otp==otpvalue:
                results=[]
                #session['logged_in'] = True
                session['cid'] = request.form['username']
                cid=request.form['username']
                results.append(cid)
                return render_template("changepin.html",results=results)
        else:
                return render_template("forgetpass.html",message="Check OTP Value")
@app.route('/changepin',methods=['POST'])
def upatepin():
        #name=request.form['name']
        cid=request.form['username']
        pin=request.form['pin']
        cpin=request.form['cpin']
        #mobile=request.form['mobile']
        cmd="SELECT * FROM student WHERE rollno='"+cid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Username Already Exists")
                cmd="UPDATE student SET pass='"+str(pin)+"'WHERE rollno='"+cid+"'"
                print(cmd)
                print("Inserted Successfully")
                
                conn.execute(cmd)
                mydb.commit()
                return render_template("login.html",message="PIN Updated")
                
        else:
                return render_template("forgetpass.html",message="Client id not Exist")
@app.route('/registerpage',methods=['POST'])
def reg_page():
    return render_template("register.html")
        
@app.route('/loginpage',methods=['POST'])
def log_page():
    return render_template("login.html")
@app.route('/sloginpage',methods=['POST'])
def slog_page():
    return render_template("slogin.html")
@app.route('/questionpage',methods=['POST'])
def quest_page():
    return render_template("addquestion.html")
@app.route('/Back')
def back():
        
        cmd="SELECT qid FROM quest"
        print(cmd)
        conn.execute(cmd)
        data=conn.fetchall()
        return render_template("home1.html",data=data)
    
@app.route('/search',methods=['POST'])
def seach():
        qid=request.form['qestid'] 
        print("Qid=",qid)
        qid=qid.replace('(','')
        qid=qid.replace(',','')
        qid=qid.replace(')','')
        print("new qid==",qid)
        cmd="SELECT * FROM quest WHERE qid='"+qid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                results=[]
                for row in cursor:
                        print(row)
                        results.append(row[0])
                        results.append(row[1])
                        results.append(row[2])
                        results.append(row[3])
                print(results)
                return render_template("home.html",data=results)
        else:
                cmd="SELECT qid FROM quest "
                print(cmd)
                conn.execute(cmd)
                data=conn.fetchall()
                return render_template("home1.html",data=results)
                
@app.route('/addquest',methods=['POST'])
def qadd():
        qid=request.form['qid']
        quest=request.form['quest']
        ans=request.form['ans']
        mr=request.form['qm']
        cmd="SELECT * FROM quest WHERE qid='"+qid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                cmd="SELECT name,rollno FROM student"
                print(cmd)
                conn.execute(cmd)
                data=conn.fetchall()
                return render_template("adminhome.html",data=data) 
                #return render_template("adminhome.html")
        else:
                cmd="INSERT INTO quest(qid,quest,answer,mark) Values('"+str(qid)+"','"+str(quest)+"','"+str(ans)+"','"+str(mr)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()
                #conn.close()
                cmd="SELECT name,rollno FROM student"
                print(cmd)
                conn.execute(cmd)
                data=conn.fetchall()
                return render_template("adminhome.html",data=data)  
                #return render_template("adminhome.html")


@app.route('/register',methods=['POST'])
def reg():
        name=request.form['name']
        rollno=request.form['rollno']
        password=request.form['password']
        dept=request.form['dept']
        sem=request.form['sem']
        email=request.form['emailid']
        mobile=request.form['mobile']
        addr=request.form['addr']
        
        cmd="SELECT * FROM student WHERE rollno='"+rollno+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Rollno Already Exists")
                return render_template("usernameexist.html")
        else:
                print("insert")
                cmd="INSERT INTO student(rollno,name,dept,sem,mono,email,addr,pass) Values('"+str(rollno)+"','"+str(name)+"','"+str(dept)+"','"+str(sem)+"','"+str(mobile)+"','"+str(email)+"','"+str(addr)+"','"+str(password)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()
                #conn.close() 
                return render_template("inserted.html")


@app.route('/finalevaluvation/<text>,<qid>,<rollno>')
def finalevaluvation(text,qid,rollno):
        total_score=0.0
        scoreforaquest=0.0
        print("text==",text)
        print("qid==",qid)
        cmd="SELECT answer FROM quest where qid='"+qid+"'"
        print(cmd)
        conn.execute(cmd)
        data=conn.fetchall()
        total_score += sc.process(str(data), text)
        print("Total score for this text==",total_score)
        #total_score /= 2
        cmd="SELECT mark FROM quest where qid='"+qid+"'"
        print(cmd)
        conn.execute(cmd)
        data1=conn.fetchall()
        actualmark=data1
        print("Actual mark==",actualmark[0])
        am=int(''.join(map(str, actualmark[0])))
        print("am==",am)
        
        total_score = round(total_score, 3)
        
        if total_score > 40.0:
                scoreforaquest=am
                status = "Pass"
        elif total_score > 30.0 and total_score<40.0 :
                scoreforaquest=am/2
                status = "Pass"
        elif total_score > 20.0 and total_score<30.0 :
                scoreforaquest=am/3
                status = "Pass"
        else:
                scoreforaquest=0.0
                status = "Fail"
        print("Score for Question 1=",total_score)
        print("Result=",status)
        session["score"] = str(np.round(scoreforaquest, decimals=2))
        session["result"] = status
        mark=np.round(scoreforaquest, decimals=2)
        mark=mark.item()
        qid=str(qid)
        print("mark==",mark)
        cmd="SELECT * FROM result WHERE rollno='"+rollno+"' and qid='"+qid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Already Score Calculated")
                cmd="SELECT name,rollno FROM student"
                print(cmd)
                conn.execute(cmd)
                data=conn.fetchall()
                message="Already evaluated for this question id: "+str(qid)
                return render_template("adminhome.html",data=data,message=message)
                #return render_template("adminhome.html")
        else:
                print("insert")
                result=[]
                cmd="INSERT INTO result(rollno,qid,mark) Values('"+str(rollno)+"','"+str(qid)+"','"+str(mark)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()
                result.append(str(qid))
                result.append(str(mark))
                result.append(str(rollno))
                print("Iam going to redirect to score.html")
                return render_template("score.html", result=result)

@app.route('/viewmark',methods=['GET', 'POST'])
def view_mark():
        urollno=session['username']
        cmd="SELECT qid,mark FROM result where rollno='"+urollno+"'"
        print(cmd)
        conn.execute(cmd)
        data=conn.fetchall()
        return render_template("yourmarks.html",text=data,rollno=urollno)


@app.route('/evaluvation/<rollno>,<qid>')
def evaluvation(rollno,qid):
        print("rollno==",rollno)
        print("qid==",qid)
        path="input//"+rollno+"//"+qid
        print("image path=",path)
        textdata=ocr.process(path)
        print("Extracted Text==",textdata)
        return render_template("extractedtext.html",text=textdata,qid1=qid,rollno=rollno)

@app.route('/fcalc',methods=['POST'])
def finalscore():
        user=session['username']
        cmd="SELECT SUM(MARK) FROM result where rollno='"+user+"'"
        print(cmd)
        conn.execute(cmd)
        mark=conn.fetchall()
        print("Final mark===",mark)
        cmd="SELECT COUNT(*) FROM result where rollno='"+user+"'"
        print(cmd)
        conn.execute(cmd)
        n=conn.fetchall()
        print("n==",n)
        m=n[0]
        ms=mark[0]
        print("m==",m)
        print("ms==",ms)
        totalmarks=ms[0]
        print("total marks==",totalmarks)

        return render_template("score1.html",fnalmark=totalmarks,rollno=user)

@app.route('/evaluvate/<rollno>')
def evaluvate(rollno):
        print("rollno==",rollno)
        user=rollno
        cmd="SELECT qid FROM student_upload where rollno='"+rollno+"'"
        print(cmd)
        conn.execute(cmd)
        data=conn.fetchall()

        return render_template("evaluationpage.html",data=data,user1=rollno)
        
@app.route('/login',methods=['POST'])
def log_in():
        #complete login if name is not an empty string or doesnt corss with any names currently used across sessions
        if request.form['username'] != None and request.form['username'] != "" and request.form['password'] != None and request.form['password'] != "":
                username=request.form['username']
                password=request.form['password']
                if username=="admin" and password=="Admin@001":
                        session['username'] = request.form['username']
                        cmd="SELECT name,rollno FROM student"
                        print(cmd)
                        conn.execute(cmd)
                        data=conn.fetchall()
                        return render_template("adminhome.html",data=data) 
                else:
                        
                        cmd="SELECT name,pass FROM student WHERE rollno='"+username+"' and pass='"+password+"'"
                        print(cmd)
                        conn.execute(cmd)
                        cursor=conn.fetchall()
                        isRecordExist=0
                        
                        for row in cursor:
                                isRecordExist=1
                        if(isRecordExist==1):
                                session['logged_in'] = True
                                # cross check names and see if name exists in current session
                                session['username'] = request.form['username']
                                return redirect(url_for('index'))
                        else:
                                return redirect(url_for('index'))
                       # return redirect(url_for('index'))
        
@app.route("/logout",methods=['POST'])
def log_out():
    session.clear()
    return render_template("login.html")
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/answerupload', methods=['GET', 'POST'])
def segment_file():
        uname= session['username']
        path=""
        qid=""
        
        if request.method == 'POST':
                qid=request.form['qid']
                print("qid==",qid)
                #path=request.form['imf']
                #print("Path==",path)
                if 'imf' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                file = request.files['imf']
                if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        path=uname
                        pathlib.Path(app.config['UPLOAD_FOLDER'], path).mkdir(exist_ok=True)
                        pathlib.Path(app.config['UPLOAD_FOLDER'], path,qid).mkdir(exist_ok=True)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'],path,qid,filename))
                cmd="INSERT INTO student_upload(rollno,qid) Values('"+str(uname)+"','"+str(qid)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()

        
        
        return render_template("result.html",class_name="Your Answer Uploaded")
        
        
@app.route('/download', methods=['POST'])
def download_file():
        path=""
        uname= session['patname']
        print("uname==",uname)
        path=str(uname)+"result.pdf"
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
