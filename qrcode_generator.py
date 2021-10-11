import qrcode

APP_ORDER_URL = 'http://127.0.0.1:5000/order/'
TABLE_AMOUNT = 15

#Creating an instance of qrcode
qr = qrcode.QRCode(version=1, box_size=10, border=5)

for i in range(TABLE_AMOUNT):
    input_data = f'{APP_ORDER_URL}{i+1}'

    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'app/static/images/qrcode/qrcode{i+1}.png')