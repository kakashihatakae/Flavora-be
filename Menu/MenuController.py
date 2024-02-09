from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from Models import Items, Menus
from Models.User import User
from Menu.schemas import ItemSchema, MenuSchema
import Common_CRUD as COMCR
import Menu.CRUD as NewMenuCRUD
import json
from Auth.AuthController import authenticate_request
from typing import Annotated

# TODO: add name of business
# add image of business
# on vendor portal !!
# formate new menu time to local time, store unix time ?

NewMenuRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @NewMenuRouter.get("/")
# async def temp(
#     db: Session = Depends(get_db),
# ):
#     u = User.User(
#         role=User.Roles.USER,
#         name="Shreyas",
#         email="shreyasb2@gmail.com",
#         password="1234",
#     )
#     db.add(u)
#     db.flush()
#     it = Items.Items(image="", price=3, item_owner_id=u.id)
#     db.add(it)
#     db.commit()
#     return ""
# u = User(user_name=u'dusual')
# u.clients.append(Client(orgname="dummy_org"))


@NewMenuRouter.post("/menu/menu")
async def createNewMenu(
    NewMenu: MenuSchema,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    try:
        new_menu = await NewMenuCRUD.add_new_menu(
            NewMenu=NewMenu, menu_owner_id=user.id, db=db
        )
    except Exception as e:
        print("New menu fail")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert new menu in db. url: menu/newmenu, Error: {e}",
        )

    try:
        await NewMenuCRUD.add_items_new_menu(
            item_ids=NewMenu.item_ids, menu_id=new_menu.menu_id, db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert menu items in menu-item mapping. url: menu/newmenu, Error: {e}",
        )
    return JSONResponse(content={"message": "Successful"}, status_code=200)


@NewMenuRouter.get("/menu/menu")
async def getAllMenus(
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    return await NewMenuCRUD.get_all_menus(menu_owner_id=user.id, db=db)


@NewMenuRouter.post("/menu/newitem")
async def createNewItem(
    NewItem: ItemSchema,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    try:
        new_added_item = await NewMenuCRUD.add_new_item(
            NewItem=NewItem, item_owner_id=user.id, db=db
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert items in db. url:menu/newitem , Error: {e}",
        )
    print(new_added_item.item_id, new_added_item.name, new_added_item.price)
    return new_added_item


@NewMenuRouter.get("/menu/getallitems")
async def getAllItems(
    user: Annotated[User, Depends(authenticate_request)], db: Session = Depends(get_db)
):
    try:
        items = await NewMenuCRUD.get_all_items(item_owner_id=user.id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to get items. url:/menu/getallitems .Error: {e}",
        )
    return items


# --- mobile


@NewMenuRouter.get("/menu/active")
async def getAllActiveMenus(
    user: Annotated[User, Depends(authenticate_request)], db: Session = Depends(get_db)
):
    return await NewMenuCRUD.get_all_active_menus(db=db)


@NewMenuRouter.get("/menu/active/items/{menu_id}")
async def getAllItemsInAMenu(
    user: Annotated[User, Depends(authenticate_request)],
    menu_id: int,
    db: Session = Depends(get_db),
):
    try:
        items = await NewMenuCRUD.get_all_items_in_active_menu(menu_id=menu_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get items. url:/menu/active/items .Error: {e}",
        )
    return items
