from Models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from Profile.ProfileSchema import UserInformation


async def get_user_information(user_id: int, db: Session):
    try:
        db.query(User.User).filter_by(id=user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def update_user_information(
    user_id: int, db: Session, new_user_info: UserInformation
):
    try:
        user_to_be_updated = db.query(User.User).filter_by(id=user_id).first()

        if user_to_be_updated:
            user_to_be_updated.addressLine1 = new_user_info.addressLine1
            user_to_be_updated.addressLine2 = new_user_info.addressLine2
            user_to_be_updated.city = new_user_info.city
            user_to_be_updated.name = new_user_info.name
            user_to_be_updated.state = new_user_info.state
            user_to_be_updated.zipCode = new_user_info.zipCode
            user_to_be_updated.country = new_user_info.country
            user_to_be_updated.delivery = new_user_info.delivery
            user_to_be_updated.pickup = new_user_info.pickup
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Internal Server Error")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def update_image_url(user_id: int, db: Session, url: str):
    try:
        user_to_be_updated = db.query(User.User).filter_by(id=user_id).first()

        if user_to_be_updated:
            user_to_be_updated.image = url
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Internal Server Error")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
