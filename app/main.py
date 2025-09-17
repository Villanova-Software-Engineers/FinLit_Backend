from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Item).filter(models.Item.id == item_id).first()