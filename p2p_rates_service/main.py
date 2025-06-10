from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from .database import SessionLocal, init_db, Click

app = FastAPI()

# Dependency to get DB session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    init_db()

@app.get("/click")
def click(target_url: str, user_id: str, db: Session = Depends(get_db)):
    if not target_url:
        raise HTTPException(status_code=400, detail="target_url required")
    click = Click(user_id=user_id, target_url=target_url, timestamp=datetime.utcnow())
    db.add(click)
    db.commit()
    return RedirectResponse(url=target_url)

@app.get("/report")
def report(db: Session = Depends(get_db)):
    result = db.query(Click.target_url, Click.user_id).all()
    stats = {}
    for url, user in result:
        stats.setdefault(url, {})
        stats[url][user] = stats[url].get(user, 0) + 1
    return stats
