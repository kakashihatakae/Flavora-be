from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from database import get_db
from typing import Annotated
from Models.User import User
from sqlalchemy.orm import Session
from Auth.AuthController import authenticate_request
from Profile import CRUD
from Profile.ProfileSchema import UserInformation, ImageUrl

ProfileRouter = APIRouter()


@ProfileRouter.get("/profile/info")
async def getUserInformation(
    user: Annotated[User, Depends(authenticate_request)], db: Session = Depends(get_db)
):
    user_dict = {}
    for key in user.__dict__:
        if key not in ["password", "id", "role", "email", "image"]:
            user_dict[key] = user.__dict__[key]
    hasAddress = (
        user.name
        and user.addressLine1
        and user.city
        and user.country
        and user.state
        and user.zipCode
    )

    user_dict["hasAddress"] = bool(hasAddress)
    return user_dict


@ProfileRouter.put("/profile/info")
async def updateProfileInfo(
    new_information: UserInformation,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    try:
        await CRUD.update_user_information(
            user_id=user.id, new_user_info=new_information, db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(content={"message": "Successful"}, status_code=200)


@ProfileRouter.get("/profile/image")
async def getUserInformation(
    user: Annotated[User, Depends(authenticate_request)], db: Session = Depends(get_db)
):
    return user.image


@ProfileRouter.put("/profile/image")
async def updateImageUrl(
    image_url: ImageUrl,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    try:
        await CRUD.update_image_url(user_id=user.id, url=image_url.url, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return JSONResponse(content={"message": "Successful"}, status_code=200)
