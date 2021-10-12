import qrcode

APP_ORDER_URL = 'https://restaurant-order-app.herokuapp.com/order/'
TABLE_AMOUNT = 15

for i in range(TABLE_AMOUNT):
    #Creating an instance of qrcode
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    input_data = f'{APP_ORDER_URL}{i+1}'

    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f'app/static/images/qrcode/qrcode{i+1}.png')

    input_data = ''