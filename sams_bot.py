from lxml import html 
import requests
import time 
import schedule
import smtplib 
import sys
import os

####   1. Enter product detail urls to scrape   ####
url1 = 'https://www.samsclub.com/p/lysol-early-morning-4-pack/prod21421260'
url2 = 'https://www.samsclub.com/p/clorox-disinfecting-wipes-bleach-free/prod24380340'
url3 = 'https://www.samsclub.com/p/member-s-mark-disinfecting-wipes-variety-pack-4-pk-78-ct-each/prod1790898'
url4 = 'https://www.samsclub.com/p/lysol-spray-4-19oz/prod16940021'
url5 = 'https://www.samsclub.com/p/mm-91-iso-alcohol-twin-pack/prod17750489'
url6 = 'https://www.samsclub.com/p/mm-hand-sanitizer-67-6-fo-2l/prod21420240'
url7 = 'https://www.samsclub.com/p/whole-kernel-corn-12-pk/prod16900107'

####   2. Edit the list to include the urls defined above   ####
products = [url4, url5, url6, url7]


# define header to show you are a browser
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'} 

def sendemail(name, i): 
    ####   3. Enter sender Gmail username here (eg. enter "smith" if your sender email is smith@gmail.com), email must be existing   ####
    GMAIL_USERNAME = "username"
    ####   4. Enter sender Gmail password here   ####
    GMAIL_PASSWORD = "password"
    
    ####   5. Enter receiver email here   ####
    recipient = 'smith@gmail.com'

    body_of_email = 'In Stock!<br>' + name + '<br>' + '<a href="{}">Link</a>'.format(i)
    email_subject = 'In Stock! ' + name
      
    # creates SMTP session  
    s = smtplib.SMTP('smtp.gmail.com', 587)  
      
    # start TLS for security  
    s.starttls()  
      
    # Authentication  
    s.login(GMAIL_USERNAME, GMAIL_PASSWORD)  
      
    # message to be sent  
    headers = "\r\n".join(["from: " + GMAIL_USERNAME, 
                        "subject: " + email_subject, 
                        "to: " + recipient, 
                        "mime-version: 1.0", 
                        "content-type: text/html"]) 
  
    content = headers + "\r\n\r\n" + body_of_email 
    s.sendmail(GMAIL_USERNAME, recipient, content) 
    s.quit()  

def check():
  for i in products:
    # get a website
    page = requests.get(i, headers=headers)

    # parsing the html content 
    doc = html.fromstring(page.content)

    # extract product name
    XPATH_NAME = doc.xpath('//html/head/title/text()')

    # checking availaility 
    XPATH_AVAILABILITY = doc.xpath('//meta[@content="InStock"]')

    if len(XPATH_AVAILABILITY) == 1:
      print('In Stock')
      print(XPATH_NAME[0])
      sendemail(XPATH_NAME[0], i)
      print('Email sent!')
      print()
    else:
      print('Out of Stock')
      print(XPATH_NAME[0])
      print()


def countdown():
####   6. "120" is in seconds, change to the interval you want.   ####
  for remaining in range(120, 0, -1):
    # write over existing written line

    sys.stdout.write("\r")
    # : states a format, 2d states two decimal places
    sys.stdout.write("{:2d} seconds remaining.".format(remaining))
    sys.stdout.flush()
    time.sleep(1)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


while True:
  check()
  countdown()
  cls()