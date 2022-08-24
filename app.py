import string
import mysql.connector.errorcode
from flask import *
import mysql.connector
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

app = Flask(__name__)
app.secret_key = 'login'
mydb = mysql.connector.connect(host="localhost", user="Kishore", passwd="Kishore@123",
                               auth_plugin='mysql_native_password', database="BusBooking")
# print(mydb, "connection Successful")
Cursor = mydb.cursor()
Cursor.execute("Use BusBooking")
Book_Status = {} # to maintain booking status with session and database
check = []
User_partial = {}
Gen_Check = {}


# Starting route
@app.route('/')
def home():
    # print('Signup page rendered')
    return redirect(url_for('Dashboard'))


@app.route('/login', methods=['post', 'get'])
def login():
    if 'Mobile_num' in session:
        return redirect(url_for('Dashboard'))
    if request.method == 'POST':
        # print("inside login post")
        Mobile_Num = request.form['Mobile_num']
        Password = request.form['Pass']
        get_data = f"SELECT Password,Gender,Name FROM User WHERE MobileNum = {Mobile_Num}"
        Cursor.execute(get_data)
        result = Cursor.fetchall()
        # print(result)
        if len(result):
            if result[0][0] == Password:
                session['Mobile_num'] = Mobile_Num
                session['Gender'] = result[0][1]
                session['user'] = result[0][2]
                # print(session, "Session printed")
                return redirect(url_for('Dashboard'))
            else:
                return render_template('login.html', msg='Authentication Failed, Enter Valid Credentials !!!')
        else:
            return render_template('login.html', msg='User Does Not Exist')
    else:
        return render_template('login.html')


# Signup route
@app.route('/Signup', methods=['post', 'get'])
def Signup():
    if 'Mobile_num' in session:
        return redirect(url_for('Dashboard'))
    if request.method == 'POST':
        # print('signup route')
        user_name = request.form['user_Name']
        User_Age = int(request.form['User_Age'])
        Gender = request.form['Gender']
        Email = request.form['Email']
        Mobile_number = request.form['Mobile_number']
        Password = request.form['Password']
        C_password = request.form['C_password']
        upper_case = any([1 if c in string.ascii_uppercase else 0 for c in Password])
        lower_case = any([1 if c in string.ascii_lowercase else 0 for c in Password])
        Special = any([1 if c in string.punctuation else 0 for c in Password])
        Digits = any([1 if c in string.digits else 0 for c in Password])
        # password_hash = bcrypt.generate_password_hash(Password)
        # print(password_hash)
        # print(upper_case, lower_case, Special, Digits)
        if not upper_case or not lower_case or not Special or not Digits or not (8 <= len(Password) <= 12):
            return render_template('Signup.html', msg='Password Must Contain 8 to 12 Characters, one Upper, one Lower, one Special character and one Digit')
        if Password != C_password:
            return render_template('Signup.html', msg='Entered Password and Confirm-password are not Same')
        if Gender == '0':
            return render_template('Signup.html', msg='Gender Not Selected')
        if len(Mobile_number) != 10:
            return render_template('Signup.html', msg='Enter Valid Mobile Number!!!')
        else:
            data = (user_name, User_Age, Gender, Email, Mobile_number, Password)
            add_Data = '''INSERT INTO User (Name, Age, Gender, Email, MobileNum, Password) VALUES ('%s', %d, '%s', '%s', '%s', '%s');''' % data
            Cursor.execute(add_Data)
            mydb.commit()
            return redirect(url_for('login'))
    else:
        return render_template('Signup.html')


@app.route('/Logout')
def Logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/SearchBus', methods=['post', 'get'])
def SearchBus():
    if request.method == 'POST' and "Mobile_num" in session:
        route_from = request.form['From']
        route_to = request.form['To']
        if route_from == '' or route_to == '':
            return redirect(url_for('Dashboard'))
        else:
            user = session['user']
            return render_template('index.html', From=route_from, To=route_to, msg='BusSearched', user_name=user)
    else:
        return redirect(url_for('login'))


@app.route('/ViewSeats', methods=['post', 'get'])
def ViewSeats():
    if request.method == 'POST' and "Mobile_num" in session:
        Cursor.execute(
            'UPDATE BookStatus SET PassengerName  = DEFAULT(PassengerName), PassengerAge = DEFAULT(PassengerAge), PassengerGender = DEFAULT(PassengerGender), BookingStatus = DEFAULT(BookingStatus), TimeStamp = DEFAULT(TimeStamp) WHERE TimeStamp < (NOW() - INTERVAL 2 MINUTE) AND BookingStatus = "Partial"')
        mydb.commit()
        Data()
        # for i in Gen_Check:
        #     print(i, '-->', Gen_Check[i])
        check.clear()
        return render_template('Booking.html', Book_Status=Book_Status, length=len(check), Gen_Check=Gen_Check,
                               Gender=session["Gender"])
    else:
        return redirect(url_for('login'))


