from flask import Flask, jsonify, request, render_template
import json
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'app', 'templates'))

DATA_FILE = "/home/dell/dg1_2412111021/app/data/students.json"


def load_students():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_students(data):
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
# RUN SERVER
# =========================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )