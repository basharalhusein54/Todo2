from sqlalchemy.orm import Session

from app.models.users import Users


def create_superuser(db:Session):
    user = db.query.filter(username=="super").first()