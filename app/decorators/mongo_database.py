from app.mongo_database import client

def mongo_transactional(origin_func):
    def wrapper_func(*args, **kwargs):
        with client.start_session() as session:
            with session.start_transaction():
                return origin_func(*args, session=session, **kwargs)

    return wrapper_func