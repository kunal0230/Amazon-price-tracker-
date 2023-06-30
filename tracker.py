

from requests_html import HTMLSession
import json
import smtplib
import time
from config import PRODUCTS_TO_TRACK, FROM_EMAIL_ID, FROM_EMAIL_ID_PASSWORD, TO_EMAIL_ID, SMTP_HOST, SMTP_PORT



def main():


    timeDelay = int(input("Enter Time loop var:"))
    budget = int(input("Enter your Budget: "))




    #Continous checking
    while True:

        s = HTMLSession()

        # ------------ EDIT BELOW THIS LINE ---------------
        products_to_track = PRODUCTS_TO_TRACK
        from_email_id = FROM_EMAIL_ID
        from_email_id_password = FROM_EMAIL_ID_PASSWORD
        to_email_id = TO_EMAIL_ID
        smtp_host = SMTP_HOST
        smtp_port = SMTP_PORT
        # ------------ EDIT ABOVE THIS LINE ---------------

        database = {}
        # Loading database
        print("Loading database...")
        try:
            with open('database.json', 'r+') as f:
                database = json.load(f)
        except:
            print("Couldn't load database! (Database might be empty)")


        # Searching for products
        print("Searching for products...")
        for product in products_to_track:
            link_to_product = f'https://www.amazon.in/dp/{product}'

            r = s.get(link_to_product) # r = response, s = session
            r.html.render(sleep=1)

            try:
                product_name = r.html.find('#productTitle', first=True)
                price = r.html.find('.a-price' '.priceToPay' '> span:nth-child(1)', first=True)

                # If normal price is not available, try to find the offer price
                if (price == None):
                    price = r.html.find('.a-price' '.apexPriceToPay' '> span:nth-child(1)', first=True)
            except:
                pass

            # Formatting data
            product_name = product_name.text.strip()
            # If price is None (product might be unavailable), skip product
            if (price == None):
                print("\nPrice not available! Product might be unavailable. Skipping...")
                continue
            price = price.text.replace(',', '').replace('₹', '').strip()

            print(f"\nFound product {product}!\nProduct Name: {product_name}\nProduct Price: {price}")

            if product in database:

                if (float(price)< float(budget)):
                    print(f'{product_name} price has dropped! Notifying via email...')

                    # Send email notification
                    try:
                        server = smtplib.SMTP(smtp_host, smtp_port)
                        server.starttls() # Secure the connection
                        server.login(from_email_id, from_email_id_password)

                        subject = f"Price drop for {product_name}"
                        body = f"Price of {product_name} has dropped to {price}!\n\nLink to product: {link_to_product}"
                        msg = f"Subject: {subject}\n\n{body}"

                        server.sendmail(from_email_id, to_email_id, msg)
                        print(f"Email notification sent to {to_email_id}!")

                    except Exception as e:
                        print(e)
                    finally:
                        server.quit()
                        return

                if (float(price) < float(database[product]['price'])):

                    print(f'{product_name} price has dropped! Notifying via email...')

                    # Send email notification
                    try:
                        server = smtplib.SMTP(smtp_host, smtp_port)
                        server.starttls() # Secure the connection
                        server.login(from_email_id, from_email_id_password)

                        subject = f"Price drop for {product_name}"
                        body = f"Price of {product_name} has dropped to {price}!\n\nLink to product: {link_to_product}"
                        msg = f"Subject: {subject}\n\n{body}"

                        server.sendmail(from_email_id, to_email_id, msg)
                        print(f"Email notification sent to {to_email_id}!")

                    except Exception as e:
                        print(e)
                    finally:
                        server.quit()
                        return

                else:
                    print("Price hasn't dropped!")
                database[product]['price'] = price # Updating database

            else:
                database[product] = {
                    "product_name": product_name,
                    "price": price
                }
                print("Product added to database...")

        # Dump data to database.json
        with open('database.json', 'w+') as f:
            json.dump(database, f, indent=4)
        print("Sleeping...")
        time.sleep(1*timeDelay)
        print("Awaking...")






main()
exit()
