from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
import json
from typing import Annotated

from Models.User import User
from Auth.AuthController import authenticate_request
from Order.OrderSchema import OrderSchema
from Order import CRUD

# TODO: add name of business
# add image of business
# on vendor portal !!
# formate new menu time to local time, store unix time ?

OrderRouter = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@OrderRouter.post("/order/order")
async def startANewOrder(
    order: OrderSchema,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    try:
        new_order = await CRUD.add_new_order(
            menu_id=order.menu_id, user_id=user.id, order_mode=order.order_mode, db=db
        )

        await CRUD.add_items_new_order(
            items=order.items, order_id=new_order.order_id, db=db
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to insert order items in order-item mapping and/or new order in db. url: order/order, Error: {e}",
        )
    return JSONResponse(content={"message": "Successful"}, status_code=200)


@OrderRouter.get("/order/order/{menuId}")
async def getAllOrdersForMenuId(
    menuId: int,
    user: Annotated[User, Depends(authenticate_request)],
    db: Session = Depends(get_db),
):
    # TODO
    return await CRUD.get_all_orders_by_menu_id(menu_id=menuId, db=db)


@OrderRouter.get("/order/order")
async def getOrderByUserId(
    user: Annotated[User, Depends(authenticate_request)], db: Session = Depends(get_db)
):
    return await CRUD.get_all_orders_by_user_id(user_id=user.id, db=db)
