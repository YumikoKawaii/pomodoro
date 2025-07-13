from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from app.db.models import Task, User
from app.models.task import TaskCreate, TaskUpdate, TaskPriority, TaskStatus


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Get a single task by ID with user information"""
    return db.query(Task).options(joinedload(Task.user)).filter(Task.id == task_id).first()


def get_tasks(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        category: Optional[str] = None,
        search: Optional[str] = None
) -> List[Task]:
    """Get tasks with filtering options"""
    query = db.query(Task).options(joinedload(Task.user))

    # Apply filters
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    if status is not None:
        query = query.filter(Task.status == status)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    if category is not None:
        query = query.filter(Task.category == category)

    if search:
        # Search in title and description
        search_filter = or_(
            Task.title.ilike(f"%{search}%"),
            Task.description.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    return query.offset(skip).limit(limit).all()


def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    """Get all tasks for a specific user"""
    return db.query(Task).options(joinedload(Task.user)).filter(
        Task.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_tasks_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        user_id: Optional[int] = None
) -> List[Task]:
    """Get tasks within a date range"""
    query = db.query(Task).options(joinedload(Task.user))

    # Filter by date range (using start_time or created_at)
    date_filter = or_(
        and_(Task.start_time >= start_date, Task.start_time <= end_date),
        and_(Task.start_time.is_(None), Task.created_at >= start_date, Task.created_at <= end_date)
    )
    query = query.filter(date_filter)

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    return query.all()


def create_task(db: Session, task: TaskCreate) -> Task:
    """Create a new task"""
    # Verify user exists
    user = db.query(User).filter(User.id == task.user_id).first()
    if not user:
        raise ValueError(f"User with id {task.user_id} not found")

    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        user_id=task.user_id,
        start_time=task.start_time,
        end_time=task.end_time,
        category=task.category
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Load the task with user relationship
    return db.query(Task).options(joinedload(Task.user)).filter(Task.id == db_task.id).first()


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """Update an existing task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    # If user_id is being updated, verify the new user exists
    if "user_id" in update_data:
        user = db.query(User).filter(User.id == update_data["user_id"]).first()
        if not user:
            raise ValueError(f"User with id {update_data['user_id']} not found")

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)

    # Return task with user relationship
    return db.query(Task).options(joinedload(Task.user)).filter(Task.id == task_id).first()


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


def get_tasks_count(
        db: Session,
        user_id: Optional[int] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None
) -> int:
    """Get total count of tasks with optional filters"""
    query = db.query(Task)

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    if status is not None:
        query = query.filter(Task.status == status)

    if priority is not None:
        query = query.filter(Task.priority == priority)

    return query.count()


def mark_task_completed(db: Session, task_id: int) -> Optional[Task]:
    """Mark a task as completed"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        return None

    db_task.status = TaskStatus.COMPLETED
    if not db_task.end_time:
        db_task.end_time = datetime.utcnow()

    db.commit()
    db.refresh(db_task)

    return db.query(Task).options(joinedload(Task.user)).filter(Task.id == task_id).first()


def get_overdue_tasks(db: Session, user_id: Optional[int] = None) -> List[Task]:
    """Get tasks that are overdue (end_time has passed and status is not completed)"""
    now = datetime.utcnow()
    query = db.query(Task).options(joinedload(Task.user)).filter(
        and_(
            Task.end_time < now,
            Task.status != TaskStatus.COMPLETED,
            Task.status != TaskStatus.CANCELLED
        )
    )

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    return query.all()


def get_tasks_by_priority(db: Session, priority: TaskPriority, user_id: Optional[int] = None) -> List[Task]:
    """Get all tasks with a specific priority"""
    query = db.query(Task).options(joinedload(Task.user)).filter(Task.priority == priority)

    if user_id is not None:
        query = query.filter(Task.user_id == user_id)

    return query.all()