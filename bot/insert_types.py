"""
Functionality to build up and pre-fill database with basic information.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from bot.models import ItemType

DATABASE_URL = str(os.getenv("DATABASE_URL"))

engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)()

cinema_type = ItemType(
    data_type="cinema",
    description="Here you can store films that you want to watch later."
    " Any serials and youtube videos can be placed here too.",
)
scroll_type = ItemType(
    data_type="page_with_curl",
    description="This category is more likely to be used for kinda science"
    " papers or maybe some long-read blog posts."
    " You can place here news articles as well.",
)
book_type = ItemType(
    data_type="books",
    description="It's a place for your books. Maybe friends recommended you some"
    " cool book or you just want to buy some cool example"
    " of book you have read before.",
)

# Building database structure
# base.metadata.create_all(engine)

# Fill data about types
# session.add(cinema_type)
# session.add(scroll_type)
# session.add(book_type)
# session.commit()
