import jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from film_api.config import settings
from film_api.database import get_session
from film_api.models import KullaniciDB


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/kullanici/giris"
)


def aktif_kullanici_getir(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> KullaniciDB:

    kimlik_hatasi = HTTPException(
        status_code=401,
        detail="Geçersiz veya süresi dolmuş token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        kullanici_id = payload.get("sub")

        if kullanici_id is None:
            raise kimlik_hatasi

        kullanici_id = int(kullanici_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise kimlik_hatasi

    kullanici = session.get(
        KullaniciDB,
        kullanici_id
    )

    if kullanici is None:
        raise kimlik_hatasi

    return kullanici