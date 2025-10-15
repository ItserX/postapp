from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database
import logging
import sys
import os

log_path = "/logs/app.log"
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_path),
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI(title="Simple Blog API")

models.Base.metadata.create_all(bind=database.engine)

@app.get("/posts", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    logging.info(f"Fetched {len(posts)} posts")
    return posts

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db)):
    new_post = models.Post(title=post.title, content=post.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logging.info(f"Created post with id={new_post.id}")
    return new_post
