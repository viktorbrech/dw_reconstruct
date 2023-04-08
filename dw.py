import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Regiment, Fighter, GridCell, Base

engine = create_engine('sqlite:///dw.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create a list of grid cells that do not already exist in the database
width = 20
height = 20
new_cells = [
    GridCell(x=i, y=j)
    for i in range(width)
    for j in range(height)
    if session.query(GridCell).filter_by(x=i, y=j).count() == 0
]

# Add new grid cells to the session
session.add_all(new_cells)
session.commit()

# Query all regiments from the database
all_regiments = session.query(Regiment).all()

# Loop through each regiment and print its name
for regiment in all_regiments:
    print(f"* {regiment.name}")

    # Query all fighters associated with the current regiment
    fighters = session.query(Fighter).filter(Fighter.regiment_id == regiment.id).all()

    # Loop through each fighter and print their name
    for fighter in fighters:
        print(f"    * {fighter.name} ({fighter.grid_cell.x}, {fighter.grid_cell.y})")

# Example usage: add a regiment of random size
regiment: Regiment = Regiment(random.randint(2, 5), session)
# Add fighters and regiment to the database
session.add_all([regiment])
# Commit changes and close the session
session.commit()
session.close()
