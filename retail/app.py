from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ambikha_retail_secret_key'

# Sample product database
products = {
    'laptop': {'name': 'Laptop', 'price': 999.99, 'stock': 10},
    'phone': {'name': 'Smartphone', 'price': 499.99, 'stock': 20},
    'headphones': {'name': 'Wireless Headphones', 'price': 99.99, 'stock': 50},
    'tablet': {'name': 'Tablet', 'price': 299.99, 'stock': 15},
    'watch': {'name': 'Smartwatch', 'price': 199.99, 'stock': 25}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        search_term = request.form.get('search', '').lower()

        # Handle product search
        if search_term in products:
            session['last_search'] = search_term
            return render_template('product.html',
                                  product=products[search_term],
                                  product_id=search_term)
        else:
            # Return template with specific error ID for test verification
            return render_template('product.html', error='product_not_found')

    return render_template('product.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 0))

    # Validate quantity
    if quantity <= 0:
        # Return template with specific error ID for test verification
        return render_template('product.html',
                              product=products.get(product_id),
                              product_id=product_id,
                              error='invalid_quantity')

    # Check if product exists
    if product_id not in products:
        return render_template('product.html', error='product_not_found')

    # Check stock
    if quantity > products[product_id]['stock']:
        return render_template('product.html',
                              product=products[product_id],
                              product_id=product_id,
                              error='out_of_stock')

    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = {}

    # Add to cart
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity

    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0

    if 'cart' in session:
        for product_id, quantity in session['cart'].items():
            if product_id in products:
                item = products[product_id]
                subtotal = item['price'] * quantity
                cart_items.append({
                    'id': product_id,
                    'name': item['name'],
                    'price': item['price'],
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal

    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/checkout', methods=['POST'])
def checkout():
    # Check if cart is empty
    if 'cart' not in session or not session['cart']:
        return render_template('cart.html', error='empty_cart')

    # Simulate crash for testing
    if request.form.get('simulate_crash') == 'true':
        return render_template('error.html', error='checkout_error')

    # Check stock availability
    for product_id, quantity in session['cart'].items():
        if product_id not in products or products[product_id]['stock'] < quantity:
            return render_template('cart.html', error='out_of_stock')

    # Update stock
    for product_id, quantity in session['cart'].items():
        products[product_id]['stock'] -= quantity

    # Clear cart after successful checkout
    session.pop('cart', None)
    return redirect(url_for('index'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

# Add a route to simulate out of stock scenario for testing
@app.route('/simulate_out_of_stock', methods=['POST'])
def simulate_out_of_stock():
    product_id = request.form.get('product_id')
    if product_id in products:
        products[product_id]['stock'] = 0
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)