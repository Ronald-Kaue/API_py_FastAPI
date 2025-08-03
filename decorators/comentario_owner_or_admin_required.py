from functools import wraps
from fastapi import HTTPException
from http import HTTPStatus

def comentario_owner_or_admin_required(get_owner_id_func):
    def decorator(func):
        @wraps(func)
        def wrapper(id: int, id_comentario: int, *args, db, current_user, **kwargs):
            owner_id = get_owner_id_func(db, id_comentario)
            if current_user.id != owner_id and current_user.role != 'admin':
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Permissão negada"
                )
            return func(id, id_comentario, *args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator
