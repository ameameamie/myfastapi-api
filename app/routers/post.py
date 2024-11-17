from typing import Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('SELECT * FROM posts;')
    # posts = cursor.fetchall()
    # posts = (
    #     db.query(models.Post)
    #     .filter(func.lower(models.Post.title).contains(search.lower()) | func.lower(models.Post.content).contains(search.lower()))
    #     .limit(limit)
    #     .offset(skip)
    #     .all())
    
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(func.lower(models.Post.title).contains(search.lower()) | func.lower(models.Post.content).contains(search.lower()))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute('INSERT INTO posts (title, content, visible) VALUES (%s, %s, %s) RETURNING *;',
    #                (post.title, post.content, post.visible))
    # new_post = cursor.fetchone()
    # connection.commit()
    post = post.model_dump()

    post.update({"author_id": current_user.id})
    new_post = models.Post(**post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(f'SELECT * FROM posts WHERE id = %s ', (id,))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label('votes'))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id).first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found.",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):

    # cursor.execute('DELETE FROM posts WHERE id = %s RETURNING *', (id,))
    # post = cursor.fetchone()
    # connection.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found."
        )

    if current_user.id != post.first().author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't delete other people's posts",
        )

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    # cursor.execute('UPDATE posts SET title = %s, content = %s, visible = %s WHERE id = %s RETURNING *', (post.title, post.content, post.visible, id))
    # post = cursor.fetchone()
    # connection.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post_for_update = post_query.first()

    if post_for_update == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id} found."
        )

    if current_user.id != post_for_update.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't edit other people's posts",
        )

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
