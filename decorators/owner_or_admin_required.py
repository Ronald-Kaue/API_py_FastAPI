from functools import wraps
from fastapi import HTTPException, Depends
from security import current_user
from database import get_db
from http import HTTPStatus

def owner_or_admin_required(get_owner_id_func):
    def decorator(f):
        @wraps(f)
        def wrapper(id: int, *args, db=Depends(get_db), current_user=Depends(current_user), **kwargs):
            owner_id = get_owner_id_func(db, id)
            if current_user.id != owner_id and current_user.role != 'admin':
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail='{"error": "Você não tem permissão para alterar esta mensagem"}'
                )
            return f(id, *args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator