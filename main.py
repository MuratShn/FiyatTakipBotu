import requests 
from bs4 import BeautifulSoup as bs
import smtplib
import time

url = "https://www.hepsiburada.com/platoon-3-5-mm-mikrofon-ve-kulaklik-ayirici-splinter-kablo-p-HBV0000081NP6"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}

response = requests.get(url,headers = headers)

def check_price():
    page = requests.get(url,headers = headers)
    soup = bs(page.content,"html.parser")
    price = soup.find("span",{"data-bind": "text: product().currentListing.currentPriceBeforePoint + ',' + product().currentListing.currentPriceAfterPoint"}).get_text().strip()
    title = soup.find("h1",{"id": "product-name"}).get_text().strip()
    price = float(price.replace(",","."))    
    
    if(price < 15):
        send_mail(title)
        return True
        
def send_mail(title):
    sender = "" #mail sahibi
    receiver = "" #ileticilecek mail
    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        server.login(sender,"***") #sender sifresi
        subject ="istedigin fiyata dustu"
        body = "bu linkten gidebilirsin =>" + url
        mailContent = f"to:{receiver}\nFrom:{sender}\nSubject:{subject}\n\n{body}"
        server.sendmail(sender,receiver,mailContent)
        print("Mail gönderildi")
    except smtplib.SMTPException as e  :
        print(e)
    finally:
        server.quit()
        
while(1):
    
    check_price()
    
    if(check_price() == True):
        break
    
    time.sleep(60+60) #1 saatte bir
    
