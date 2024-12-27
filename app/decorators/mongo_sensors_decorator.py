from app.mongo_sensors_database import client

def mongo_sensors_transactional(origin_func):
    def wrapper_func(*args, **kwargs):
        with client.start_session() as session:
            with session.start_transaction():
                return origin_func(*args, sensors_session=session, **kwargs)

    return wrapper_func