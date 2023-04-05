import mysql.connector


def DATABASE_DETAILS(vehicleno , vehicleType , allocspace , cin , cout , cindate , coutdate , amnt ,phone):
  
  mydb = mysql.connector.connect(host="sql12.freesqldatabase.com",user="sql12608644",password="tWjGz515yZ",database="sql12608644")

  myconn = mydb.cursor()

  mySql_insert_query = "INSERT INTO PARKINGSYSTEM(VEHICLE_NUMBER, VEHICLE_TYPE, SPACE_ALLOCATED, CHECK_IN_TIME, CHECK_OUT_TIME, CHECK_IN_DATE, CHECK_OUT_DATE, AMOUNT, PHONE)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
  
  data=(vehicleno , vehicleType , allocspace , cin , cout , cindate , coutdate , amnt , phone)

  myconn.execute(mySql_insert_query,data)

  mydb.commit()
  
  mydb.close()


#DATABASE_DETAILS('XPG','Four',5,'10:12','10:30','2023-03-20','2023-03-20',50.0,7337010225)