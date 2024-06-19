from flask import Flask, render_template, request
import requests
from datetime import date

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    req = requests.get("https://fakestoreapi.com/products")
    products = req.json()
    return render_template('home.html', products=products)


@app.get('/shop_now')
def shop_now():
    id = request.args.get('id')
    req = requests.get(f'https://fakestoreapi.com/products/{id}')
    product = req.json()
    return render_template('shopnow.html', product=product)


@app.get('/check_out')
def check_out():
    id = request.args.get('id')
    req = requests.get(f'https://fakestoreapi.com/products/{id}')
    product = req.json()
    return render_template('checkout.html', product=product)


@app.post('/confirmBooking')
def confirmBooking():
    p_id = request.form.get('p_id')
    name = request.form.get('name')
    telephone = request.form.get('telephone')
    email = request.form.get('email')
    address = request.form.get('address')
    req = requests.get(f'https://fakestoreapi.com/products/{p_id}')
    product = req.json()

    msg = (
        "<strong>New Confirm Booking 🔔</strong>\n"
        "<code>Name: {name}</code>\n"
        "<code>Telephone: {telephone}</code>\n"
        "<code>Email: {email}</code>\n"
        "<code>Address: {address}</code>\n"
        "<code>Booking Date📆: {date}</code>\n"
        "<code>============================</code>\n"
        "<code>1. {product_name} 1x${price}</code>\n"
    ).format(
        name=name,
        telephone=telephone,
        email=email,
        address=address,
        date=date.today(),
        product_name=product['title'],
        price=product['price']+2)

    sendNotify(msg)
    return render_template('confirmBooking.html', name=name, telephone=telephone, email=email, address=address,
                           product=product)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html')


def sendNotify(msg):
    bot_token = "6929981912:AAHx8Ks5oN57LcpJ8lTI_TK_paE-Qz_kOs0"
    chat_id = "@ss25bots"
    html = requests.utils.quote(msg)
    telegram = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={html}&parse_mode=HTML"
    res = requests.get(telegram)
    return res


if __name__ == '__main__':
    app.run()
