# Book_Management_System
Book Management System API Documentation Guide

This is a backend application which allows management of books and reviews . Users can register, log in, and perform CRUD operations on books and reviews. JWT tokens are used for authentication.
The application has the following functionalities:

    - User Registration: Register a new user.
    - User Login: Log in a user and return a JWT token.
    - Get All Books: Retrieve a list of all books.
    - Get Specific Book: Retrieve a specific book by its ID.
    - Create New Book: Add a new book to the database.
    - Update Book: Update the details of an existing book.
    - Delete Book: Delete a book from the database.
    - Get All Reviews: Retrieve all reviews for a specific book.
    - Add Review: Add a review to a specific book.

Authentication:

Endpoints except /register and /login require a valid JWT token.
User Registration and Login:

Register a New User

URL: /register
Method: POST
Request Body:
json
 
{
  "username": "string",
  "password": "string"
}
Responses:
201 Created: User registered successfully.
400 Bad Request: Username already exists.
Log in a User

URL: /login
Method: POST
Request Body:
json
 
{
  "username": "string",
  "password": "string"
}
Responses:
200 OK: Returns a JWT token.
401 Unauthorized: Invalid username or password.
Book Management:

Get All Books

URL: /books
Method: GET
Responses:
200 OK: Returns a list of books.
Get a Specific Book

URL: /books/{book_id}
Method: GET
Responses:
200 OK: Returns the book details.
404 Not Found: Book not found.
Create a New Book

URL: /books
Method: POST
Request Body:
json
 
{
  "title": "string",
  "author": "string",
  "genre": "string",
  "year_published": 2023
}
Responses:
201 Created: Book added successfully.
Update a Book

URL: /books/{book_id}
Method: PUT
Request Body:
json
 
{
  "title": "string",
  "author": "string",
  "genre": "string",
  "year_published": 2023
}
Responses:
200 OK: Book updated successfully.
404 Not Found: Book not found.
Delete a Book

URL: /books/{book_id}
Method: DELETE
Responses:
204 No Content: Book deleted successfully.
404 Not Found: Book not found.
Review Management:

Get All Reviews for a Book

URL: /books/{book_id}/reviews
Method: GET
Responses:
200 OK: Returns a list of reviews.
404 Not Found: Book not found.
Add a Review to a Book

URL: /books/{book_id}/reviews
Method: POST
Request Body:
json
 
{
  "user_id": 1,
  "review_text": "string",
  "rating": 5
}
Responses:
201 Created: Review added successfully.
404 Not Found: Book not found.