from flask import Flask, render_template, jsonify, request, abort
from markupsafe import escape

app = Flask(__name__)


# =========================
# DỮ LIỆU SÁCH
# =========================

BOOKS = [
    {
        "id": 1,
        "title": "Lập trình Python",
        "author": "Nguyễn Văn A",
        "year": 2024,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 2,
        "title": "HTML và CSS cơ bản",
        "author": "Trần Văn B",
        "year": 2023,
        "category": "Web",
        "available": True
    },
    {
        "id": 3,
        "title": "JavaScript nâng cao",
        "author": "Lê Văn C",
        "year": 2022,
        "category": "Web",
        "available": False
    },
    {
        "id": 4,
        "title": "Cấu trúc dữ liệu và giải thuật",
        "author": "Phạm Văn D",
        "year": 2024,
        "category": "Lập trình",
        "available": True
    },
    {
        "id": 5,
        "title": "Cơ sở dữ liệu SQL",
        "author": "Hoàng Văn E",
        "year": 2023,
        "category": "Cơ sở dữ liệu",
        "available": False
    }
]


# =========================
# TRANG CHỦ
# =========================

@app.route("/")
def index():
    total_books = len(BOOKS)

    available_books = sum(
        1 for book in BOOKS
        if book["available"]
    )

    return render_template(
        "index.html",
        total_books=total_books,
        available_books=available_books
    )


# =========================
# DANH SÁCH SÁCH
# =========================

@app.route("/books")
def books():
    category = request.args.get("category", "").strip()

    if category:
        filtered_books = [
            book for book in BOOKS
            if book["category"] == category
        ]
    else:
        filtered_books = BOOKS

    categories = sorted(
        set(book["category"] for book in BOOKS)
    )

    return render_template(
        "books.html",
        books=filtered_books,
        categories=categories,
        selected_category=category
    )


# =========================
# CHI TIẾT SÁCH
# =========================

@app.route("/books/<int:book_id>")
def book_detail(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        abort(404)

    return render_template(
        "book_detail.html",
        book=book
    )


# =========================
# API - DANH SÁCH SÁCH
# =========================

@app.route("/api/books")
def api_books():
    return jsonify(BOOKS)


# =========================
# API - CHI TIẾT SÁCH
# =========================

@app.route("/api/books/<int:book_id>")
def api_book_detail(book_id):
    book = next(
        (book for book in BOOKS if book["id"] == book_id),
        None
    )

    if book is None:
        return jsonify({
            "error": f"Không có sách với ID = {book_id}"
        }), 404

    return jsonify(book)


# =========================
# XỬ LÝ 404
# =========================

@app.errorhandler(404)
def page_not_found(error):

    # Nếu URL bắt đầu bằng /api/
    # thì trả JSON
    if request.path.startswith("/api/"):
        return jsonify({
            "error": "Không tìm thấy tài nguyên"
        }), 404

    # Ngược lại trả trang HTML
    return render_template("404.html"), 404


# =========================
# CHẠY APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)