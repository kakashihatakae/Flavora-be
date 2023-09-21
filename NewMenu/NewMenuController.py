from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from Models import User, Items, Menus
from NewMenu.schemas import NewItem, NewMenu
import Common_CRUD as COMCR
import NewMenu.CRUD as NewMenuCRUD
import json


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


# TODO: check roles
@NewMenuRouter.post("/menu/menu")
async def createNewMenu(NewMenu: NewMenu, db: Session = Depends(get_db)):
    # to be added
    # menu_owner_id: user who is addeing this.
    # we will get user info through auth
    menu_owner_id = 1  # TODO: Change
    try:
        new_menu = await NewMenuCRUD.add_new_menu(
            NewMenu=NewMenu, menu_owner_id=menu_owner_id, db=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert new menu in db. url: menu/newmenu, Error: {e}",
        )

    # add items to MenuItems Table
    # get menu id from the above operations
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
async def getAllMenus(db: Session = Depends(get_db)):
    user_id = 1
    return await NewMenuCRUD.get_all_menus(menu_owner_id=user_id, db=db)


@NewMenuRouter.post("/menu/newitem")
async def createNewItem(NewItem: NewItem, db: Session = Depends(get_db)):
    item_owner_id = 1  # TODO: Change
    try:
        new_added_item = await NewMenuCRUD.add_new_item(
            NewItem=NewItem, item_owner_id=item_owner_id, db=db
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert items in db. url:menu/newitem , Error: {e}",
        )
    print(new_added_item.item_id)
    return new_added_item


@NewMenuRouter.get("/menu/getallitems")
async def getAllItems(db: Session = Depends(get_db)):
    item_owner_id = 1  # TODO: Change
    try:
        items = await NewMenuCRUD.get_all_items(item_owner_id=item_owner_id, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to get items. url:/menu/getallitems .Error: {e}",
        )
    return items
