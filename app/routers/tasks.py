from fastapi import APIRouter, HTTPException, Query, Depends, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.task import Task, TaskCreate, TaskUpdate, TaskResponse, TaskPriority, TaskStatus
from app.core.database import get_db
from app.crud import tasks as crud_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
        skip: int = Query(0, ge=0, description="Number of tasks to skip"),
        limit: int = Query(10, ge=1, le=100, description="Maximum number of tasks to return"),
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
        priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
        category: Optional[str] = Query(None, description="Filter by task category"),
        search: Optional[str] = Query(None, description="Search in title and description"),
        db: Session = Depends(get_db)
):
    """Get all tasks with optional filtering and pagination"""
    tasks = crud_tasks.get_tasks(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        status=status,
        priority=priority,
        category=category,
        search=search
    )

    # Format response with user information
    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            user_id=task.user_id,
            start_time=task.start_time,
            end_time=task.end_time,
            category=task.category,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_email=task.user.email if task.user else None,
            user_username=task.user.username if task.user else None
        )
        task_responses.append(task_response)

    return task_responses


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
        task_id: int = Path(..., description="ID of the task to retrieve"),
        db: Session = Depends(get_db)
):
    """Get a specific task by ID"""
    db_task = crud_tasks.get_task(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        priority=db_task.priority,
        status=db_task.status,
        user_id=db_task.user_id,
        start_time=db_task.start_time,
        end_time=db_task.end_time,
        category=db_task.category,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_email=db_task.user.email if db_task.user else None,
        user_username=db_task.user.username if db_task.user else None
    )


@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    try:
        db_task = crud_tasks.create_task(db=db, task=task)

        return TaskResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            priority=db_task.priority,
            status=db_task.status,
            user_id=db_task.user_id,
            start_time=db_task.start_time,
            end_time=db_task.end_time,
            category=db_task.category,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            user_email=db_task.user.email if db_task.user else None,
            user_username=db_task.user.username if db_task.user else None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
        task_id: int = Path(..., description="ID of the task to update"),
        task_update: TaskUpdate = ...,
        db: Session = Depends(get_db)
):
    """Update an existing task"""
    try:
        db_task = crud_tasks.update_task(db, task_id=task_id, task_update=task_update)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        return TaskResponse(
            id=db_task.id,
            title=db_task.title,
            description=db_task.description,
            priority=db_task.priority,
            status=db_task.status,
            user_id=db_task.user_id,
            start_time=db_task.start_time,
            end_time=db_task.end_time,
            category=db_task.category,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            user_email=db_task.user.email if db_task.user else None,
            user_username=db_task.user.username if db_task.user else None
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{task_id}")
async def delete_task(
        task_id: int = Path(..., description="ID of the task to delete"),
        db: Session = Depends(get_db)
):
    """Delete a task"""
    success = crud_tasks.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_tasks_by_user(
        user_id: int = Path(..., description="ID of the user"),
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """Get all tasks for a specific user"""
    tasks = crud_tasks.get_tasks_by_user(db, user_id=user_id, skip=skip, limit=limit)

    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            user_id=task.user_id,
            start_time=task.start_time,
            end_time=task.end_time,
            category=task.category,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_email=task.user.email if task.user else None,
            user_username=task.user.username if task.user else None
        )
        task_responses.append(task_response)

    return task_responses


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def mark_task_completed(
        task_id: int = Path(..., description="ID of the task to mark as completed"),
        db: Session = Depends(get_db)
):
    """Mark a task as completed"""
    db_task = crud_tasks.mark_task_completed(db, task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=db_task.id,
        title=db_task.title,
        description=db_task.description,
        priority=db_task.priority,
        status=db_task.status,
        user_id=db_task.user_id,
        start_time=db_task.start_time,
        end_time=db_task.end_time,
        category=db_task.category,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
        user_email=db_task.user.email if db_task.user else None,
        user_username=db_task.user.username if db_task.user else None
    )


@router.get("/overdue/list", response_model=List[TaskResponse])
async def get_overdue_tasks(
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        db: Session = Depends(get_db)
):
    """Get all overdue tasks"""
    tasks = crud_tasks.get_overdue_tasks(db, user_id=user_id)

    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            user_id=task.user_id,
            start_time=task.start_time,
            end_time=task.end_time,
            category=task.category,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_email=task.user.email if task.user else None,
            user_username=task.user.username if task.user else None
        )
        task_responses.append(task_response)

    return task_responses


@router.get("/priority/{priority}", response_model=List[TaskResponse])
async def get_tasks_by_priority(
        priority: TaskPriority = Path(..., description="Task priority to filter by"),
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        db: Session = Depends(get_db)
):
    """Get all tasks with a specific priority"""
    tasks = crud_tasks.get_tasks_by_priority(db, priority=priority, user_id=user_id)

    task_responses = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            user_id=task.user_id,
            start_time=task.start_time,
            end_time=task.end_time,
            category=task.category,
            created_at=task.created_at,
            updated_at=task.updated_at,
            user_email=task.user.email if task.user else None,
            user_username=task.user.username if task.user else None
        )
        task_responses.append(task_response)

    return task_responses


@router.get("/stats/count")
async def get_tasks_count(
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
        priority: Optional[TaskPriority] = Query(None, description="Filter by task priority"),
        db: Session = Depends(get_db)
):
    """Get total count of tasks with optional filters"""
    count = crud_tasks.get_tasks_count(db, user_id=user_id, status=status, priority=priority)
    return {"count": count}


@router.get("/stats/summary")
async def get_task_summary(
        user_id: Optional[int] = Query(None, description="Filter by user ID"),
        db: Session = Depends(get_db)
):
    """Get task summary statistics"""

    total_tasks = crud_tasks.get_tasks_count(db, user_id=user_id)
    pending_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, status=TaskStatus.PENDING)
    in_progress_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, status=TaskStatus.IN_PROGRESS)
    completed_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, status=TaskStatus.COMPLETED)
    cancelled_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, status=TaskStatus.CANCELLED)

    high_priority_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, priority=TaskPriority.HIGH)
    urgent_tasks = crud_tasks.get_tasks_count(db, user_id=user_id, priority=TaskPriority.URGENT)

    overdue_tasks = len(crud_tasks.get_overdue_tasks(db, user_id=user_id))

    return {
        "total_tasks": total_tasks,
        "by_status": {
            "pending": pending_tasks,
            "in_progress": in_progress_tasks,
            "completed": completed_tasks,
            "cancelled": cancelled_tasks
        },
        "high_priority_tasks": high_priority_tasks,
        "urgent_tasks": urgent_tasks,
        "overdue_tasks": overdue_tasks
    }