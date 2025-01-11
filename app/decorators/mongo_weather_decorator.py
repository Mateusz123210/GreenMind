from app.mongo_weather_database import client

def mongo_weather_transactional(origin_func):
    def wrapper_func(*args, **kwargs):
        with client.start_session() as session:
            with session.start_transaction():
                return origin_func(*args, weather_session=session, **kwargs)

    return wrapper_func