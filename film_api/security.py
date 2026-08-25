from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from film_api.config import settings

password_hash = PasswordHash.recommended()

def access_token_olustur(kullanici_id: int) -> str:
    bitis_zamani = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    token_verisi = {
        "sub": str(kullanici_id),
        "exp": bitis_zamani
    }
    return jwt.encode(
        token_verisi,
        settings.secret_key,
        algorithm=settings.algorithm
    )

def sifre_hashle(sifre: str) -> str:
    return password_hash.hash(sifre)

def sifre_dogrula(
        girilen_sifre: str,
        kayitli_hash: str
) -> bool:
    return password_hash.verify(
        girilen_sifre,
        kayitli_hash
    )
