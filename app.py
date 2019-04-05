from __future__ import print_function
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField,DateField, PasswordField, BooleanField, SubmitField, validators, FloatField
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
import MySQLdb.cursors
from functools import wraps
from random import randint
from compute import computeTarget



app = Flask(__name__)

#Config MySQL

#app.config['MYSQL_HOST'] = 'soumitra-data-instance.cy0ndyu27pmg.us-east-2.rds.amazonaws.com'
#app.config['MYSQL_USER'] = 'soumitra_user'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'soumitradata'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    name = StringField('Name', [
    validators.Length(min = 1, max = 50),
    validators.DataRequired()
    ])
    email_id = StringField('Email', [
    validators.Length(min = 6, max = 50),
    validators.DataRequired()
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    usertype = BooleanField('Developer?')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email_id = form.email_id.data
        password = sha256_crypt.encrypt(str(form.password.data))
        usertype = form.usertype.data
        #create cursor
        cur = mysql.connection.cursor()
        # Execute Query

        cur.execute("INSERT INTO users(name, email_id, password, usertype) VALUES (%s, %s, %s, %s)", (name, email_id, password, usertype))

        #commit to DB

        mysql.connection.commit()

        #close connection

        cur.close()

        flash('You are now Registered and can Log In', 'success')

        return redirect(url_for('login'))

        #return render_template('register.html', form = form)
    return render_template('register.html', form = form)

#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Fields
        email_id = request.form['email_id']
        password_candidate = request.form['password']

        #Create a cursor

        cur = mysql.connection.cursor()

        #Get user by email_id
        result = cur.execute('SELECT * FROM users WHERE email_id = %s', [email_id])
        #record = cur.fetchall()


        if result > 0:
            #Get stored hash
            data = cur.fetchone()
            password = data['password']
            #Compare the password

            if sha256_crypt.verify(password_candidate, password):
                # Passed

                session['logged_in'] = True
                session['email_id'] = email_id
                session['name'] = data['name']
                session['usertype'] = data['usertype']

                flash('You are now logged in', 'success')
                return redirect(url_for('about'))


            else:
                error = 'Invalid Login'
                return render_template('login.html', error = error)
            #close connection
            cur.close()
        else:
            error = 'Email Not Found'
            return render_template('login.html', error = error)

    return render_template('login.html')


#Check if user logged in

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Login', 'danger')
            return redirect(url_for('login'))
    return wrap


#logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

#Statistics
@app.route('/statistics')
@is_logged_in
def statistics():

    cur = mysql.connection.cursor()

    #Get Graphs data and location
    result = cur.execute("SELECT * FROM statistics")
    data = cur.fetchall()
    #return str(data)
    #print(data['graph_name'])
    cur.close()
    text = open('textfile1.txt', 'r+')
    content = text.read()
    text.close()
    return render_template('statistics.html', data = data, text = content)

class EnquiryForm(Form):
    first_name = StringField('First Name', [
    validators.Length(min = 1, max = 50),
    validators.DataRequired()
    ])
    last_name = StringField('Last Name', [
    validators.Length(min = 1, max = 50),
    validators.DataRequired()
    ])
    contact_no = StringField('Contact Number', [
        validators.Length(min = 12, max = 12),
        validators.DataRequired()

    ])


@app.route('/cancer_detector', methods = ['GET', 'POST'])
def cancer_detector():
    form = EnquiryForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        contact_no = form.contact_no.data

        #create cursor
        cur = mysql.connection.cursor()


    #Get Graphs data and location
        result = cur.execute("SELECT p.first_name, p.last_name, p.contact_no,b.class from patient_info p,breast_cancer b where p.first_name = %s and p.last_name= %s and p.contact_no= %s and b.id = p.patient_id",[first_name,last_name,contact_no])

        data = cur.fetchall()


        if result > 0:
            return render_template('dashboard.html', data = data)
        else:
            error = 'No Information Found'
            return render_template('cancer_detector.html', error = error)
        mysql.connection.commit()

        cur.close()


    return render_template('cancer_detector.html', form = form)



class AddPatientForm(Form):
    first_name = StringField('First Name', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])
    last_name = StringField('Last Name', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])
    contact_no = StringField('Contact Number', [
        validators.Length(min = 12, max = 12),
        validators.DataRequired()
    ])
    address = TextAreaField('Address', [
        validators.Length(min = 12, max = 50),
        validators.DataRequired()
    ])
    dob = DateField('Date of Birth', [
        validators.Length(min = 12, max = 12),
        validators.DataRequired()
    ])
    ct = StringField('Clump Thickness', [
    validators.Length(min=1,max=2),
    validators.DataRequired()
    ])
    ucsi = StringField('Uniformity of Cell Size',[
        validators.Length(min =1, max=2),
        validators.DataRequired()
    ])
    ucsh = StringField('Uniformity of Cell Shape',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    ma = StringField('Marginal Adhesion',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    secs = StringField('Single Epithelial Cell Size',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    bn = StringField('Bare Nuclei',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    bc = StringField('Bland Chromatin',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    nm = StringField('Normal Nucleoli',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])
    mi = StringField('Mitoses',[
        validators.Length(min = 1, max = 2),
        validators.DataRequired()
    ])

@app.route('/addPatient', methods = ['GET','POST'])
def addPatient():
    form = AddPatientForm(request.form)
    if request.method == 'POST' and form.validate():
        first_name = form.first_name.data
        last_name = form.last_name.data
        contact_no = form.contact_no.data
        address = form.address.data
        dob = form.dob.data
        ct = form.ct.data
        ucsi = form.ucsi.data
        ucsh = form.ucsh.data
        ma = form.ma.data
        secs = form.secs.data
        bn = form.bn.data
        bc = form.bc.data
        nm = form.nm.data
        mi = form.mi.data
        patient_id = randint(0,1000)

        a=ct
        b=ucsi
        c=ucsh
        d=ma
        e=secs
        f=bn
        g=bc
        h=nm
        i=mi
        result = computeTarget(a,b,c,d,e,f,g,h,i)
        console.log(1)

        if(result == 2):
            return ("Benign")
        elif(result == 4):
            return ("Malignant")
        else :
            return ("No Cancer")

        #if(result == 2):
        #    query = cur.execute("INSERT INTO patient_info(patient_id,first_name,last_name,address,dob,contact_no) VALUES (%s,%s,%s,%s,%s,%s,%s)",[patient_id,first_name,last_name,address,dob,contact_no])
        #    query1 = cur.execute("INSERT INTO breast_cancer(id,ct,ucsi,ucsh,ma,secs,bn,bc,nm,mi,class) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[patient_id,ct,ucsi,ucsh,ma,secs,bn,bc,nm,mi,result])

        #    patient_query = cur.execute("SELECT p.first_name, p.last_name, p.contact_no,b.class from patient_info p,breast_cancer b where p.first_name = %s and p.last_name= %s and p.contact_no= %s and b.id = p.patient_id",[first_name,last_name,contact_no])

        #    data = cur.fetchall()

        #    return render_template('/dashboard.html',data=result)
        #else:
        #    query = cur.execute("INSERT INTO patient_info(patient_id,first_name,last_name,address,dob,contact_no) VALUES (%s,%s,%s,%s,%s,%s,%s)",[patient_id,first_name,last_name,address,dob,contact_no])
        #    query1 = cur.execute("INSERT INTO breast_cancer(id,ct,ucsi,ucsh,ma,secs,bn,bc,nm,mi,class) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[patient_id,ct,ucsi,ucsh,ma,secs,bn,bc,nm,mi,result])

        #    patient_query = cur.execute("SELECT p.first_name, p.last_name, p.contact_no,b.class from patient_info p,breast_cancer b where p.first_name = %s and p.last_name= %s and p.contact_no= %s and b.id = p.patient_id",[first_name,last_name,contact_no])

        #    data = cur.fetchall()
        #    return render_template('/dashboard.html',data=result)


    return render_template('addPatient.html',form = form)

def computeTarget(a,b,c,d,e,f,g,h,i):

    engine = create_engine(URL(
    drivername="mysql",
    username="root",
    password="",
    host="localhost",
    database="soumitradata"
    ))

    conn = engine.connect()

    dataset = pd.read_sql(sql='SELECT  ct, ucsi, ucsh, ma, secs, bn, bc, nm, mi, class FROM breast_cancer' , con=conn)

    print(dataset.head())

    dataset = dataset[['ct', 'ucsi','ucsh', 'ma','secs', 'bn', 'bc', 'nm', 'mi', 'class']]

    dataset = dataset.dropna()

    X = dataset.drop('class', axis =1)
    y = dataset['class']

    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state = 1)
    model = tree.DecisionTreeClassifier(random_state= 1)
    print(dataset.head())
    print(model)

    #iris = load_iris()
    k =a
    l = b
    m =c
    n= d
    o = e
    p = f
    q = g
    r = h
    s  = i
    print(model.fit(X_train, y_train))
    values = np.array([[k, l, m, n, o, p, q, r, s]], dtype=np.float64)

    print(values)


if __name__ == '__main__' :
    app.secret_key='secret123'
    app.run(debug=True)
