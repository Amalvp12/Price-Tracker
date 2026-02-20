# 🏪 Competitor Price Tracking Module

A web application that helps customers compare product prices from both **local offline shops** and **online stores** in one place.

---

## 💡 What Does This App Do?

Instead of checking multiple websites and visiting multiple shops to compare prices, this app does it all in one search.

**Example:** Search "iPhone 17" and instantly see:

| Store | Price | Type | Availability |
|-------|-------|------|-------------|
| Raja Electronics | ₹78,999 | 🏪 Offline | ✅ Available |
| Amazon | ₹79,999 | 🌐 Online | 🚚 2 days delivery |
| Flipkart | ₹81,999 | 🌐 Online | 🚚 3 days delivery |

---

## 🧩 Three Modules

### 1. 👤 User Module (Customer)
- Register and login
- Search products by typing or by **voice**
- Compare prices from offline shops and online stores
- See cheapest price highlighted automatically

### 2. 🏪 Shop Module (Shop Owner)
- Register your shop
- Add products and prices manually
- Update stock status (available / out of stock)
- View your product dashboard

### 3. 🔐 Admin Module
- Approve or reject shop registrations
- Add online store products manually (Amazon, Flipkart, etc.)
- Monitor all users, shops, and products
- View platform statistics

---

## 🎤 Voicebot Feature

Customers can search by speaking instead of typing.

```
Click the 🎤 mic button
Say "Show me Samsung TV"
App automatically searches and shows results
```

Works using the browser's built-in Web Speech API. No extra setup needed.

---

## 🛠️ Tech Stack

| Part | Tool Used |
|------|-----------|
| Backend | Python + Flask |
| Database | SQLite |
| Frontend | HTML + CSS + JavaScript |
| Voicebot | Web Speech API (built into Chrome) |
| Language | Python 3 |

**Everything is 100% free. No paid APIs or services used.**

---

## 📁 Project Structure

```
pricetracker/
│
├── app.py                  ← Main Flask server (brain of the app)
├── database.py             ← Creates all database tables
├── database.db             ← SQLite database file (auto created)
│
├── templates/              ← HTML pages
│   ├── login.html          ← Home page with 3 login options
│   ├── login_user.html     ← Customer login
│   ├── login_shop.html     ← Shop owner login
│   ├── login_admin.html    ← Admin login
│   ├── register_user.html  ← Customer registration
│   ├── register_shop.html  ← Shop owner registration
│   ├── user_dashboard.html ← Customer search page
│   ├── shop_dashboard.html ← Shop owner dashboard
│   └── admin_dashboard.html← Admin dashboard
│
├── static/                 ← CSS and JS files
└── venv/                   ← Python virtual environment
```

---

## ⚙️ How to Install and Run

### Step 1 — Make sure Python is installed
```
python --version
```
Should show Python 3.x

### Step 2 — Clone or download the project folder

### Step 3 — Open terminal inside the project folder

### Step 4 — Create virtual environment
```
python -m venv venv
```

### Step 5 — Activate virtual environment

On Windows:
```
venv\Scripts\activate
```

On Mac/Linux:
```
source venv/bin/activate
```

### Step 6 — Install Flask
```
pip install flask
```

### Step 7 — Create the database
```
python database.py
```

You should see:
```
Database created successfully!
```

### Step 8 — Run the app
```
python app.py
```

### Step 9 — Open in browser
```
http://127.0.0.1:5000
```

---

## 🔑 Login Credentials

### Admin Login
```
Email    → admin@pricetracker.com
Password → admin123
```

### Customer
Register a new account from the home page.

### Shop Owner
Register your shop and wait for admin approval.

---

## 🗄️ Database Tables

| Table | What It Stores |
|-------|----------------|
| users | Customer accounts |
| shops | Shop owner accounts |
| products | All products (offline + online) |
| saved_items | Customer wishlists |
| price_alerts | Price drop notifications |
| search_history | Customer search history |

---

## 🔄 How It Works (Simple Flow)

```
OFFLINE SHOPS
Shop owner registers → Admin approves → Shop adds products → Appears in search

ONLINE STORES
Admin manually adds Amazon/Flipkart products → Appears in search

CUSTOMER
Registers → Searches product → Sees price comparison → Picks best deal
```

---

## ✅ Features Completed

- [x] Customer register and login
- [x] Shop owner register and login
- [x] Admin login
- [x] Shop approval system
- [x] Shop owner product management
- [x] Admin adds online store products
- [x] Product search
- [x] Price comparison
- [x] Cheapest price highlighted
- [x] Voice search (voicebot)
- [x] Admin dashboard with stats

## 🔮 Future Features

- [ ] Price drop alerts (notify when price goes below target)
- [ ] Wishlist / saved items
- [ ] Search history page
- [ ] AI-powered smart recommendations
- [ ] Real online store price scraping

---

## 👨‍💻 Built With

- Python 3
- Flask
- SQLite
- HTML / CSS / JavaScript
- Web Speech API

---

## 📌 Notes

- Voice search works only on **Google Chrome**
- Run the app locally — no internet needed
- All data is stored in `database.db` file on your computer
- To reset everything, delete `database.db` and run `python database.py` again
