from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'pricetracker123'

# Helper function to connect to database
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ─────────────────────────────
# HOME PAGE
# ─────────────────────────────
@app.route('/')
def home():
    return render_template('login.html')

# ─────────────────────────────
# CUSTOMER REGISTER
# ─────────────────────────────
@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']

        db = get_db()
        try:
            db.execute('INSERT INTO users (name, email, password, location) VALUES (?, ?, ?, ?)',
                      (name, email, password, location))
            db.commit()
            return redirect(url_for('login_user'))
        except:
            return 'Email already exists! Go back and try again.'
        finally:
            db.close()

    return render_template('register_user.html')

# ─────────────────────────────
# CUSTOMER LOGIN
# ─────────────────────────────
@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                         (email, password)).fetchone()
        db.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = 'user'
            return redirect(url_for('user_dashboard'))
        else:
            return 'Wrong email or password! Go back and try again.'

    return render_template('login_user.html')

# ─────────────────────────────
# CUSTOMER DASHBOARD
# ─────────────────────────────
@app.route('/user/dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login_user'))
    return render_template('user_dashboard.html',
                           user_name=session['user_name'],
                           results=None,
                           query=None)

# ─────────────────────────────
# CUSTOMER SEARCH
# ─────────────────────────────
@app.route('/user/search', methods=['POST'])
def user_search():
    if session.get('role') != 'user':
        return redirect(url_for('login_user'))

    query = request.form['query']

    db = get_db()

    # Save search history
    db.execute('INSERT INTO search_history (user_id, search_term) VALUES (?, ?)',
              (session['user_id'], query))
    db.commit()

    # Search products by name or category
    results = db.execute('''
        SELECT * FROM products
        WHERE (name LIKE ? OR category LIKE ? OR description LIKE ?)
        AND stock_status != "out_of_stock"
        ORDER BY price ASC
    ''', (f'%{query}%', f'%{query}%', f'%{query}%')).fetchall()

    db.close()

    return render_template('user_dashboard.html',
                           user_name=session['user_name'],
                           results=results,
                           query=query)
