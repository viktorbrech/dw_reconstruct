from models import Regiment, Fighter, GridCell
import test_utils
import pytest
from sqlalchemy.orm.scoping import ScopedSession
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

@pytest.fixture(scope="module")
def session():
    engine: Engine = test_utils.create_test_engine()
    test_utils.create_test_database(engine)
    test_utils.initialize_test_grid(engine, width=20, height=20)
    session: ScopedSession = test_utils.create_test_session(engine)
    yield session
    session.close()
    test_utils.drop_test_database(engine)

def test_regiment_creation(session):
    engine = test_utils.create_test_engine()
    test_utils.create_test_database(engine)
    test_utils.initialize_test_grid(engine, width=20, height=20)
    session = test_utils.create_test_session(engine)

    regiment_name = "Test Regiment 1"
    regiment = Regiment(5, session, regiment_name)
    session.add(regiment)
    session.commit()

    retrieved_regiment = session.query(Regiment).filter_by(name=regiment_name).first()
    assert retrieved_regiment is not None
    assert retrieved_regiment.name == regiment_name
    assert len(retrieved_regiment.fighters_in_regiment) == 5

    session.remove()
    test_utils.drop_test_database(engine)


def test_fighter_creation(session):
    engine = test_utils.create_test_engine()
    test_utils.create_test_database(engine)
    test_utils.initialize_test_grid(engine, width=20, height=20)
    session = test_utils.create_test_session(engine)

    regiment = Regiment(1, session, "Test Regiment 2")
    session.add(regiment)
    session.commit()

    fighter_name = "Test Fighter"
    x, y = 1, 1
    fighter = Fighter(regiment, x, y, session, fighter_name)
    session.add(fighter)
    session.commit()

    retrieved_fighter = session.query(Fighter).filter_by(name=fighter_name).first()
    assert retrieved_fighter is not None
    assert retrieved_fighter.name == fighter_name
    assert retrieved_fighter.grid_cell.x == x
    assert retrieved_fighter.grid_cell.y == y
    assert retrieved_fighter.regiment_id == regiment.id

    session.remove()
    test_utils.drop_test_database(engine)


def test_grid_cell_creation(session):
    engine = test_utils.create_test_engine()
    test_utils.create_test_database(engine)
    test_utils.initialize_test_grid(engine, width=20, height=20)
    session = test_utils.create_test_session(engine)

    x, y = 21, 21
    cell = GridCell(x=x, y=y)
    session.add(cell)
    session.commit()

    retrieved_cell = session.query(GridCell).filter_by(x=x, y=y).first()
    assert retrieved_cell is not None
    assert retrieved_cell.x == x
    assert retrieved_cell.y == y

    session.remove()
    test_utils.drop_test_database(engine)
