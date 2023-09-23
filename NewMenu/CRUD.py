from sqlalchemy.orm import Session, load_only
from Models import Menus, Items
from typing import List
from NewMenu.schemas import NewMenu, NewItem


async def add_new_menu(NewMenu: NewMenu, menu_owner_id: int, db: Session):
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


async def add_new_item(NewItem: NewItem, item_owner_id: int, db: Session):
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
