import urllib
import numpy as np
import mysql.connector
import cv2
import pyttsx3
import pickle
from datetime import datetime
import sys
import PySimpleGUI as sg

# 1 Create database connection
myconn = mysql.connector.connect(host="localhost", user="root", passwd="Wenger<3", database="facerecognition")
date = datetime.utcnow()
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()


#2 Load recognize and read label from model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("train.yml")

labels = {"person_name": 1}
with open("labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

# create text to speech
engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 175)

# Define camera and detect face
face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)


# 3 Define pysimplegui setting
layout =  [
    [sg.Text('Setting', size=(18,1), font=('Any',18),text_color='#1c86ee' ,justification='left')],
    [sg.Text('Confidence'), sg.Slider(range=(0,100),orientation='h', resolution=1, default_value=60, size=(15,15), key='confidence')],
    [sg.OK(), sg.Cancel()]
      ]
win = sg.Window('iKYC System',
        default_element_size=(21,1),
        text_justification='right',
        auto_size_text=False).Layout(layout)
event, values = win.Read()
if event is None or event =='Cancel':
    exit()
args = values
gui_confidence = args["confidence"]
win_started = False

# 4 Open the camera and start face recognition
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

    for (x, y, w, h) in faces:
        print(x, w, y, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # 4.1 If the face is recognized
        if conf >= gui_confidence:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # Find the customer information in the database.
            select = "SELECT customer_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date), login_time FROM Customer WHERE name='%s' AND customer_id='%d'" %(name, id_)
            name = cursor.execute(select)
            result = cursor.fetchall()
            print(result)


            #storing the information in variables for display by frontend
            c_id = result[0][0]
            c_name = result[0][1]
            c_login_d = result[0][2]
            c_login_m = result[0][3]
            c_login_y = result[0][4]
            c_time =  result[0][5]

            print("customer id = ", c_id)
            print("customer name = ", c_name)
            print("login date ", c_login_d, c_login_m, c_login_y)
            print("login time ", c_time)


            # print(result)
            data = "error"

            for x in result:
                data = x

            # If the customer's information is not found in the database
            if data == "error":
                # the customer's data is not in the database
                print("The customer", current_name, "is NOT FOUND in the database.")

            # If the customer's information is found in the database
            else:
                """
                Implement useful functions here.


                """
                update =  "UPDATE Customer SET login_date=%s WHERE name=%s AND customer_id=%s"
                val = (date, current_name, id_)
                cursor.execute(update, val)
                update = "UPDATE Customer SET login_time=%s WHERE name=%s AND customer_id=%s"
                val = (current_time, current_name, id_)
                cursor.execute(update, val)
                myconn.commit()

                hello = ("Hello ", current_name, "Welcom to the iKYC System")
                print(hello)
                engine.say(hello)

                select = "SELECT account_num FROM Customer_Account WHERE customer_id=%s"
                # select = "SELECT * FROM Customer_Account"

                val = (c_id,)
                cursor.execute(select, val)
                listof_account_nums = cursor.fetchall()

                print(listof_account_nums)


                #The customer can view his/her account information such as a list of accounts (e.g. saving,current, HKD, USD, etc.), account numbers, balances, etc.\

                for account_num in listof_account_nums:
                    print ("the account number is: ", account_num)

                    # DISPLAY the current accounts and Savings accounts for this user

                    # displaying the current accounts first
                    # for a current account it should not be in savings account
                    select = "SELECT Acc.balance, Acc.currency FROM Account Acc, Customer_Account Ca WHERE Ca.customer_id = %s and Acc.account_num= %s AND Acc.account_num = Ca.account_num AND %s NOT IN (SELECT account_num FROM Savings_Account WHERE account_num = %s)"
                    val = (c_id, account_num[0], account_num[0], account_num[0])
                    cursor.execute(select, val)
                    account_data = cursor.fetchall()

                    if account_data:
                        print('current account:' )
                        print(account_data)



                    # to be displayed by frotnend
                    # if account_data:
                    #     print("current account data is: ")
                    #     print(account_data)

                    else:


                        #disply the information for a savings account
                        select = """
                        SELECT Sa.balance, Sa.currency, Sa.interest_rate
                        FROM Customer_Account Ca, Savings_Account Sa
                        WHERE Ca.customer_id = %s and Ca.account_num= %s
                        AND Ca.account_num = Sa.account_num and %s IN (
                        SELECT account_num
                        FROM Savings_Account
                        WHERE account_num = %s
                        )
                        """
                        val = (c_id, account_num[0], account_num[0], account_num[0])
                        cursor.execute(select, val)
                        account_data = cursor.fetchall()
                        # to be displayed by frotnend
                        print("savings account data is: ")
                        print(account_data)





                    # The customer can click the account to see the detail transactions, and search the
                    # transactions based on month, day, time and amount.
                    # • The transactions can be presented in the GUI.

                    # frontend should make acocunt numbers clickable, then retrieve the clicked account number as a variable. the database will perform a search query

                    # using this account number, display the transaction details then search based on month, day, time and amount

                    select = """
                    SELECT T.to, T.from, T.trans_id, T.time, T.date, T.amount
                    FROM Transaction T, Account A
                    WHERE A.account_num =%s AND (A.account_num=T.to OR A.account_num=T.from)
                    """

                    val = (account_num[0],)
                    cursor.execute(select, val)
                   
                    trans_details = cursor.fetchall()
                    # to be displayed by frotnend
                    #also convert total seconds to time when displaying on frontend
                    print("The transaction details are: ", trans_details)

                    # for a given account number (frontend) implementing searching based on Month
                    

                    select = """
                    SELECT T.to, T.from, T.trans_id, T.time, T.date, T.amount
                    FROM Transaction T, Account A
                    WHERE A.account_num=%s AND (A.account_num=T.to OR A.account_num=T.from)
                    ORDER BY YEAR(T.date) DESC, MONTH(T.date) DESC
                    """

                    val = (account_num[0],)
                    cursor.execute(select, val)
                    trans_bymonth = cursor.fetchall()
                    # to be displayed by frotnend
                    #also convert seconds to time when displaying on frontend
                    print("Sorted by month details are: ", trans_bymonth)

                    # for a given account number (frontend) implementing searching based on day
                    # dummy_account_num = "A1004"

                    select = """
                    SELECT T.to, T.from, T.trans_id, T.time, T.date, T.amount
                    FROM transaction T, Account A
                    WHERE A.account_num = %s AND (A.account_num=T.to OR A.account_num=T.from)
                    ORDER BY YEAR(T.date) DESC, MONTH(T.date) DESC, DAY(T.date) DESC
                    """

                    val = (account_num[0],)
                    cursor.execute(select, val)
                    trans_byday = cursor.fetchall()
                    # # to be displayed by frotnend
                    #also convert seconds to time when displaying on frontend
                    print("Sorted by day details are: ", trans_byday)

                    # for a given account number (frontend) implementing searching based on time
                    # dummy_account_num = "A1004"

                    select = """
                    SELECT T.to, T.from, T.trans_id, T.time, T.date, T.amount
                    FROM Transaction T, Account A
                    WHERE A.account_num=%s AND (A.account_num=T.to OR A.account_num=T.from)
                    ORDER BY YEAR(T.date) DESC, MONTH(T.date) DESC, DAY(T.date) DESC, T.time DESC
                    """

                    val = (account_num[0],)
                    cursor.execute(select, val)
                    trans_bytime = cursor.fetchall()
                    # # to be displayed by frotnend
                    #also convert seconds to time when displaying on frontend
                    print("Sorted by time details are: ", trans_bytime)


                    # for a given account number (frontend) implementing searching based on amount
                    # dummy_account_num = "A1004"

                    select = """
                    SELECT T.to, T.from, T.trans_id, T.time, T.date, T.amount
                    FROM Transaction T, Account A
                    WHERE A.account_num=%s AND (A.account_num=T.to OR A.account_num=T.from)
                    ORDER BY T.amount DESC
                    """

                    val = (account_num[0],)
                    cursor.execute(select, val)
                    trans_byamount = cursor.fetchall()
                    # # to be displayed by frotnend
                    #also convert seconds to time when displaying on frontend
                    print("Sorted by amount details are: ", trans_byamount)


        # 4.2 If the face is unrecognized
        else:
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
            hello = ("Your face is not recognized")
            print(hello)
            engine.say(hello)
            # engine.runAndWait()

    # GUI
    imgbytes = cv2.imencode('.png', frame)[1].tobytes()
    if not win_started:
        win_started = True
        layout = [
            [sg.Text('iKYC System Interface', size=(30,1))],
            [sg.Image(data=imgbytes, key='_IMAGE_')],
            [sg.Text('Confidence'),
                sg.Slider(range=(0, 100), orientation='h', resolution=1, default_value=60, size=(15, 15), key='confidence')],
            [sg.Exit()]
        ]
        win = sg.Window('iKYC System',
                default_element_size=(14, 1),
                text_justification='right',
                auto_size_text=False).Layout(layout).Finalize()
        image_elem = win.FindElement('_IMAGE_')
    else:
        image_elem.Update(data=imgbytes)

    event, values = win.Read(timeout=20)
    if event is None or event == 'Exit':
        break
    gui_confidence = values['confidence']


win.Close()
cap.release()
