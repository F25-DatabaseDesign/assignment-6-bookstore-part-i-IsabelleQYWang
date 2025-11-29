from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


app = Flask(__name__)
app.secret_key = "secretkey123"

categories = [
    {
        "id": 1,
        "name": "Classic Detective Fiction",
        "image": "category1.jpg",
        "blurb": (
            "Golden-age mysteries and noir staples starring legendary sleuths."
        ),
    },
    {
        "id": 2,
        "name": "Modern Crime",
        "image": "category2.jpg",
        "blurb": (
            "Contemporary suspense novels with gripping plots and complex characters."
        ),
    },
    {
        "id": 3,
        "name": "Police Procedurals",
        "image": "category3.jpg",
        "blurb": (
            "Detailed investigations following law enforcement through complex cases."
        ),
    },
    {
        "id": 4,
        "name": "Cozy Mysteries",
        "image": "category4.jpg",
        "blurb": (
            "Charming whodunits with amateur sleuths and delightful settings."
        ),
    },
]

books = [
    {
        "id": 1,
        "categoryId": 1,
        "title": "The Maltese Falcon",
        "author": "Dashiell Hammett",
        "isbn": "9780679722649",
        "price": 15.99,
        "image": "maltese_falcon.jpg",
        "readNow": True,
    },
    {
        "id": 2,
        "categoryId": 1,
        "title": "Murder on the Orient Express",
        "author": "Agatha Christie",
        "isbn": "9780062693662",
        "price": 13.5,
        "image": "orient_express.jpg",
        "readNow": False,
    },
    {
        "id": 3,
        "categoryId": 1,
        "title": "The Big Sleep",
        "author": "Raymond Chandler",
        "isbn": "9780394758282",
        "price": 14.75,
        "image": "big_sleep.jpg",
        "readNow": True,
    },
    {
        "id": 4,
        "categoryId": 1,
        "title": "The Hound of the Baskervilles",
        "author": "Arthur Conan Doyle",
        "isbn": "9780451528018",
        "price": 9.99,
        "image": "hound_baskervilles.jpg",
        "readNow": False,
    },
    {
        "id": 5,
        "categoryId": 2,
        "title": "The Girl with the Dragon Tattoo",
        "author": "Stieg Larsson",
        "isbn": "9780307269751",
        "price": 16.99,
        "image": "dragon_tattoo.jpg",
        "readNow": True,
    },
    {
        "id": 6,
        "categoryId": 2,
        "title": "Gone Girl",
        "author": "Gillian Flynn",
        "isbn": "9780307588371",
        "price": 15.99,
        "image": "gone_girl.jpg",
        "readNow": False,
    },
    {
        "id": 7,
        "categoryId": 2,
        "title": "The Reversal",
        "author": "Michael Connelly",
        "isbn": "9780316069489",
        "price": 14.99,
        "image": "the_reversal.jpg",
        "readNow": True,
    },
    {
        "id": 8,
        "categoryId": 2,
        "title": "The Snowman",
        "author": "Jo Nesbø",
        "isbn": "9780307270603",
        "price": 16.50,
        "image": "snowman_nesbo.jpg",
        "readNow": False,
    },
    {
        "id": 9,
        "categoryId": 3,
        "title": "Blue Blood",
        "author": "Edward Conlon",
        "isbn": "9780312424111",
        "price": 17.99,
        "image": "blue_blood.jpg",
        "readNow": True,
    },
    {
        "id": 10,
        "categoryId": 3,
        "title": "A Great Deliverance",
        "author": "Elizabeth George",
        "isbn": "9780553278021",
        "price": 15.50,
        "image": "great_deliverance.jpg",
        "readNow": False,
    },
    {
        "id": 11,
        "categoryId": 3,
        "title": "I Am Pilgrim",
        "author": "Terry Hayes",
        "isbn": "9781439177723",
        "price": 18.99,
        "image": "i_am_pilgrim.jpg",
        "readNow": True,
    },
    {
        "id": 12,
        "categoryId": 3,
        "title": "The Black Echo",
        "author": "Michael Connelly",
        "isbn": "9780316154079",
        "price": 14.75,
        "image": "black_echo.jpg",
        "readNow": False,
    },
    {
        "id": 13,
        "categoryId": 4,
        "title": "Still Life",
        "author": "Louise Penny",
        "isbn": "9780312541538",
        "price": 15.99,
        "image": "still_life.jpg",
        "readNow": True,
    },
    {
        "id": 14,
        "categoryId": 4,
        "title": "The Sweetness at the Bottom of the Pie",
        "author": "Alan Bradley",
        "isbn": "9780385342308",
        "price": 14.50,
        "image": "sweetness_pie.jpg",
        "readNow": False,
    },
    {
        "id": 15,
        "categoryId": 4,
        "title": "A Deadly Inside Scoop",
        "author": "Abby Collette",
        "isbn": "9780593098160",
        "price": 16.99,
        "image": "deadly_inside_scoop.jpg",
        "readNow": True,
    },
    {
        "id": 16,
        "categoryId": 4,
        "title": "Death by Darjeeling",
        "author": "Laura Childs",
        "isbn": "9780425185446",
        "price": 13.99,
        "image": "death_by_darjeeling.jpg",
        "readNow": False,
    },
]


def find_category(category_id: int):
    return next((c for c in categories if c["id"] == category_id), None)


def get_cart_count():
    """Get the total number of items in the cart."""
    if "cart" not in session:
        session["cart"] = {}
    return sum(session["cart"].values())


@app.context_processor
def inject_global_vars():
    """Make cart_count and categories available to all templates."""
    return dict(cart_count=get_cart_count(), categories=categories)


@app.route("/")
def home():
    """Landing page listing categories."""
    return render_template("index.html", categories=categories)


@app.route("/category/<int:categoryId>")
def category(categoryId):
    """Display all books for the selected category."""
    selected_category = find_category(categoryId)
    if selected_category is None:
        abort(404)

    selected_books = [book for book in books if book["categoryId"] == categoryId]
    return render_template(
        "category.html",
        categories=categories,
        books=selected_books,
        selectedCategory=categoryId,
        selectedCategoryDetails=selected_category,
    )


@app.route("/search", methods=["GET", "POST"])
def search():
    """Placeholder search that routes visitors back to the matching category."""
    query = ""
    if request.method == "POST":
        query = request.form.get("search", "").strip()
    else:
        query = request.args.get("q", "").strip()

    if query:
        match = next(
            (
                book
                for book in books
                if query.lower() in book["title"].lower()
            ),
            None,
        )
        if match:
            return redirect(url_for("category", categoryId=match["categoryId"]))

    return redirect(url_for("home"))


@app.route("/add-to-cart/<int:bookId>", methods=["POST"])
def add_to_cart(bookId):
    """Add a book to the cart."""
    if "cart" not in session:
        session["cart"] = {}
    
    book = next((b for b in books if b["id"] == bookId), None)
    if book:
        if str(bookId) in session["cart"]:
            session["cart"][str(bookId)] += 1
        else:
            session["cart"][str(bookId)] = 1
        session.modified = True
    
    book_obj = next((b for b in books if b["id"] == bookId), None)
    if book_obj:
        return redirect(url_for("category", categoryId=book_obj["categoryId"]))
    return redirect(url_for("home"))


@app.errorhandler(Exception)
def handle_error(e):
    """Render a helpful error page while keeping the shared layout intact."""
    return (
        render_template("error.html", error=e, categories=categories),
        getattr(e, "code", 500),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
