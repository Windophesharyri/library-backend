from psycopg2 import *
from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
from pydantic import *

from datetime import *

from typing import Optional
# uvicorn server:app --reload

postgre = connect(dbname="newlibr", host="127.0.0.1", user="postgres", password="1234", port="5432")
cursor = postgre.cursor()

app = FastAPI(
    title="Library",
    description="Backend for DB library",
    version='1.0',
    openapi_tags=[
        {
            "name": "Authors",
            "description": "All endpoints related to author table"
        },
        {
            "name": "BookGenres",
            "description": "All endpoints related to book_genres table"
        },
        {
            "name": "Books",
            "description": "All endpoints related to books table"
        },
        {
            "name": "Genres",
            "description": "All endpoints related to genres table"
        },
        {
            "name": "Readers",
            "description": "All endpoints related to readers table"
        },
        {
            "name": "Process",
            "description": "All endpoints related to give_process table"
        },
    ]
)

origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/authors/get", tags = ["Authors"])
async def get_authors():
    try:
        allData = []
        queries = ['SELECT * FROM authors']
        for query in queries:
            cursor.execute(query)
            for row in cursor:
                element = []
                element.append(f'id: {row[0]}')
                element.append(f'name: {row[1]}')
                element.append(f'birthday: {row[2]}')
                allData.append(element)
        return allData
    except Error as e:
        print(e)
        postgre.rollback()

@app.post('/authors/post', tags = ["Authors"])
async def post_author(name: str, birthday: str):
    try:
        FORMAT = '%Y-%m-%d'
        readyDate = datetime.strptime(birthday, FORMAT).date()
        try:
            cursor.execute(f'CALL create_author(\'{name}\'::VARCHAR, \'{readyDate}\'::DATE)')
        except Error as e:
            print(f'Error drop: {e}')
    except Error as e:
        print(e)
        postgre.rollback()


@app.get('/books/get', tags = ["Books"])
async def get_books():
    try:
        allData = []
        queries = ['SELECT * FROM books']
        for query in queries:
            cursor.execute(query)
            for row in cursor.fetchall():
                print(row)
                element = []
                element.append(f'id: {row[0]}')
                element.append(f'title: {row[1]}')
                element.append(f'storage_count: {row[2]}')
                if row[3]:
                    cursor.execute(f'SELECT a.name FROM authors a JOIN books b ON b.author_id = a.author_id WHERE {row[3]} = b.author_id LIMIT 1')
                    for rowS in cursor:
                        element.append(f'author: {" ".join(rowS)}')
                element.append(f'pic: {row[4]}')
                allData.append(element)

        return allData
    except Error as e:
        print(e)
        postgre.rollback()

class NewBook(BaseModel):
    book: str
    storage_count: int
    author: str
    picture: str
#title: str, storage_count: int, author: str
@app.post('/books/post', tags = ["Books"])
async def post_book(item: NewBook):
    try:
        cursor.execute(f'CALL create_book(\'{item.book}\'::VARCHAR, \'{item.storage_count}\'::INT, \'{item.author}\'::VARCHAR, \'{item.picture}\'::TEXT)')
    except Error as e:
        print(e)
        postgre.rollback()


@app.get('/genres/get', tags = ["Genres"])
async def get_genres():
    try:
        allData = []
        queries = ['SELECT * FROM genres']
        for query in queries:
            cursor.execute(query)
            for row in cursor:
                element = []
                element.append(f'id: {row[0]}')
                element.append(f'name: {row[1]}')
                element.append(f'description: {row[2]}')
                allData.append(element)
        return allData
    except Error as e:
        print(e)
        postgre.rollback()

@app.post('/genres/post', tags = ["Genres"])
async def post_genre(name: str, description: Optional[str] = 'NULL'):
    try:
        if (description == 'NULL'):
            cursor.execute(f'CALL create_genre(\'{name}\'::VARCHAR, {description}::VARCHAR)')
        else:
            cursor.execute(f'CALL create_genre(\'{name}\'::VARCHAR, \'{description}\'::VARCHAR)')
    except Error as e:
        print(e)
        postgre.rollback()


