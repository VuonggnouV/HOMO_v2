from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify 
from werkzeug.security import generate_password_hash, check_password_hash
import os
from utils.helper import geocode_address, calculate_distance, get_here_api_key
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.secret_key = 'HOMO_exe'  # Thay đổi 'your_secret_key_here' thành một chuỗi ngẫu nhiên và bí mật
#NYMGQFV3ZB7E25YQ4WU26WFW
# Đường dẫn đến tệp người dùng
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'user.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Bảng User (khách hàng)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Bảng Driver (tài xế)
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)  # Loại xe

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_from = db.Column(db.String(255), nullable=False)
    address_to = db.Column(db.String(255), nullable=False)
    support = db.Column(db.String(10), nullable=False)  # "Có" hoặc "Không"
    insurance_value = db.Column(db.String(20), nullable=True)  # Giá trị bảo hiểm
    total_price = db.Column(db.Integer, nullable=False)

class UsedVoucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # Mã order_id đã dùng làm voucher
    
# Tạo database nếu chưa có
with app.app_context():
    db.create_all()

#route
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            error = "Email đã tồn tại. Vui lòng chọn email khác."
            return render_template('register.html', error=error)

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, phone=phone, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        session['username'] = name
        session['user_type'] = 'customer'  # Lưu loại người dùng vào session
        return redirect(url_for('success'))

    return render_template('register.html', error=error)


@app.route("/validate_voucher")
def validate_voucher():
    code = request.args.get("code", "").strip()

    if not code.isdigit():
        return jsonify(valid=False, reason="invalid")

    # Kiểm tra mã có tồn tại trong đơn hàng không
    order = Order.query.filter_by(order_id=code).first()
    if not order:
        return jsonify(valid=False, reason="invalid")

    # Kiểm tra mã đã được sử dụng chưa
    used = UsedVoucher.query.filter_by(code=code).first()
    if used:
        return jsonify(valid=False, reason="used")  # Gửi thêm lý do để JS hiển thị

    return jsonify(valid=True)



@app.route('/success')
def success():
    return render_template('success.html')


# Đăng nhập (cho cả User và Driver)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Kiểm tra trong bảng User trước
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.name
            session['user_type'] = 'customer'
            return redirect(url_for('index'))

        # Kiểm tra trong bảng Driver nếu không tìm thấy trong User
        driver = Driver.query.filter_by(email=email).first()
        if driver and check_password_hash(driver.password, password):
            session['username'] = driver.name
            session['user_type'] = 'driver'
            session['vehicle_type'] = driver.vehicle_type  # Lưu loại xe tài xế vào session
            return redirect(url_for('index'))
        error = "Sai thông tin đăng nhập"

    return render_template('login.html', error=error)


# Đăng ký tài xế
@app.route('/driver_register', methods=['GET', 'POST'])
def driver_register():
    error = None 

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        vehicle_type = request.form['vehicle_type']
        
        if vehicle_type == "ba_gac": 
            vehicle_type = "Ba gác"
        elif vehicle_type == "nho":
            vehicle_type = "Tải nhỏ"
        elif vehicle_type == "trung":
            vehicle_type = "Tải trung"



        if Driver.query.filter_by(email=email).first():
            error = "Email đã tồn tại. Vui lòng chọn email khác."
            return render_template('driver_register.html', error=error)

        hashed_password = generate_password_hash(password)
        new_driver = Driver(name=name, phone=phone, email=email, password=hashed_password, 
                            address=address, vehicle_type=vehicle_type)
        db.session.add(new_driver)
        db.session.commit()

        session['username'] = name
        session['user_type'] = 'driver'
        session['vehicle_type'] = vehicle_type  # Lưu loại xe vào session
        return redirect(url_for('success'))

    return render_template('driver_register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)  # Xóa thông tin tên người dùng khỏi phiên
    return redirect(url_for('index'))  # Chuyển hướng về trang chính


@app.route('/booking')
def booking_page():
    return render_template('booking.html')

@app.route('/booking2')
def booking_page2():
    return render_template('booking2.html')

@app.route('/booking3')
def booking_page3():
    return render_template('booking3.html')


@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    try:
        data = request.json  
        order_id = str(data.get("order_id"))
        name = data.get("name")
        phone = data.get("phone")
        address_from = data.get("from")
        address_to = data.get("to")
        support = "Có" if data.get("support") else "Không"  
        insurance_value = data.get("insurance_type")  # Lưu trực tiếp giá trị bảo hiểm
        total_price = int(data.get("total_price"))

        if not name or not phone or not address_from or not address_to or not total_price:
            return jsonify({"error": "Thiếu thông tin đơn hàng"}), 400

        if Order.query.filter_by(order_id=order_id).first():
            return jsonify({"error": "Mã đơn hàng đã tồn tại"}), 400

        # Lưu đơn hàng mới
        new_order = Order(
            order_id=order_id,
            name=name,
            phone=phone,
            address_from=address_from,
            address_to=address_to,
            support=support,
            insurance_value=insurance_value if insurance_value else None,
            total_price=total_price
        )
        db.session.add(new_order)

        voucher_code = data.get("voucher_code")
        voucher_discount = data.get("voucher_discount", 0)
        if voucher_code and int(voucher_discount) > 0:
            if not UsedVoucher.query.filter_by(code=voucher_code).first():
                db.session.add(UsedVoucher(code=voucher_code))

        db.session.commit()

        return jsonify({"message": "Đặt xe thành công!", "order_id": order_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/address_calculator')
def address_calculator():
    # Lấy tham số từ query string
    address1 = request.args.get('from')
    address2 = request.args.get('to')

    if not address1 or not address2:
        return jsonify({"error": "Thiếu tham số 'from' hoặc 'to'"}), 400

    # Geocode địa chỉ
    coord1 = geocode_address(address1)
    coord2 = geocode_address(address2)

    if not coord1 or not coord2:
        return jsonify({"error": "Không thể tìm thấy tọa độ từ địa chỉ"}), 400

    # Tính khoảng cách và thời gian
    distance, duration = calculate_distance(coord1, coord2)

    if not distance or not duration:
        return jsonify({"error": "Không thể tính toán khoảng cách"}), 400

    # Trả về kết quả dưới dạng JSON
    return jsonify({
        "distance": distance,
        "duration": duration
    })


@app.route("/address_suggestions")
def address_suggestions():
    query = request.args.get("query")
    if not query or len (query)<20:
        return jsonify([])

    HERE_API_KEY = get_here_api_key()  # Lấy API Key từ helper.py
    url = f"https://autocomplete.search.hereapi.com/v1/autocomplete?q={query}&apiKey={HERE_API_KEY}&lang=vi"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        suggestions = [item["address"]["label"] for item in data.get("items", [])]
        return jsonify(suggestions)
    else:
        return jsonify([]), 500



if __name__ == '__main__':
    app.run(debug=True)
