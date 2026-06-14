from flask import Flask, json, redirect, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_login import LoginManager
from flask.globals import request, session
import json
import os

# Configure Flask to use project templates and static assets
app = Flask(__name__, 
    static_folder=os.path.join(os.path.dirname(__file__), 'templates', 'static'),
    static_url_path='/static',
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'))
app.secret_key="prabhatpraveen"

# Database configuration - supports SQLite by default, MySQL via DATABASE_URL env var
db_url = os.environ.get('DATABASE_URL')
if db_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    # Default to SQLite for local development
    db_path = os.path.join(os.path.dirname(__file__), '..', 'lab.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Authentication
login_manager = LoginManager(app)
login_manager.login_view = 'login' 


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(config_path, 'r') as c:
    params=json.load(c)["params"]

@login_manager.user_loader
def load_user(user_id):
    return Teacher.query.get(int(user_id)) or Student.query.get(int(user_id))


class Teacher(UserMixin, db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(100))
    sub_code = db.Column(db.String(10))
    sub_name = db.Column(db.String(100))
    dob = db.Column(db.String(1000))
    batches = db.relationship('Batch', backref='teacher', lazy=True)
    experiments = db.relationship('Experiment', backref='teacher', lazy=True)

class Batch(db.Model):
    b_id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    time_in = db.Column(db.String(20))
    time_out = db.Column(db.String(20))
    t_id = db.Column(db.Integer, db.ForeignKey('teacher.t_id'))
    students = db.relationship('Student', backref='batch', lazy=True)

class System(db.Model):
    sys_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50))
    students = db.relationship('Student', backref='system', lazy=True)

class Student(UserMixin, db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(100))
    dob = db.Column(db.String(1000))
    b_id = db.Column(db.Integer, db.ForeignKey('batch.b_id'))
    sys_id = db.Column(db.Integer, db.ForeignKey('system.sys_id'))
    email = db.Column(db.String(100))

class Experiment(db.Model):
    e_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    doe = db.Column(db.String(50))
    t_id = db.Column(db.Integer, db.ForeignKey('teacher.t_id'))

# Initialize database on startup
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        if(username==params['user'] and password==params['password']):
            session['user']=username
            flash("login success","success")
            return redirect("/admin")
        else:
            flash("wrong input","danger")
    return render_template("adminlogin.html")


@app.route('/addsystem',methods=['POST','GET'])
def addsystem():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            sys_id=request.form.get('sys_id')
            sat=request.form.get('status')
            checkid=System.query.filter_by(sys_id=sys_id).first()
            print(checkid)
            if checkid :
                flash("System already exist in Database","warning")
                return render_template("addsystem.html")
            else:
                checkid=db.engine.execute(f"INSERT INTO `system` (`sys_id`,`status`) VALUES ('{sys_id}','{sat}') ")
                flash("Data Added Successfully","success")
                return render_template("admin.html")
        else:
            flash("Add data","success")
            return render_template("addsystem.html")

@app.route('/addteacher',methods=['POST','GET'])
def addteacher():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            tid=request.form.get('t_id')
            tname=request.form.get('tname')
            subcode=request.form.get('sub_code')
            subname=request.form.get('sub_name')
            dob=request.form.get('dob')
            nuser=Teacher.query.filter_by(t_id=tid).first()
            print(nuser)
            if nuser :
                flash("Teacher already exist in Database","warning")
                return render_template("admin.html")
            else:
                nuser=db.engine.execute(f"INSERT INTO `teacher` (`t_id`,`t_name`,`sub_code`,`sub_name`,`dob`) VALUES ('{tid}','{tname}','{subcode}','{subname}','{dob}') ")
                flash("Data Added Successfully","success")
                return render_template("admin.html")
        else:
            flash("Login and try again","success")
            return render_template("addteacher.html")



@app.route('/addstudent',methods=['POST','GET'])
def addstudent():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            s_id=request.form.get('s_id')
            sname=request.form.get('sname')
            s_email=request.form.get('semail')
            bid=request.form.get('bid')
            sysid=request.form.get('sys_id')
            s_dob=request.form.get('dob')
            nuser=Student.query.filter_by(s_id=s_id).first()
            print(nuser)
            if nuser :
                flash("Student already exist in Database","warning")
                return render_template("admin.html")
            else:
                nuser=db.engine.execute(f"INSERT INTO `student` (`s_id`,`s_name`,`dob`,`b_id`,`sys_id`,`email`) VALUES ('{s_id}','{sname}','{s_dob}','{bid}','{sysid}','{s_email}') ")
                flash("Data Added Successfully","success")
                return render_template("admin.html")
        else:
            flash("Add data","success")
            return render_template("addstudent.html")

