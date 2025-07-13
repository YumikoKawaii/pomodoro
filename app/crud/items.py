from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.models import Item
from app.models.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 100, is_active: Optional[bool] = None) -> List[Item]:
    query = db.query(Item)
    if is_active is not None:
        query = query.filter(Item.is_active == is_active)
    return query.offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate) -> Item:
    db_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        is_active=item.is_active
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True


def get_items_count(db: Session, is_active: Optional[bool] = None) -> int:
    query = db.query(Item)
    if is_active is not None:
        query = query.filter(Item.is_active == is_active)
    return query.count()