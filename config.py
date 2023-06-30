PRODUCTS_TO_TRACK = []

link=input("Enter Product Link: ")
p_id=''
lIndex=int(link.find("dp/"))
rIndex=int(link.find("?"))
for i in range(lIndex+3, rIndex):
    p_id+=link[i]


prod = p_id
PRODUCTS_TO_TRACK.append(prod)
FROM_EMAIL_ID = "authenticator.api@gmail.com"
FROM_EMAIL_ID_PASSWORD = "generate app password for your mail id and paste it here "

TO_EMAIL_ID = "Enter your email here"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