@app.route('/addbatch',methods=['POST','GET'])
def addbatch():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            b_id=request.form.get('b_id')
            bday=request.form.get('day')
            btin=request.form.get('tin')
            btout=request.form.get('tout')
            btid=request.form.get('btid')
            nuser=Batch.query.filter_by(b_id=b_id).first()
            print(nuser)
            if nuser :
                flash("Batch already exist in Database","warning")
                return render_template("admin.html")
            else:
                nuser=db.engine.execute(f"INSERT INTO `batch` (`b_id`,`day`,`time_in`,`time_out`,`t_id`) VALUES ('{b_id}','{bday}','{btin}','{btout}','{btid}') ")
                flash("Data Added Successfully","success")
                return render_template("admin.html")
        else:
            flash("Add Data","success")
            return render_template("addbatch.html")



@app.route('/addexperiment',methods=['POST','GET'])
def addexperiment():
        #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            e_id=request.form.get('e_id')
            etitle=request.form.get('title')
            edoe=request.form.get('deo')
            etid=request.form.get('etid')
            nuser=Experiment.query.filter_by(e_id=e_id).first()
            if nuser :
                flash("Experiment already exist in Database","warning")
                return render_template("admin.html")
            else:
                nuser=db.engine.execute(f"INSERT INTO `experiment` (`e_id`,`title`,`doe`,`t_id`) VALUES ('{e_id}','{etitle}','{edoe}','{etid}') ")
                flash("Data Added Successfully","success")
                return render_template("admin.html")
        else:
            flash("Add data","success")
            return render_template("addexperiment.html")


@app.route('/deleteteacher',methods=['POST','GET'])
def deleteteacher():
     #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            tid=request.form.get('tr_id')
            duser=Teacher.query.filter_by(tr_id=tid).first()
            if duser :
                Teacher.query.filter(Teacher.t_id == tid).delete()
                db.session.commit()
                flash("Teacher ID is deleted Database","success")
                return render_template("admin.html")
            else:
                
                flash("Teacher ID not present in DATABASE","danger")
                return render_template("admin.html")
        else:
            flash("Delete data","success")
            return render_template("deleteteacher.html")

@app.route('/deleteexperiment',methods=['POST','GET'])
def deleteexperiment():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            e_id=request.form.get('e_id')
            duser=Experiment.query.filter_by(e_id=e_id).first()
            if duser :
                Experiment.query.filter(Experiment.e_id == e_id).delete()
                db.session.commit()
                flash("Experiment ID is deleted Database","success")
                return render_template("admin.html")
            else:
                
                flash("Teacher ID not present in DATABASE","danger")
                return render_template("admin.html")
        else:
            flash("Delete data","success")
            return render_template("deleteexperiment.html")

@app.route('/deletestudent', methods=['POST','GET'])
def deletestudent():#if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            s_id=request.form.get('s_id')
            duser=Student.query.filter_by(s_id=s_id).first()
            if duser :
                Student.query.filter(Student.s_id == s_id).delete()
                db.session.commit()
                flash("Student ID is deleted Database","success")
                return render_template("admin.html")
            else:
                flash("Student ID not present in DATABASE","danger")
                return render_template("admin.html")
        else:
            flash("Delete data","success")
            return render_template("deletestudent.html")

@app.route('/deletesystem',methods=['POST','GET'])
def deletesystem():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            sysid=request.form.get('sys_id')
            duser=System.query.filter_by( sys_id = sysid ).first()
            if duser :
                System.query.filter(System.sys_id == sysid).delete()
                db.session.commit()
                flash("Teacher ID is deleted Database","success")
                return render_template("admin.html")
            else:
                flash("Teacher ID not present in DATABASE","danger")
                return render_template("admin.html")
        else:
            flash("Delete data","success")
            return render_template("deletesystem.html")

@app.route('/deletebatch',methods=['POST','GET'])
def deletebatch():
    #if('user' in session and session['user']==params['user']):
        if request.method=="POST":
            b_id=request.form.get('b_id')
            duser=Batch.query.filter_by(b_id=b_id).first()
            if duser :
                Batch.query.filter(Batch.b_id == b_id).delete()
                db.session.commit()
                flash("Batch is deleted Database","success")
                return render_template("admin.html")
            else:
                
                flash("Batchher ID not present in DATABASE","danger")
                return render_template("admin.html")
        else:
            flash("Delete data","success")
            return render_template("deletebatch.html")


