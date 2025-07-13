from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.item import Item, ItemCreate, ItemUpdate
from app.core.database import get_db
from app.crud import items as crud_items

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[Item])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all items with optional filtering and pagination"""
    items = crud_items.get_items(db, skip=skip, limit=limit, is_active=is_active)
    return items

@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific item by ID"""
    db_item = crud_items.get_item(db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Create a new item"""
    return crud_items.create_item(db=db, item=item)

@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing item"""
    db_item = crud_items.update_item(db, item_id=item_id, item_update=item_update)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete an item"""
    success = crud_items.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}

@router.get("/stats/count")
async def get_items_count(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get total count of items"""
    count = crud_items.get_items_count(db, is_active=is_active)
    return {"count": count}