from sqlalchemy.orm import Session
from Models import User
from Auth.AuthSchemas import UserSchema

# from Auth import models
# from Auth.AuthSchemas import User


def create_user(db: Session, user: UserSchema):
    hashed_password = user.password
    new_user = User.User(email=user.email, password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    return new_user


def get_user_by_email(db: Session, email: str, role: str):
    current_user = db.query(User.User).filter_by(email=email, role=role).first()
    return current_user
