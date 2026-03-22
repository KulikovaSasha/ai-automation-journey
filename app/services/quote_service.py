import random
from app.database.models import Quote


def get_random_quote(db):
    quotes = db.query(Quote).all()

    if not quotes:
        return None

    return random.choice(quotes)