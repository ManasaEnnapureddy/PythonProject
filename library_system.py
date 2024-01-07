from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn

    def display_info(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class EBook(Book):
    def __init__(self, title, author, isbn, file_format):
        super().__init__(title, author, isbn)
        self.file_format = file_format

    def display_info(self):
        return f"{super().display_info()} - Format: {self.file_format}"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_all_books(self):
        return [book.display_info() for book in self.books]

    def search_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book.display_info()
        raise HTTPException(status_code=404, detail="Book not found")

    def delete_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                self.books.remove(book)
                return {"message": f"Book with ISBN {isbn} deleted successfully"}
        raise HTTPException(status_code=404, detail="Book not found")

library_instance = Library()

@app.post("/add_book")
def add_book(title: str, author: str, isbn: str, file_format: str = None):
    if file_format:
        new_book = EBook(title=title, author=author, isbn=isbn, file_format=file_format)
    else:
        new_book = Book(title=title, author=author, isbn=isbn)

    library_instance.add_book(new_book)
    return {"message": "Book added successfully"}

@app.get("/list_books")
def list_books():
    return library_instance.display_all_books()


@app.get("/search_book/{title}")
def search_book(title: str):
    return library_instance.search_book_by_title(title)

@app.delete("/delete_book/{isbn}")
def delete_book(isbn: str):
    return library_instance.delete_book_by_isbn(isbn)


if __name__ == "__main__":
    uvicorn.run("library_system:app", host="127.0.0.1", port=8000, reload=True)