# ─────────────────────────────
# SHOP REGISTER
# ─────────────────────────────
@app.route('/register/shop', methods=['GET', 'POST'])
def register_shop():
    if request.method == 'POST':
        shop_name = request.form['shop_name']
        owner_name = request.form['owner_name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        category = request.form['category']

        db = get_db()
        try:
            db.execute('''INSERT INTO shops 
                         (shop_name, owner_name, email, password, phone, address, category)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (shop_name, owner_name, email, password, phone, address, category))
            db.commit()
            return redirect(url_for('login_shop'))
        except:
            return 'Email already exists! Go back and try again.'
        finally:
            db.close()

    return render_template('register_shop.html')

# ─────────────────────────────
# SHOP LOGIN
# ─────────────────────────────
@app.route('/login/shop', methods=['GET', 'POST'])
def login_shop():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        shop = db.execute('SELECT * FROM shops WHERE email = ? AND password = ?',
                         (email, password)).fetchone()
        db.close()

        if shop:
            if shop['status'] == 'pending':
                return 'Your shop is still pending admin approval!'
            session['shop_id'] = shop['id']
            session['shop_name'] = shop['shop_name']
            session['role'] = 'shop'
            return redirect(url_for('shop_dashboard'))
        else:
            return 'Wrong email or password! Go back and try again.'

    return render_template('login_shop.html')

# ─────────────────────────────
# SHOP DASHBOARD
# ─────────────────────────────
@app.route('/shop/dashboard')
def shop_dashboard():
    if session.get('role') != 'shop':
        return redirect(url_for('login_shop'))

    db = get_db()
    products = db.execute('SELECT * FROM products WHERE shop_id = ?',
                         (session['shop_id'],)).fetchall()
    total_products    = len(products)
    available_products= len([p for p in products if p['stock_status'] == 'available'])
    out_of_stock      = len([p for p in products if p['stock_status'] == 'out_of_stock'])
    db.close()

    return render_template('shop_dashboard.html',
                           shop_name=session['shop_name'],
                           products=products,
                           total_products=total_products,
                           available_products=available_products,
                           out_of_stock=out_of_stock)

# ─────────────────────────────
# SHOP ADD PRODUCT
# ─────────────────────────────
@app.route('/shop/add-product', methods=['POST'])
def shop_add_product():
    if session.get('role') != 'shop':
        return redirect(url_for('login_shop'))

    name         = request.form['name']
    price        = request.form['price']
    category     = request.form['category']
    stock_status = request.form['stock_status']
    description  = request.form['description']

    db = get_db()
    shop = db.execute('SELECT * FROM shops WHERE id = ?',
                     (session['shop_id'],)).fetchone()
    db.execute('''INSERT INTO products
                 (name, price, category, stock_status, description,
                  store_name, store_type, shop_id)
                 VALUES (?, ?, ?, ?, ?, ?, "offline", ?)''',
              (name, price, category, stock_status, description,
               shop['shop_name'], session['shop_id']))
    db.commit()
    db.close()
    return redirect(url_for('shop_dashboard'))

# ─────────────────────────────
# SHOP UPDATE STOCK
# ─────────────────────────────
@app.route('/shop/stock/<int:product_id>/out', methods=['POST'])
def mark_out_of_stock(product_id):
    if session.get('role') != 'shop':
        return redirect(url_for('login_shop'))
    db = get_db()
    db.execute('UPDATE products SET stock_status = "out_of_stock" WHERE id = ?',
              (product_id,))
    db.commit()
    db.close()
    return redirect(url_for('shop_dashboard'))

@app.route('/shop/stock/<int:product_id>/in', methods=['POST'])
def mark_available(product_id):
    if session.get('role') != 'shop':
        return redirect(url_for('login_shop'))
    db = get_db()
    db.execute('UPDATE products SET stock_status = "available" WHERE id = ?',
              (product_id,))
    db.commit()
    db.close()
    return redirect(url_for('shop_dashboard'))
# ─────────────────────────────
# ADMIN LOGIN
# ─────────────────────────────
@app.route('/login/admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Admin credentials hardcoded for now
        if email == 'admin@pricetracker.com' and password == 'admin123':
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Wrong admin credentials! Go back and try again.'

    return render_template('login_admin.html')

# ─────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    
    db = get_db()
    shops    = db.execute('SELECT * FROM shops').fetchall()
    products = db.execute('SELECT * FROM products').fetchall()
    total_users    = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    total_shops    = db.execute('SELECT COUNT(*) FROM shops').fetchone()[0]
    total_products = db.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    pending_shops  = db.execute('SELECT COUNT(*) FROM shops WHERE status = "pending"').fetchone()[0]
    db.close()

    return render_template('admin_dashboard.html',
                           shops=shops,
                           products=products,
                           total_users=total_users,
                           total_shops=total_shops,
                           total_products=total_products,
                           pending_shops=pending_shops)

# ─────────────────────────────
# ADMIN APPROVE SHOP
# ─────────────────────────────
@app.route('/admin/approve/<int:shop_id>', methods=['POST'])
def approve_shop(shop_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    db = get_db()
    db.execute('UPDATE shops SET status = "approved" WHERE id = ?', (shop_id,))
    db.commit()
    db.close()
    return redirect(url_for('admin_dashboard'))

# ─────────────────────────────
# ADMIN REJECT SHOP
# ─────────────────────────────
@app.route('/admin/reject/<int:shop_id>', methods=['POST'])
def reject_shop(shop_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login_admin'))
    db = get_db()
    db.execute('UPDATE shops SET status = "rejected" WHERE id = ?', (shop_id,))
    db.commit()
    db.close()
    return redirect(url_for('admin_dashboard'))

# ─────────────────────────────
# ADMIN ADD ONLINE PRODUCT
# ─────────────────────────────
@app.route('/admin/add-product', methods=['POST'])
def admin_add_product():
    if session.get('role') != 'admin':
        return redirect(url_for('login_admin'))

    name         = request.form['name']
    price        = request.form['price']
    category     = request.form['category']
    store_name   = request.form['store_name']
    delivery_days= request.form['delivery_days']
    description  = request.form['description']

    db = get_db()
    db.execute('''INSERT INTO products 
                 (name, price, category, store_name, store_type, delivery_days, description)
                 VALUES (?, ?, ?, ?, "online", ?, ?)''',
              (name, price, category, store_name, delivery_days, description))
    db.commit()
    db.close()
    return redirect(url_for('admin_dashboard'))
# ─────────────────────────────
# LOGOUT
# ─────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
