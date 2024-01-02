import sqlite3
from datetime import datetime

class LibraryManagementSystem:
    def __init__(self, database_name='library.db'):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                available_quantity INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def display_books(self):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        if books:
            print("\nLibrary Catalog:")
            for book in books:
                print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Quantity: {book[4]}, Available Quantity: {book[5]}")
        else:
            print("\nNo books available in the library.")

    def add_book(self, title, author, isbn, quantity):
        available_quantity = quantity
        self.cursor.execute('''
            INSERT INTO books (title, author, isbn, quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, isbn, quantity, available_quantity))
        self.conn.commit()
        print(f"\n'{title}' by {author} added to the library.")

    def borrow_book(self, book_id):
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = self.cursor.fetchone()

        if book and book[5] > 0:
            self.cursor.execute('UPDATE books SET available_quantity = ? WHERE id = ?', (book[5] - 1, book_id))
            self.conn.commit()
            print("\nBook borrowed successfully.")
        else:
            print("\nBook not available for borrowing.")

    def return_book(self, book_id):
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = self.cursor.fetchone()

        if book:
            self.cursor.execute('UPDATE books SET available_quantity = ? WHERE id = ?', (book[5] + 1, book_id))
            self.conn.commit()
            print("\nBook returned successfully.")
        else:
            print("\nInvalid book ID. Book not found.")

    def close_connection(self):
        self.conn.close()

def main():
    library = LibraryManagementSystem()

    while True:
        print("\nLibrary Management System Menu:")
        print("1. Display Books")
        print("2. Add Book")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            library.display_books()
        elif choice == '2':
            title = input("Enter book title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            quantity = int(input("Enter quantity: "))
            library.add_book(title, author, isbn, quantity)
        elif choice == '3':
            book_id = int(input("Enter ID of the book to borrow: "))
            library.borrow_book(book_id)
        elif choice == '4':
            book_id = int(input("Enter ID of the book to return: "))
            library.return_book(book_id)
        elif choice == '5':
            library.close_connection()
            print("\nExiting the Library Management System. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