@app.route('/updateteacher',methods=['POST','GET'])
def updateteacher():
    if request.method=="POST":
            tid=request.form.get('t_id')
            tname=request.form.get('tname')
            subcode=request.form.get('sub_code')
            subname=request.form.get('sub_name')
            dob=request.form.get('dob')
            nuser=Teacher.query.filter_by(t_id=tid).first()
            if nuser :

                nuser.t_id=tid
                nuser.t_name=tname
                nuser.sub_code=subcode
                nuser.sub_name=subname
                nuser.dob=dob
                db.session.commit()
                flash("Data Updated in Database","success")
                return render_template("admin.html")
            else:
                flash("Data not found","danger")
                return render_template("updatestudent.html")
    else:
        flash("Update data","success")
        return render_template("updateteacher.html")

@app.route('/updateexperiment',methods=['POST','GET'])
def updateexperiment():
        if request.method=="POST":
            e_id=request.form.get('e_id')
            etitle=request.form.get('title')
            edoe=request.form.get('deo')
            etid=request.form.get('etid')
            nuser=Experiment.query.filter_by(e_id=e_id).first()
            print(nuser)
            if nuser :

                nuser.e_id=e_id
                nuser.title=etitle
                nuser.doe=edoe
                nuser.t_id=etid
                db.session.commit()
                flash("Data Updated in Database","success")
                return render_template("admin.html")
            else:
                flash("Data not found","danger")
                return render_template("updatestudent.html")
        else:
            flash("Update data","success")
            return render_template("updateexperiment.html")

@app.route('/updatestudent', methods=['POST','GET'])
def updatestudent():
        if request.method=="POST":
            s_id=request.form.get('s_id')
            sname=request.form.get('sname')
            s_email=request.form.get('semail')
            bid=request.form.get('bid')
            sysid=request.form.get('sys_id')
            s_dob=request.form.get('dob')
            nuser=Student.query.filter_by(s_id=s_id).first()
            print(nuser)
            if nuser :

                nuser.s_id = s_id
                nuser.s_name = sname
                nuser.dob = s_dob
                nuser.b_id = bid
                nuser.sys_id = sysid
                nuser.email = s_email
                db.session.commit()
                flash("Data Updated in Database","success")
                return render_template("admin.html")
            else:
                flash("Data not found","danger")
                return render_template("updatestudent.html")
        else:
            flash("Update data","success")
            return render_template("updatestudent.html")

@app.route('/updatesystem',methods=['POST','GET'])
def updatesystem(): 
        if request.method=="POST":
            sys_id=request.form.get('sys_id')
            sat=request.form.get('status')
            checkid=System.query.filter_by(sys_id=sys_id).first()
            print(checkid)
            if checkid :

                checkid.sys_id=sys_id
                checkid.status=sat
                db.session.commit()
                flash("Data Updated in Database","success")
                return render_template("admin.html")
            else:
                flash("Data not found","danger")
                return render_template("updatestudent.html")
        else:
            flash("Update data","success")
            return render_template("updatesystem.html")


@app.route('/updatebatch',methods=['POST','GET'])
def updatebatch():
        if request.method=="POST":
            b_id=request.form.get('b_id')
            bday=request.form.get('day')
            btin=request.form.get('tin')
            btout=request.form.get('tout')
            btid=request.form.get('btid')
            nuser=Batch.query.filter_by(b_id=b_id).first()
                     
            if nuser :

                nuser.b_id=b_id
                nuser.day=bday
                nuser.time_in=btin
                nuser.time_out=btout
                nuser.t_id=btid
                db.session.commit()
                flash("Data Updated in Database","success")
                return render_template("admin.html")
            else:
                flash("Data not found","danger")
                return render_template("updatestudent.html")
        else:
            flash("Update data","success")
            return render_template("updatebatch.html")

@app.route('/tablestudent', methods=['POST','GET'])
def tablestudent():
    students = Student.query.all()
    return render_template('tablestudent.html', student=students)

'''@app.route('/tablestudent', methods=['POST','GET'])
def tablestudent():
    stu=db.engine.execute("SELECT * FROM `student` ORDER BY `s_id`")
    return render_template("tablestudent.html", Student)'''




@app.route('/admin',methods=['POST','GET'])
def admin():
    return render_template("admin.html")

@app.route("/teacherlogin")
def teacherlogin():
    return render_template("teacherlogin.html")

@app.route("/studentlogin")
def studentlogin():
    return render_template("studentlogin.html")

if __name__ == '__main__':
    app.run(debug=True)