@app.route('/Button', methods=['post', 'get'])
def Button():
    if request.method == 'POST' and 'Mobile_num' in session:
        Btn = int(request.form['btn'])
        Cursor.execute(f"SELECT SeatNo FROM BookStatus WHERE No = {Btn}")
        Result = Cursor.fetchall()
        if User_partial[Btn] == 'Partial':
            return render_template('Booking.html', Book_Status=Book_Status, length=len(check), Gen_Check=Gen_Check,
                                   Gender=session["Gender"])
        if Book_Status[Btn] == 'unBooked':
            if len(check) > 5:
                # print(check)
                return render_template('Booking.html', Book_Status=Book_Status,
                                       msg='The maximum number of seats that can be selected is 6', length=len(check),
                                       Gen_Check=Gen_Check, Gender=session["Gender"])
            check.append(Result[0][0])
            Book_Status[Btn] = 'Partial'
        elif Book_Status[Btn] == 'Partial':
            check.remove(Result[0][0])
            Book_Status[Btn] = 'unBooked'
        return render_template('Booking.html', Book_Status=Book_Status, length=len(check), Gen_Check=Gen_Check,
                               Gender=session["Gender"])
    else:
        return redirect(url_for('login'))


@app.route('/Block', methods=['post', 'get'])
def Block():
    if request.method == 'POST' and 'Mobile_num' in session:
        user = session["Mobile_num"]
        get_data = f"SELECT Name,Age,Gender FROM User WHERE MobileNum = {user}"
        Cursor.execute(get_data)
        Result = Cursor.fetchall()
        length = len(check)
        for i in range(0, length):
            data = (Result[0][0], int(Result[0][1]), Result[0][2], check[i])
            User_partial[check[i]] = 'Partial'
            add_Data = ''' UPDATE BookStatus SET PassengerName = '%s', PassengerAge = %d, PassengerGender = '%s', BookingStatus = 'Partial', TimeStamp = now() WHERE SeatNo = '%s';''' % data
            Cursor.execute(add_Data)
            mydb.commit()
        return render_template('PassengerDetails.html', check=check, length=len(check))
    else:
        return redirect(url_for('login'))


@app.route('/Confirm', methods=['post', 'get'])
def Confirm():
    if request.method == 'POST' and 'Mobile_num' in session:
        length = len(check)
        for i in range(1, length + 1):
            Book_Status[check[i - 1]] = 'Booked'
            # print(check[i - 1], '-->', Book_Status[check[i - 1]])
            data = (request.form['N' + str(i)], int(request.form['A' + str(i)]), request.form['G' + str(i)],
                    request.form['G' + str(i)], check[i - 1])
            # print(data)
            add_Data = '''UPDATE BookStatus SET PassengerName = '%s', PassengerAge = %d, PassengerGender = '%s', BookingStatus = 'Booked', Gen = '%s' WHERE SeatNo = '%s';''' % data
            Cursor.execute(add_Data)
            mydb.commit()
            # print("Query Executed")
        for i in check:
            # print(i)
            get_data = "SELECT * FROM BookStatus WHERE SeatNo = '%s'" % i
            Cursor.execute(get_data)
            Result = Cursor.fetchall()
            # print(Result)
            # print(Result[0][6], type(Result[0][6]))
            if Result[0][7] == 'Female':
                if (1 <= Result[0][6] <= 6) or (19 <= Result[0][6] <= 24):
                    val = Result[0][6] + 6
                    add_Data = ''' UPDATE BookStatus SET Gen = 'Reserved' WHERE No = %d AND Gen = 'Nothing';''' % val
                    Cursor.execute(add_Data)
                    mydb.commit()
                elif (7 <= Result[0][6] <= 12) or (25 <= Result[0][6] <= 30):
                    val = Result[0][6] - 6
                    add_Data = ''' UPDATE BookStatus SET Gen = 'Reserved' WHERE No = %d AND Gen = 'Nothing';''' % val
                    Cursor.execute(add_Data)
                    mydb.commit()
        user = session['user']
        # for key in Gen_Check:
        #     print(key, '-->', Gen_Check[key])
        return render_template('index.html', msg="Bus Booked Successfully", user_name=user)
    else:
        return redirect(url_for('login'))


@app.route('/Dashboard')
def Dashboard():
    if 'Mobile_num' in session:
        user = session['user']
        return render_template('index.html', user_name=user)
    else:
        return redirect(url_for('login'))


@app.route('/ADMIN', methods=['post', 'get'])
def ADMIN():
    if request.method == 'POST':
        admin_user = request.form['admin_user']
        admin_pass = request.form['admin_pass']
        if admin_user == 'Kishore' and admin_pass == 'Kishore':
            return render_template('admin.html')
        else:
            return redirect(url_for('ADMIN'))
    else:
        return render_template('Admin_login.html')


# data from database
def Data():
    Cursor.execute("select * from BookStatus")
    data = Cursor.fetchall()
    for row in data:
        Book_Status[row[6]] = row[4]
        User_partial[row[6]] = row[4]
        Gen_Check[row[6]] = row[7]


if __name__ == '__main__':
    Data()
    # print('flask started')
    app.run(debug=True, port=8000)
