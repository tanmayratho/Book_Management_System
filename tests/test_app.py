import pytest
from sqlalchemy.future import select
from ..app import  db, create_app
from ..app.models import User
from ..app.routes import Book


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+asyncpg://postgres:postgres@123@localhost:5432/book_management_system'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


@pytest.mark.asyncio
async def test_user_registration(app, client):
    response = await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'User created successfully'}

    async with app.db_session() as session:
        result = await session.execute(select(User).filter_by(username='testuser'))
        user = result.scalar_one_or_none()
        assert user is not None
        assert user.username == 'testuser'


@pytest.mark.asyncio
async def test_user_login(app, client):
    await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'token' in response.json


@pytest.mark.asyncio
async def test_create_book(app, client):
    await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.json['token']

    response = await client.post('/books', json={
        'title': 'Book',
        'author': 'Author',
        'genre': 'Test Genre',
        'year_published': 2023
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 201
    assert 'id' in response.json

    book_id = response.json['id']

    async with app.db_session() as session:
        result = await session.execute(select(Book).filter_by(id=book_id))
        book = result.scalar_one_or_none()
        assert book is not None
        assert book.title == 'Book'
        assert book.author == 'Author'


@pytest.mark.asyncio
async def test_get_book(app, client):

    await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.json['token']

    create_response = await client.post('/books', json={
        'title': 'Book',
        'author': 'Author',
        'genre': 'Genre',
        'year_published': 2023
    }, headers={'Authorization': f'Bearer {token}'})

    book_id = create_response.json['id']

    response = await client.get(f'/books/{book_id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json['title'] == 'Book'
    assert response.json['author'] == 'Author'


@pytest.mark.asyncio
async def test_update_book(app, client):

    await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.json['token']

    create_response = await client.post('/books', json={
        'title': 'Book',
        'author': 'Author',
        'genre': 'Genre',
        'year_published': 2023
    }, headers={'Authorization': f'Bearer {token}'})

    book_id = create_response.json['id']

    response = await client.put(f'/books/{book_id}', json={
        'title': 'Updated  Book',
        'author': 'Updated Author',
        'genre': 'Updated Genre',
        'year_published': 2024,
        'summary': 'This is an updated Book.'
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.json['message'] == 'Book updated successfully'

    get_response = await client.get(f'/books/{book_id}', headers={'Authorization': f'Bearer {token}'})
    assert get_response.json['title'] == 'Updated Book'
    assert get_response.json['author'] == 'Updated Author'


@pytest.mark.asyncio
async def test_delete_book(client):
    await client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    login_response = await client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    token = login_response.json['token']

    create_response = await client.post('/books', json={
        'title': 'Book',
        'author': 'Author',
        'genre': 'Test Genre',
        'year_published': 2023,
        'summary': 'This is a Book.'
    }, headers={'Authorization': f'Bearer {token}'})

    book_id = create_response.json['id']

    response = await client.delete(f'/books/{book_id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 204

    get_response = await client.get(f'/books/{book_id}', headers={'Authorization': f'Bearer {token}'})
    assert get_response.status_code == 404
