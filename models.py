import random

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from sqlalchemy.orm.exc import NoResultFound

Base = declarative_base()

class Regiment(Base):
    __tablename__: str = 'regiments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # fighters = relationship("Fighter", back_populates="regiment")

    def __init__(self, num_fighters: int, session: Session, name: str | None = None) -> None:
        if name is None:
            adjectives = ["Mighty", "Glorious", "Fearless", "Valiant", "Legendary"]
            nouns = ["Band", "Unit", "Squad", "Brigade", "Company"]
            titles = ["of Cornwall", "IV", "the Conquerors", "the Invincibles", "the Champions"]
            name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(titles)}"
        self.name = name
        self.fighters = [Fighter(regiment = self, x=(i + 1) * 2, y=(i + 1) * 3, session = session) for i in range(num_fighters)]
    def __repr__(self):
        return f"{self.name} ({len(self.fighters)} fighters)"

class Fighter(Base):
    __tablename__ = 'fighters'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grid_cell_id = Column(Integer, ForeignKey("grid_cells.id"))
    grid_cell = relationship("GridCell", back_populates="fighters")
    regiment_id = Column(Integer, ForeignKey('regiments.id'))
    regiment = relationship("Regiment", backref="fighters_in_regiment")
    def __init__(self, regiment: Regiment, x: int, y: int, session: Session, name: str | None = None):
        self.regiment = regiment
        if name is None:
            first_names = ["Arthur", "Edmund", "William", "Geoffrey", "Henry", "Leofric", "Osbert", "Ralph", "Godric", "Alfred"]
            name = f"{random.choice(first_names)}"
        self.name = name
        try:
            self.grid_cell: GridCell = session.query(GridCell).filter_by(x=x, y=y).one()
        except NoResultFound:
            print("No matching grid cell found.")
        except MultipleResultsFound:
            print("Multiple matching grid cells found.")
    def __repr__(self):
        return f"{self.name}"

class GridCell(Base):
    __tablename__ = "grid_cells"
    id = Column(Integer, primary_key=True)
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)
    terrain_type = Column(String, nullable=True)
    elevation = Column(Integer, nullable=True)
    fighters = relationship("Fighter", back_populates="grid_cell")
    __table_args__ = (UniqueConstraint('x', 'y', name='_x_y_unique'),)