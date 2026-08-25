from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from film_api.database import get_session
from film_api.models import (
    KullaniciCreate,
    KullaniciDB,
    KullaniciPublic,
    Token
)
from film_api.security import (
    sifre_dogrula,
    access_token_olustur
)
from film_api.security import sifre_hashle


router = APIRouter(
    prefix="/kullanici",
    tags=["kullanıcılar"],
)

@router.post(
    "/kayit",
    response_model=KullaniciPublic,
    status_code=201
)
def kullanici_kaydet(
        yeni_kullanici: KullaniciCreate,
        session: Session = Depends(get_session)
):
    kullanici_adi = yeni_kullanici.kullanici_adi.lower()

    sorgu = select(KullaniciDB).where(
        KullaniciDB.kullanici_adi == kullanici_adi
    )
    mevcut_kullanici = session.exec(sorgu).first()

    if mevcut_kullanici is not None:
        raise HTTPException(
            status_code=409,
            detail="Bu kullanıcı adı zaten alınmış"
        )
    db_kullanici = KullaniciDB(
        kullanici_adi=kullanici_adi,
        sifre_hash=sifre_hashle(yeni_kullanici.sifre)
    )
    session.add(db_kullanici)
    session.commit()
    session.refresh(db_kullanici)
    return db_kullanici

@router.post("/giris", response_model=Token)
def kullanici_giris(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    kullanici_adi = form_data.username.lower()

    sorgu = select(KullaniciDB).where(
        KullaniciDB.kullanici_adi == kullanici_adi
    )

    kullanici = session.exec(sorgu).first()

    if kullanici is None or not sifre_dogrula(
        form_data.password,
        kullanici.sifre_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="kullanıcı adı veya sifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = access_token_olustur(kullanici.id)
    return Token(
        access_token=token,
        token_type="bearer"
    )