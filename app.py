from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Ashreddy@123",
    database="electrician_connect"
)

# Home Login Page
@app.route('/')
def home():
    return render_template("login.html")


# Login Validation
@app.route('/login', methods=['POST'])
def login():

    email = request.form['email']
    password = request.form['password']

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=%s AND password=%s",
        (email, password)
    )

    user = cur.fetchone()

    if user:
        return redirect('/dashboard')
    else:
        return "Invalid Email or Password"


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(name,email,phone,password) VALUES(%s,%s,%s,%s)",
            (name, email, phone, password)
        )

        conn.commit()

        return redirect('/')

    return render_template("register.html")


# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# Electricians
@app.route('/electricians')
def electricians():

    cur = conn.cursor()

    cur.execute("SELECT * FROM electricians")

    data = cur.fetchall()

    return render_template(
        "electricians.html",
        electricians=data
    )


# Book Service
# Book Service
@app.route('/book', methods=['GET', 'POST'])
def book():

    electrician_name = request.args.get('electrician', '')

    if request.method == 'POST':

        user_name = request.form['user_name']
        electrician_name = request.form['electrician_name']
        service_type = request.form['service_type']

        cur = conn.cursor()

        cur.execute(
            "INSERT INTO bookings(user_name,electrician_name,service_type,status) VALUES(%s,%s,%s,%s)",
            (user_name, electrician_name, service_type, "Pending")
        )

        conn.commit()

        return f"""
        <html>
        <head>
        <title>Booking Successful</title>
        <style>
        body {{
            font-family: Arial;
            background:#f4f6f9;
            text-align:center;
            padding-top:100px;
        }}

        .box {{
            background:white;
            width:500px;
            margin:auto;
            padding:30px;
            border-radius:15px;
            box-shadow:0px 2px 10px rgba(0,0,0,0.2);
        }}

        button {{
            background:#0d6efd;
            color:white;
            border:none;
            padding:12px 25px;
            border-radius:5px;
        }}
        </style>
        </head>

        <body>

        <div class="box">

        <h1 style="color:green;">✅ Booking Successful</h1>

        <p><b>Customer:</b> {user_name}</p>
        <p><b>Electrician:</b> {electrician_name}</p>
        <p><b>Service:</b> {service_type}</p>
        <p><b>Status:</b> Pending</p>

        <br>

        <a href="/dashboard">
        <button>Back Dashboard</button>
        </a>

        </div>

        </body>
        </html>
        """

    return render_template(
        "booking.html",
        electrician_name=electrician_name
    )
# Tool Rental
@app.route('/tools')
def tools():

    cur = conn.cursor()

    cur.execute("SELECT * FROM tools")

    data = cur.fetchall()

    return render_template(
        "tools.html",
        tools=data
    )


# Product Store
@app.route('/products')
def products():

    cur = conn.cursor()

    cur.execute("SELECT * FROM products")

    data = cur.fetchall()

    return render_template(
        "products.html",
        products=data
    )


# Tutorials
@app.route('/tutorials')
def tutorials():
    return render_template("tutorials.html")


# AI Assistant
# AI Assistant
@app.route('/assistant', methods=['GET', 'POST'])
def assistant():

    answer = ""

    if request.method == 'POST':

        question = request.form['question'].lower()

        if "switch" in question:
            answer = "Before installing a switch, always turn OFF the main power supply and use insulated tools."

        elif "fan" in question:
            answer = "Ensure the fan is securely mounted and all wiring connections are properly insulated."

        elif "safety" in question:
            answer = "Always switch OFF the main supply, wear safety gloves, and never touch exposed wires."

        elif "wiring" in question:
            answer = "Use the correct wire gauge, proper insulation, and avoid overloading circuits."

        elif "mcb" in question:
            answer = "MCB protects electrical circuits from overloads and short circuits."

        elif "shock" in question:
            answer = "Turn off power immediately and avoid touching the victim directly. Use a non-conductive object."

        elif "earthing" in question:
            answer = "Proper earthing protects people and equipment from electrical faults and leakage currents."

        elif "fuse" in question:
            answer = "A fuse protects electrical devices by breaking the circuit when excess current flows."

        else:
            answer = "I can help with wiring, switches, fans, MCBs, fuses, earthing, electrical safety, and troubleshooting."

    return render_template(
        "assistant.html",
        answer=answer
    )
    # Order Page
@app.route('/order/<item_name>', methods=['GET', 'POST'])
def order(item_name):

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        phone = request.form['phone']
        address = request.form['address']
        payment_method = request.form['payment_method']

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO orders
            (customer_name, phone, address, item_name, payment_method, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                customer_name,
                phone,
                address,
                item_name,
                payment_method,
                "Confirmed"
            )
        )

        conn.commit()

        return render_template(
            "success.html",
            item=item_name,
            customer=customer_name
        )

    return render_template(
        "order.html",
        item=item_name
    )

# Add To Cart

@app.route('/add_to_cart/<item_name>/<int:price>')
def add_to_cart(item_name, price):

    cur = conn.cursor()

    cur.execute(
        "INSERT INTO cart(item_name,price) VALUES(%s,%s)",
        (item_name, price)
    )

    conn.commit()

    return redirect('/cart')


# View Cart

@app.route('/cart')
def cart():

    cur = conn.cursor()

    cur.execute("SELECT * FROM cart")

    items = cur.fetchall()

    return render_template(
        "cart.html",
        items=items
    )
if __name__ == "__main__":
    app.run(debug=True)