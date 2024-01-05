from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"},
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": books})

# Get book by id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):  # Add book_id as a parameter
    for book in books:
        if book['id'] == book_id:
            return jsonify({"book": book})
    return {'error': 'Book not found'}

#create a book
@app.route('/books', methods=['POST'])
def create_book():
    new_book={'id':len(books)+1, 'title': request.json['title'], 'author': request.json['author']}
    books.append(new_book)
    return new_book

#update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['title'] = request.json.get('title', book['title'])
            book['author'] = request.json.get('author', book['author'])
            return jsonify({"book": book})
    return {'error': 'book not found'}

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {'data': 'book deleted successfully'}
    return {'error': 'book not found'}

# Run the flask app
if __name__ == '__main__':
    app.run(debug=True)
