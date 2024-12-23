import contextvars
from functools import wraps
from app.database import SessionMaker

db_session_context = contextvars.ContextVar("db_session", default=None)

def transactional(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()

        if db_session is None:
            db_session = SessionMaker()
            db_session_context.set(db_session)

            try:
                result = func(*args, **kwargs)
                db_session.commit()

            except Exception as e:
                db_session.rollback()
                raise

            finally:
                db_session.close()
                db_session_context.set(None)

        else:
            return func(*args, **kwargs)
        return result

    return wrap_func


def db(func):
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()
        return func(*args, **kwargs, db=db_session)

    return wrap_func