from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from film_api.database import get_session
from film_api.models import (
    YonetmenDB,
    YonetmenCreate,
    YonetmenPublic,
)

router = APIRouter(
    prefix="/yonetmenler",
    tags=["Yönetmenler"]
)

@router.post(
    "",
    response_model=YonetmenPublic,
    status_code=201
)
def yonetmen_ekle(
        yeni_yonetmen: YonetmenCreate,
        session: Session = Depends(get_session)
):
    db_yonetmen = YonetmenDB(
        ad=yeni_yonetmen.ad
    )
    session.add(db_yonetmen)
    session.commit()
    session.refresh(db_yonetmen)
    return db_yonetmen

@router.get("", response_model=list[YonetmenPublic])
def yonetmen_getir(
        session: Session = Depends(get_session)
):
    sorgu = select(YonetmenDB)
    return session.exec(sorgu).all()
