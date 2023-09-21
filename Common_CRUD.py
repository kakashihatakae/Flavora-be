from sqlalchemy.orm import Session
from Models import User, Items
from typing import List


def get_user_by_email(email: str, db: Session):
    current_user = db.query(User.User).filter_by(email=email).first()
    return current_user


def get_all_items(user_id: str, item_ids: List[int], db: Session):
    return (
        db.query(Items.Items)
        .filter(Items.Items.item_owner_id == user_id, Items.Items.item_id.in_(item_ids))
        .all()
    )
