from monitor import app
from email.mime.text import MIMEText
from email.header import Header
from monitor import config
import requests
import time
import smtplib
import datetime


@app.task
def monitor_my_site():
    status = requests_my_site()
    if status != 200:
        send_mail(status)
        

def requests_my_site():
    url = config.MY_SITE
    # url = "http://zyp12581.xyz"
    res = requests.get(url)

    return res.status_code

def send_mail(status):
    message = MIMEText('服务器error: {}'.format(status), 'plain', 'utf-8')
    message['From'] = Header("site", 'utf-8')
    message['To'] = Header('Error', 'utf-8')
    message['Subject'] = Header('服务器error', 'utf-8')

    try:
        obj = smtplib.SMTP_SSL(config.MAIL_HOST, 465)
        # obj.connect(config.MAIL_HOST, 25)
        obj.login(config.MAIL_USER, config.MAIL_PASS)
        obj.sendmail(config.SNEDER, [config.RECEIVER], message.as_string())
        obj.quit()
    except Exception as e:
        with open('error.log', 'a') as f:
            info = "[{}] error: {}\n".format(datetime.datetime.now(), e)
            f.write(info)
        

if __name__ == "__main__":
    send_mail('200')