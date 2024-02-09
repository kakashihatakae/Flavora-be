from sqlalchemy.orm import Session
from sqlalchemy.orm import load_only
from Models import User
from Auth.AuthSchemas import UserSchema, ConsumerAccountInfo

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


async def add_consumer_address_name(
    account_info: ConsumerAccountInfo, user: User.User, db: Session
):
    user_to_update = db.query(User.User).filter_by(id=user.id).first()
    user_to_update.name = account_info.name
    user_to_update.addressLine1 = account_info.addressLine1
    user_to_update.addressLine2 = account_info.addressLine2
    user_to_update.city = account_info.city
    user_to_update.state = account_info.state
    user_to_update.zipCode = account_info.zipCode
    user_to_update.country = account_info.country
    db.commit()


async def get_consumer_address_name(user_id: int, db: Session):
    user_to_get = db.query(User.User).filter(User.User.id == user_id).first()

    return {
        "addressLine1": user_to_get.addressLine1,
        "addressLine2": user_to_get.addressLine2,
        "city": user_to_get.city,
        "state": user_to_get.state,
        "zipCode": user_to_get.zipCode,
        "name": user_to_get.name,
    }
