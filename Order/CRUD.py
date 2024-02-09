from sqlalchemy.orm import Session, load_only, lazyload, joinedload
from typing import List
from Order.OrderSchema import OrderSchema, OrderedItemSchema
from Models import Orders, Items, User, Menus
from fastapi import HTTPException
from sqlalchemy import desc


async def add_new_order(
    menu_id: int, user_id: int, order_mode: Orders.OrderModes, db: Session
):
    new_order = Orders.Orders(user_id=user_id, menu_id=menu_id, order_mode=order_mode)
    db.add(new_order)
    db.flush()
    # db.commit()
    return new_order


async def add_items_new_order(
    items: List[OrderedItemSchema], order_id: int, db: Session
):
    for item in items:
        order_item_mapping = Orders.OrderedItems(
            item_id=item.item_id, count=item.count, order_id=order_id
        )
        db.add(order_item_mapping)
    # db.commit()


async def get_all_orders_by_menu_id(menu_id: int, db: Session):
    try:
        orders = (
            db.query(Orders.Orders, User.User)
            .join(User.User)
            .filter(
                Orders.Orders.menu_id == menu_id, User.User.id == Orders.Orders.user_id
            )
            .all()
        )

        if not orders:
            return []

        order_list = []
        for order, user in orders:
            ordered_items = (
                db.query(Orders.OrderedItems)
                .filter(Orders.OrderedItems.order_id == order.order_id)
                .all()
            )
            order_list.append((ordered_items, user, order))

        orders_by_menu_id = []
        for ordered_items, user, order in order_list:
            items_json = []
            total_price = 0
            for ordered_item in ordered_items:
                order_id = ordered_item.order_id
                item = (
                    db.query(Items.Items)
                    .filter(Items.Items.item_id == ordered_item.item_id)
                    .first()
                )
                if item:
                    items_json.append(
                        {
                            "item_id": item.item_id,
                            # "price": item.price,
                            "name": item.name,
                            "count": ordered_item.count,
                            "image": item.image,
                        }
                    )
                    total_price += item.price * ordered_item.count

            address_list = []
            for field in [
                user.addressLine1,
                user.addressLine2,
                user.city,
                user.state,
                user.zipCode,
                user.country,
            ]:
                address_list.append(field)

            consumerAddress = ", ".join(address_list)
            order_json = {
                "order_id": order_id,
                "total_price": total_price,
                "items": items_json,
                "consumer_email": user.email,
                "consumer_name": user.name,
                "consumer_address": consumerAddress,
                "order_mode": order.order_mode,
            }
            orders_by_menu_id.append(order_json)

        return orders_by_menu_id

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_all_orders_by_user_id(user_id: int, db: Session):
    try:
        orders = (
            db.query(Orders.Orders, User.User)
            .join(
                Menus.Menus, Orders.Orders.menu_id == Menus.Menus.menu_id
            )  # Join Orders and Menus
            .join(
                User.User, Menus.Menus.menu_owner_id == User.User.id
            )  # Join Menus and User
            .filter(
                Orders.Orders.user_id == user_id,  # Filter by user_id
            )
            .order_by(desc(Orders.Orders.order_date))
            .all()
        )

        if not orders:
            return []

        order_list = []
        for order, user in orders:
            ordered_items = (
                db.query(Orders.OrderedItems)
                .filter(Orders.OrderedItems.order_id == order.order_id)
                .all()
            )
            order_list.append((ordered_items, user, order))

        orders_by_menu_id = []
        for ordered_items, user, order in order_list:
            items_json = []
            total_price = 0
            for ordered_item in ordered_items:
                order_id = ordered_item.order_id
                item = (
                    db.query(Items.Items)
                    .filter(Items.Items.item_id == ordered_item.item_id)
                    .first()
                )
                if item:
                    items_json.append(
                        {
                            "item_id": item.item_id,
                            "price": item.price,
                            "name": item.name,
                            "count": ordered_item.count,
                            "image": item.image,
                        }
                    )
                    total_price += item.price * ordered_item.count
            order_json = {
                "order_id": order.order_id,
                "total_price": total_price,
                "items": items_json,
                "vendor_name": user.name,
                "vendor_email": user.email,
                "order_date": order.order_date,
            }
            orders_by_menu_id.append(order_json)

        return orders_by_menu_id

        return ""
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
