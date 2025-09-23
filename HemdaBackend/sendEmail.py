import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# פרטי חשבון המייל
sender_email = "zachi79@gmail.com"
password = "oikx zckq pltr yxah" # יש להשתמש בסיסמת יישום

# פרטי המייל
receiver_email = "zachi79@gmail.com"
subject = "מייל נשלח באמצעות Python!"
body = "היי, זוהי הודעת בדיקה שנשלחה מ-Python."

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