from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database
import logging
import sys
import os

app_log_dir = "/logs/app"
db_log_dir = "/logs/db"
os.makedirs(app_log_dir, exist_ok=True)
os.makedirs(db_log_dir, exist_ok=True)

app_log_path = os.path.join(app_log_dir, "app.log")
db_log_path = os.path.join(db_log_dir, "db.log")

app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)

app_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app_file_handler = logging.FileHandler(app_log_path)
app_file_handler.setFormatter(app_formatter)
app_console_handler = logging.StreamHandler(sys.stdout)
app_console_handler.setFormatter(app_formatter)

app_logger.addHandler(app_file_handler)
app_logger.addHandler(app_console_handler)

db_logger_names = [
    "sqlalchemy.engine",
    "sqlalchemy.pool",
    "sqlalchemy.orm"
]

db_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
db_file_handler = logging.FileHandler(db_log_path)
db_file_handler.setFormatter(db_formatter)
db_console_handler = logging.StreamHandler(sys.stdout)
db_console_handler.setFormatter(db_formatter)

for name in db_logger_names:
    logger = logging.getLogger(name)

    if name == "sqlalchemy.engine":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(db_file_handler)
    logger.addHandler(db_console_handler)

app = FastAPI(title="Simple Blog API")

models.Base.metadata.create_all(bind=database.engine)

@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    app_logger.info(f"Fetched {len(posts)} posts")
    return posts

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    app_logger.info(f"Created post with id={new_post.id}")
    return new_post
