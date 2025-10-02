import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# פרטי חשבון המייל
sender_email = "zachi79@gmail.com"
password = "oikx zckq pltr yxah"  # יש להשתמש בסיסמת יישום


def sendEmail(receiver_email, subject, body):

    # יצירת אובייקט הודעה
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        # התחברות לשרת ה-SMTP של גוגל
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("המייל נשלח בהצלחה!")
    except Exception as e:
        print(f"אירעה שגיאה: {e}")
    finally:
        server.quit()


def sendEmailPrepareAndSend(dataDF):

    receiver_email = "zachi79@gmail.com"
    subject = "מייל מערכת שיבוץ לוח מבחנים"

    for index, row in dataDF.iterrows():
        teacherSelect = dataDF.iloc[index]['teacherSelect']
        schoolSelect = dataDF.iloc[index]['schoolSelect']
        classSelect = dataDF.iloc[index]['classSelect']
        profSelect = dataDF.iloc[index]['profSelect']
        roomSelect = dataDF.iloc[index]['roomSelect']
        test1 = str(dataDF.iloc[index]['test1']) if dataDF.iloc[index]['test1'] is not None else "לא נקבע"
        test2 = str(dataDF.iloc[index]['test2']) if dataDF.iloc[index]['test2'] is not None else "לא נקבע"
        test3 = str(dataDF.iloc[index]['test3']) if dataDF.iloc[index]['test3'] is not None else "לא נקבע"
        test4 = str(dataDF.iloc[index]['test4']) if dataDF.iloc[index]['test4'] is not None else "לא נקבע"
        test5 = str(dataDF.iloc[index]['test5']) if dataDF.iloc[index]['test5'] is not None else "לא נקבע"
        test6 = str(dataDF.iloc[index]['test6']) if dataDF.iloc[index]['test6'] is not None else "לא נקבע"
        matkonetTest = str(dataDF.iloc[index]['matkonetTest']) if dataDF.iloc[index]['matkonetTest'] is not None else "לא נקבע"
        labTest = str(dataDF.iloc[index]['labTest']) if dataDF.iloc[index]['labTest'] is not None else "לא נקבע"

        body = f"""שלום {teacherSelect},

        להלן שיבוץ לוח המבחנים המלא:

        בית ספר: {schoolSelect}
        כיתה: {classSelect}
        מקצוע: {profSelect}
        חדר: {roomSelect}

        --- מועדי בחינה ---
        מבחן 1: {test1}
        מבחן 2: {test2}
        מבחן 3: {test3}
        מבחן 4: {test4}
        מבחן 5: {test5}
        מבחן 6: {test6}
        מבחן מתכונת: {matkonetTest}
        מבחן מעבדה: {labTest}

        בברכה,
        המערכת האוטומטית
        """
        sendEmail(receiver_email, subject, body)
    pass