@app.get('/readers/get', tags = ["Readers"])
async def get_readers():
    try:
        allData = []
        queries = ['SELECT * FROM readers']
        for query in queries:
            cursor.execute(query)
            for row in cursor:
                element = []
                element.append(f'id: {row[0]}')
                element.append(f'surname: {row[1]}')
                element.append(f'name: {row[2]}')
                element.append(f'patronymic: {row[3]}')
                element.append(f'passport: {row[4]}')
                element.append(f'passport_source: {row[5]}')
                element.append(f'phone: {row[6]}')
                allData.append(element)
        return allData
    except Error as e:
        print(e)
        postgre.rollback()

@app.post('/readers/post', tags = ["Readers"])
async def post_reader(surname: str, name: str, patronymic: str, passport: int, passport_source: str, phone: str):
    try:
        cursor.execute(f'CALL create_reader(\'{surname}\'::VARCHAR, \'{name}\'::VARCHAR, \'{patronymic}\'::VARCHAR, \'{passport}\'::BIGINT, \'{passport_source}\'::VARCHAR, \'{phone}\'::VARCHAR)')
    except Error as e:
        print(f'Error drop: {e}')


@app.get('/booksTOgenres/get', tags = ["BookGenres"])
async def get_booksTOgenres():
    allData = []
    humanData = []
    query = 'SELECT * FROM book_genres'
    cursor.execute(query)
    for row in cursor:
        allData.append(row)

    for listData in allData:
        element = []
        if listData[0]:
            cursor.execute(f'SELECT b.title FROM books b JOIN book_genres bg ON bg.book_id = b.book_id WHERE {listData[0]} = bg.book_id LIMIT 1')
            for row in cursor:
                element.append(f'book: {" ".join(row)}')
        if listData[1]:
            cursor.execute(f'SELECT g.name FROM genres g JOIN book_genres bg ON bg.genre_id = g.genre_id WHERE {listData[1]} = bg.genre_id LIMIT 1')
            for row in cursor:
                element.append(f'genre: {" ".join(row)}')
        humanData.append(element)
        continue
    return humanData

@app.post('/booksTOgenres/post', tags = ["BookGenres"])
async def post_booksTOgenres(book: str, genre: str):
    try:
        cursor.execute(f'CALL create_book_genres(\'{book}\'::VARCHAR, \'{genre}\'::VARCHAR)')
    except Error as e:
        print(f'Error drop: {e}')


@app.get('/give_process/get', tags = ["Process"])
async def get_give_process():
    allData = []
    humanData = []
    query = 'SELECT * FROM give_process'
    cursor.execute(query)
    for row in cursor:
        allData.append(row)

    for listData in allData:
        element = []
        element.append(f'id: {listData[0]}')
        if listData[1]:
            cursor.execute(f'SELECT b.title FROM books b JOIN give_process gp ON gp.book_id = b.book_id WHERE {listData[1]} = gp.book_id LIMIT 1')
            for row in cursor:
                element.append(f'book: {" ".join(row)}')

        if listData[2]:
            cursor.execute(f'SELECT CONCAT(r.surname, \' \', r.name, \' \', r.patronymic) AS full_name FROM readers r JOIN give_process gp ON gp.reader_id = r.reader_id WHERE {listData[2]} = gp.reader_id LIMIT 1')
            
            for row in cursor:
                element.append(f'reader: {" ".join(row)}')
        element.append(f'date_given: {listData[3]}')
        if (len(listData) == 7):
            element.append(f'date_return: {listData[4]}')
            element.append(f'returned: {listData[5]}')              
            element.append(f'days: {listData[6]}')
        else:
            element.append(f'returned: {listData[4]}')
            element.append(f'days: {listData[5]}')
        humanData.append(element)
        continue
    return humanData

class NewProcess(BaseModel):
    book: str
    surname: str
    name: str
    patronymic: str
    due: int

@app.post('/give_process/post', tags = ["Process"])
async def post_process(item: NewProcess):
    try:
        cursor.execute(f'CALL create_processs(\'{item.book}\'::VARCHAR, \'{item.surname}\'::VARCHAR, \'{item.name}\'::VARCHAR, \'{item.patronymic}\'::VARCHAR, \'{item.due}\'::INT)')
    except Error as e:
        print(f'Error drop: {e}')

class changeProcess(BaseModel):
    id: int
@app.post('/give_process/change', tags = ["Process"])
async def change_process(item: NewProcess):
    try:
        cursor.execute(f'CALL change_processs(\'{item.id}\'::INT)')
    except Error as e:
        print(f'Error drop: {e}')