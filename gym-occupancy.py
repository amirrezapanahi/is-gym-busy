import subprocess
import re
import time
from datetime import datetime
import pytz
import smtplib, ssl
import sys
import certifi

port = 465  # For SSL
context = ssl.create_default_context(cafile=certifi.where())
email_sender = sys.argv[1]
password_sender = sys.argv[2]
emai_receiver = sys.argv[3]

tz_GB = pytz.timezone('Europe/London')
datetime_GB = datetime.now(tz_GB)

if __name__ == '__main__':
    while True:
        if 22 >= datetime_GB.hour >= 7:
            occupancyHtml = subprocess.run('curl -s https://sport.wp.st-andrews.ac.uk | grep "Occupancy"', shell=True,
                                           text=True, capture_output=True)
            occupancy = re.search("\\d+(?:\\.\\d+)?%", occupancyHtml.stdout)
            occupancy = occupancy.group()[0:len(occupancy.group()) - 1]
            if int(occupancy) <= 50:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
                    server.login(email_sender, password_sender)
                    server.sendmail(email_sender, emai_receiver, "gym is at " + occupancy + "% occupancy, go gym fam.")

        time.sleep(20 * 60)
        datetime_GB = datetime.now(tz_GB)
