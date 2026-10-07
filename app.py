from flask import Flask, jsonify, request, render_template
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Chỉ khởi tạo app 1 lần duy nhất
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'app', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'app', 'static')
)

# Sử dụng đường dẫn tương đối để chạy chuẩn cả ở máy thật lẫn Docker container
DATA_FILE = os.path.join(BASE_DIR, 'app', 'data', 'students.json')


def load_students():
    # Kiểm tra nếu chưa có file hoặc thư mục thì tự động tạo file rỗng
    if not os.path.exists(DATA_FILE):
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_students(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =========================
# C1 - WEB
# =========================

@app.route("/")
def index():
    students = load_students()
    return render_template("index.html", students=students)


# =========================
# C2 - API GET
# =========================

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "student": os.getenv("MSSV", "2412111021")
    })


@app.route("/api/students")
def students():
    data = load_students()
    lop = request.args.get("lop")

    if lop:
        data = [s for s in data if str(s.get("lop")) == str(lop)]

    return jsonify(data)


@app.route("/api/students/<int:id>")
def student(id):
    data = load_students()

    for s in data:
        if s.get("id") == id:
            return jsonify(s)

    return jsonify({
        "error": "Not found"
    }), 404


# =========================
# C3 - API POST
# =========================

@app.route("/api/students", methods=["POST"])
def add_student():
    body = request.get_json(silent=True)

    # Không có JSON
    if not body:
        return jsonify({
            "error": "invalid JSON"
        }), 400

    # Kiểm tra trường bắt buộc
    required = [
        "mssv",
        "ho_ten",
        "lop",
        "diem"
    ]

    for field in required:
        if field not in body:
            return jsonify({
                "error": f"missing field: {field}"
            }), 400

    # Kiểm tra điểm
    try:
        diem = float(body["diem"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "diem must be a number"
        }), 400

    if diem < 0 or diem > 10:
        return jsonify({
            "error": "invalid score"
        }), 400

    # Đọc danh sách sinh viên
    students_list = load_students()

    # Tạo ID tự động
    if students_list:
        new_id = max(s.get("id", 0) for s in students_list) + 1
    else:
        new_id = 1

    body["id"] = new_id
    body["diem"] = diem

    # Thêm sinh viên
    students_list.append(body)

    # Lưu file JSON
    save_students(students_list)

    # HTTP 201
    return jsonify(body), 201


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port
    )