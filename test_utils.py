from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.engine import Engine

from models import Base


def create_test_engine() -> Engine:
    return create_engine('sqlite:///:memory:')


def create_test_session(engine: Engine) -> ScopedSession:
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def create_test_database(engine: Engine) -> None:
    Base.metadata.create_all(engine)


def drop_test_database(engine: Engine) -> None:
    Base.metadata.drop_all(engine)


def initialize_test_grid(engine: Engine, width: int, height: int) -> None:
    from models import GridCell
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(width):
        for j in range(height):
            if session.query(GridCell).filter_by(x=i, y=j).count() == 0:
                cell = GridCell(x=i, y=j)
                session.add(cell)

    session.commit()
    session.close()
