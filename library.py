from werkzeug import url_decode
from flask import Flask, render_template, request, redirect, url_for, flash

class MethodRewriteMiddleware(object):
    """Middleware for HTTP method rewriting.

    Snippet: http://flask.pocoo.org/snippets/38/
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)

class Book(object):
    """A Fake model"""

    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

@app.route('/books')
def list_books():
    """GET /books

    Lists all books"""
    books = [ Book(id=1, name=u'Lord of the rings'), Book(id=2, name=u'Dive into Python') ] # Your query here ;)
    return render_template('list_books.html', books=books)

@app.route('/books/<id>')
def show_book(id):
    """GET /books/<id>

    Get a book by its id"""
    book = Book(id=id, name=u'My great book') # Your query here ;)
    return render_template('show_book.html', book=book)

@app.route('/books/new')
def new_book():
    """GET /books/new

    The form for a new book"""
    return render_template('new_book.html')

@app.route('/books', methods=['POST',])
def create_book():
    """POST /books

    Receives a book data and saves it"""
    name = request.form['name']
    book = Book(id=2, name=name) # Save it
    flash('Book %s sucessful saved!' % book.name)
    return redirect(url_for('show_book', id=2))

@app.route('/books/<id>/edit')
def edit_book(id):
    """GET /books/<id>/edit

    Form for editing a book"""
    book = Book(id=id, name=u'Something crazy') # Your query
    return render_template('edit_book.html', book=book)

@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    """PUT /books/<id>

    Updates a book"""
    book = Book(id=id, name=u"I don't know") # Your query
    book.name = request.form['name'] # Save it
    flash('Book %s updated!' % book.name)
    return redirect(url_for('show_book', id=book.id))

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    """DELETE /books/<id>

    Deletes a books"""
    book = Book(id=id, name=u"My book to be deleted") # Your query
    flash('Book %s deleted!' % book.name)
    return redirect(url_for('list_books'))

if __name__ == '__main__':
    app.run()
