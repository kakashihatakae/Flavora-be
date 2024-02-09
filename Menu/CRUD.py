from sqlalchemy.orm import Session, load_only
from Models import Menus, Items, User
from typing import List
from Menu.schemas import MenuSchema, ItemSchema
from sqlalchemy import desc
from datetime import datetime


async def add_new_menu(NewMenu: MenuSchema, menu_owner_id: int, db: Session):
    new_menu = Menus.Menus(
        menu_owner_id=menu_owner_id,
        order_deadline=NewMenu.order_deadline,
        delivery_estimate=NewMenu.delivery_estimate,
        title=NewMenu.title,
    )
    db.add(new_menu)
    db.flush()
    db.commit()
    return new_menu


async def get_all_menus(menu_owner_id: int, db: Session):
    return (
        db.query(Menus.Menus)
        .filter_by(menu_owner_id=menu_owner_id)
        .options(
            load_only(
                Menus.Menus.order_deadline,
                Menus.Menus.delivery_estimate,
                Menus.Menus.menu_id,
                Menus.Menus.title,
            )
        )
        .all()
    )


async def add_items_new_menu(item_ids: List[int], menu_id: str, db: Session):
    for item_id in item_ids:
        menu_item_mapping = Menus.MenuItems(menu_id=menu_id, item_id=item_id)
        db.add(menu_item_mapping)
    db.commit()


async def add_new_item(NewItem: ItemSchema, item_owner_id: int, db: Session):
    new_item = Items.Items(
        image=NewItem.image,
        price=NewItem.price,
        item_owner_id=item_owner_id,
        name=NewItem.name,
    )
    db.add(new_item)
    db.flush()
    db.commit()
    return new_item


async def get_all_items(item_owner_id: str, db: Session):
    return (
        db.query(Items.Items)
        .filter(Items.Items.item_owner_id == item_owner_id)
        .options(
            load_only(
                Items.Items.image,
                Items.Items.item_id,
                Items.Items.name,
                Items.Items.price,
            )
        )
        .all()
    )


async def get_all_active_menus(db: Session):
    now = datetime.now().timestamp()
    results = (
        db.query(
            Menus.Menus.delivery_estimate,
            Menus.Menus.order_deadline,
            Menus.Menus.title,
            Menus.Menus.menu_id,
            User.User.name,
            User.User.image,
            User.User.delivery,
            User.User.pickup,
        )
        .filter(Menus.Menus.menu_owner_id == User.User.id)
        .all()
    )
    return [result._asdict() for result in results if result.order_deadline > now]


async def get_all_items_in_active_menu(menu_id: int, db: Session):
    items = (
        db.query(Items.Items)
        .join(Menus.MenuItems)
        .filter(Menus.MenuItems.menu_id == menu_id)
        .options(
            load_only(
                Items.Items.image,
                Items.Items.item_id,
                Items.Items.name,
                Items.Items.price,
            )
        )
    ).all()
    vendor_information = (
        db.query(User.User)
        .join(Menus.Menus)
        .filter(Menus.Menus.menu_id == menu_id)
        .options(
            load_only(
                User.User.image,
                User.User.name,
                User.User.delivery,
                User.User.pickup,
                User.User.addressLine1,
                User.User.addressLine2,
                User.User.city,
                User.User.state,
                User.User.country,
                User.User.zipCode,
            )
        )
    ).first()
    return {"items": items, "vendorInfo": vendor_information}
