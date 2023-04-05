import time
import mysql.connector

from ANPR.anpr import ANPR
from OBJECTSIZE.objectsize import OBJECT_SIZE
from SPACECOUNTER.spacecounter import SPACE_COUNTER
from PAYMENT.payment import payment
from MESSAGES.message import MESSAGE
from datetime import datetime , timedelta ,date
from DATABASE.database import DATABASE_DETAILS
from flask import Flask,render_template,request


app=Flask(__name__)

@app.route('/',methods=['POST','GET'])


def index():
    
    slot=''
    if request.method=='POST':
        slot=SPACE_COUNTER()
        form_data=request.form
        temp=form_data['phone']
        core_part(temp)
    return render_template('input.html',slot=slot)


def core_part(number):
    
    phone_number=number
    
    # ANPR PART

    number_plate=ANPR()


    # Timing Part

    def timing():
        
        curr_time = time.strftime("%H:%M", time.localtime())
        
        return curr_time


    checkin_time=timing()
    time1 = datetime.strptime(checkin_time, "%H:%M")

    checkout_time=( datetime.now() + timedelta( minutes=40 )).strftime('%H:%M')
    time2 = datetime.strptime(checkout_time, "%H:%M")

    diff=time2-time1
    seconds=diff.total_seconds()
    conv_minutes=round(seconds/60)



    # Date Part

    checkin_date=date.today()

    checkout_date=date.today()



    # SPACECOUNTER PART

    slot_available=SPACE_COUNTER()


    # OBJECTSIZE PART

    vehicle_type=OBJECT_SIZE()

    vehicle_spelling=""

    per_min_for_four_wheeler=0.50

    per_min_for_two_wheeler=0.25

    amount=0

    if vehicle_type > 250:
        amount=per_min_for_four_wheeler * conv_minutes
        vehicle_spelling="FOUR"
    else:
        amount=per_min_for_two_wheeler * conv_minutes
        vehicle_spelling="TWO"


    # DATABASE PART

    DATABASE_DETAILS(number_plate,vehicle_spelling,slot_available,checkin_time,checkout_time,checkin_date,checkout_date,amount,phone_number)
    
    
    # PAYMENT PART

    payment(amount)


    # MESSAGE PART

    MESSAGE(number_plate,conv_minutes,amount,phone_number)



@app.route('/result')


def result():
    vehicle_number,vehicle_type,slotallocated,check_in_time,check_out_time,check_in_date,check_out_date,phone_number,amount=getting_db_details_to_show_final_result()
    return render_template('output.html',vehicle_number=vehicle_number,vehicle_type=vehicle_type,slotallocated=slotallocated,check_in_time=check_in_time,check_out_time=check_out_time,check_in_date=check_in_date,check_out_date=check_out_date,phone_number=phone_number,amount=amount)


def getting_db_details_to_show_final_result():
    
    # Database Part

    mydb = mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12608644",password="tWjGz515yZ",database="sql12608644")
    cursor=mydb.cursor()
    mySql_fetch_query="SELECT * FROM  PARKINGSYSTEM WHERE id=(SELECT MAX(id) FROM PARKINGSYSTEM);"
    cursor.execute(mySql_fetch_query)
    record=cursor.fetchone()

    vn=record[1]
    vt=record[2]
    sa=record[3]
    cit=record[4]
    cot=record[5]
    cid=record[6]
    cod=record[7]
    amnt=record[8]
    phone=record[9]


    cursor.close()
    mydb.close()
    
    vehicle_number=vn
    vehicle_type=vt
    slotallocated=sa
    check_in_time=cit
    check_out_time=cot
    check_in_date=cid
    check_out_date=cod
    phone_number=phone
    amount=amnt

    return vehicle_number,vehicle_type,slotallocated,check_in_time,check_out_time,check_in_date,check_out_date,phone_number,amount


if __name__=='__main__':
    app.run(debug=True)