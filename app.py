from flask import Flask, render_template, request

app = Flask(__name__)

# app.py
sheets = [
    {
        "id": 1,
        "title": "TWS - 내가 S면 넌 나의 N이 되어줘",
        "composer": "TWS",
        "price": 4000,
        "image": "if-im-s-can-you-be-my-n.png",
        "pdf": "TWS - 내가 S면 넌 나의 N이 되어줘.pdf"
    },
    {
        "id": 2,
        "title": "TWS (투어스) -  첫 만남은 계획대로 되지 않아",
        "composer": "TWS",
        "price": 4000,
        "image": "Plot twist.png",
        "pdf": "TWS (투어스) -  첫 만남은 계획대로 되지 않아.pdf"
    }
]

# 악보
@app.route('/sheet/<int:sheet_id>')
def sheet_detail(sheet_id):
    sheet = next((s for s in sheets if s["id"] == sheet_id), None)
    if not sheet:
        return "악보를 찾을 수 없습니다.", 404
    return render_template('sheet_detail.html', sheet=sheet)

# 홈
@app.route('/')
def home():
    return render_template('index.html', sheets=sheets)

# ✅ 결제 페이지
@app.route('/pay')
def pay():
    sheet_id = request.args.get("sheet_id", type=int)
    sheet = next((s for s in sheets if s["id"] == sheet_id), None)
    if not sheet:
        return "악보를 찾을 수 없습니다.", 404
    return render_template('pay.html', sheet=sheet)

# ✅ 결제 성공 페이지
@app.route('/success')
def success():
    sheet_id = request.args.get("sheet_id", type=int)
    sheet = next((s for s in sheets if s["id"] == sheet_id), None)
    if not sheet:
        return "결제 정보가 잘못되었습니다.", 404
    return render_template('success.html', sheet=sheet)

# ✅ pdf 남용 방지
@app.route('/download')
def download():
    filename = request.args.get("filename")
    # 보안을 위해 파일 이름을 sheets 목록에서만 허용
    allowed_files = [s["pdf"] for s in sheets]
    if filename not in allowed_files:
        return "허용되지 않은 파일입니다.", 403
    return send_from_directory('static/files', filename, as_attachment=True)

# ✅ 반드시 마지막에 있어야 함!
if __name__ == '__main__':
    app.run(debug=True)