
from sqlalchemy import event, inspect
from sqlalchemy.orm import object_session

from Database.Models import Task, Activity_log


def get_user_id(target):
    """Get the logged-in user's ID from the SQLAlchemy session."""
    session = object_session(target)

    if session:
        return session.info.get("session_user_id")

    return None


def save_activity(connection,task_id,user_id,action,field_name=None,old_value=None,new_value=None):
    """Insert an activity log directly into the database."""

    connection.execute(
        Activity_log.__table__.insert().values(
            task_id=task_id,
            user_id=user_id,
            action=action,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None
        )
    )



@event.listens_for(Task, "after_insert")
def receive_after_insert(mapper, connection, target):
    user_id = get_user_id(target)

    fields = [
        "project_id",
        "assigned_to",
        "created_by",
        "title",
        "description",
        "priority",
        "status",
        "start_date",
        "end_date"
    ]

    for field in fields:

        value = getattr(target, field)

        save_activity(
            connection=connection,
            task_id=target.task_id,
            user_id=user_id,
            action="CREATED",
            field_name=field,
            old_value=None,
            new_value=value
        )


@event.listens_for(Task, "after_update")
def receive_after_update(mapper, connection, target):

    user_id = get_user_id(target)

    state = inspect(target)

    for attr in mapper.column_attrs:

        field_name = attr.key

        # Skip timestamp fields
        if field_name in ["updated_at"]:
            continue

        history = state.attrs[field_name].history

        if not history.has_changes():
            continue

        old_value = history.deleted[0] if history.deleted else None
        new_value = history.added[0] if history.added else getattr(target, field_name)

        # Skip if values are actually the same
        if old_value == new_value:
            continue

        save_activity(
            connection=connection,
            task_id=target.task_id,
            user_id=user_id,
            action="UPDATED",
            field_name=field_name,
            old_value=old_value,
            new_value=new_value
        )


@event.listens_for(Task, "after_delete")
def receive_after_delete(mapper, connection, target):

    user_id = get_user_id(target)

    save_activity(
        connection=connection,
        task_id=None,
        user_id=user_id,
        action="DELETED",
        field_name="task_id",
        old_value=target.task_id,
        new_value=None
    )
