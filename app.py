from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PRODUCTS = [
    {'id': 1, 'name': '商品A', 'price': 1000},
    {'id': 2, 'name': '商品B', 'price': 1500},
    {'id': 3, 'name': '商品C', 'price': 2000},
]


@app.route('/')
def index():
    if 'quantities' not in session:
        session['quantities'] = {str(product['id']): 0 for product in PRODUCTS}  # 商品IDを文字列に変換
    quantities = session['quantities']
    total_sales = sum(quantities[str(product['id'])] * product['price'] for product in PRODUCTS)
    return render_template('sales.html', products=PRODUCTS, quantities=quantities, total_sales=total_sales)

@app.route('/update_quantity/<int:product_id>/<action>')
def update_quantity(product_id, action):
    if 'quantities' not in session:
        session['quantities'] = {str(product['id']): 0 for product in PRODUCTS}  # 商品IDを文字列に変換
    
    product_id_str = str(product_id)  # 商品IDを文字列に変換
    if action == 'increment':
        session['quantities'][product_id_str] += 1
    elif action == 'decrement' and session['quantities'][product_id_str] > 0:
        session['quantities'][product_id_str] -= 1

    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
