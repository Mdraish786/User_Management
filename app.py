from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pymysql

app = FastAPI()

# Templates & Static Files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Database Connection
def get_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="raish9934",  # Replace with your MySQL password
        database="userdb",
        cursorclass=pymysql.cursors.DictCursor
    )


# Home Page
@app.get("/")
async def home(request: Request):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "users": users
        }
    )


# Add User
@app.post("/add-user")
async def add_user(
    name: str = Form(...),
    email: str = Form(...)
):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        (name, email)
    )
   
@app.get("/delete/{user_id}")
async def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = %s",
        (user_id,)
    )

    conn.commit()
    conn.close()

    return RedirectResponse(url="/", status_code=303)