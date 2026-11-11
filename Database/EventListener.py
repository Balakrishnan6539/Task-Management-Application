from sqlalchemy import event, inspect
from sqlalchemy.orm import object_session
from Database.Models import Task        
from Database.Models import Activity_log


@event.listens_for(Task, 'after_insert')
def receive_after_insert(mapper, connection, target):
    session = object_session(target)
    if not session:
        return

    user_id = session.info.get("session_user_id")

    log = Activity_log(
        task_id=target.task_id,
        user_id=user_id,
        action="CREATED",
        field_name=None,
        old_value=None,
        new_value=None
    )
    session.add(log)


@event.listens_for(Task, 'after_update')
def receive_after_update(mapper, connection, target):
    session = object_session(target)
    if not session:
        return

    user_id = session.info.get("session_user_id")
    state = inspect(target)
    
    for attr in state.attrs:
        history = attr.history
        if history.has_changes():
            field_name = attr.key
            
            # Skip internal timestamp fields
            if field_name in ["updated_at"]:
                continue
                
            old_value = str(history.deleted[0]) if history.deleted else None
            new_value = str(history.added[0]) if history.added else None

            # Skip logging if the value didn't actually change
            if old_value == new_value:
                continue

            log = Activity_log(
                task_id=target.task_id,
                user_id=user_id,
                action="UPDATED",
                field_name=field_name,
                old_value=old_value,
                new_value=new_value
            )
            session.add(log)


@event.listens_for(Task, 'after_delete')
def receive_after_delete(mapper, connection, target):
    session = object_session(target)
    if not session:
        return

    user_id = session.info.get("session_user_id")

    log = Activity_log(
        task_id=target.task_id,
        user_id=user_id,
        action="DELETED",
        field_name=None,
        old_value=None,
        new_value=None
    )
    session.add(log)