from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from film_api.database import get_session
from film_api.models import (
    FilmCreate,
    FilmDB, FilmPublic, FilmUpdate,
    YonetmenDB,
    FilmDetay,
    KullaniciDB
)
from film_api.dependencies import aktif_kullanici_getir

router = APIRouter(
    prefix="/filmler",
    tags=["filmler"]
)

@router.post(
    "",
    response_model=FilmPublic,
    status_code=201
)
def film_ekle(
        yeni_film: FilmCreate,
        session: Session = Depends(get_session),
        aktif_kullanici: KullaniciDB = Depends(
            aktif_kullanici_getir
        )
):
    yonetmen = session.get(
        YonetmenDB,
        yeni_film.yonetmen_id
    )
    if yonetmen is None:
        raise HTTPException(
            status_code=404,
            detail="Yönetmen bulunamadı"
        )
    db_film = FilmDB(
        ad = yeni_film.ad,
        yil = yeni_film.yil,
        puan = yeni_film.puan,
        aciklama=yeni_film.aciklama,
        yonetmen_id=yeni_film.yonetmen_id,
        kullanici_id=aktif_kullanici.id
    )

    session.add(db_film)
    session.commit()
    session.refresh(db_film)
    return db_film

@router.get("", response_model=list[FilmPublic])
def filmleri_getir(
        session: Session = Depends(get_session)
):
    sorgu = select(FilmDB)
    filmler = session.exec(sorgu).all()

    return filmler

@router.get("/{filmler_id}", response_model=FilmDetay)
def film_geitr(
        film_id: int,
        session: Session = Depends(get_session)
):
    film = session.get(FilmDB, film_id)

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="Film bulunamadı"
        )
    return film

@router.delete("/{film_id}", response_model=FilmPublic)
def film_sil(
        film_id: int,
        session: Session = Depends(get_session),
        aktif_kullanici: KullaniciDB = Depends(
            aktif_kullanici_getir
        )
):
    film = session.get(FilmDB, film_id)

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="film bulunamadı"
        )
    if film.kullanici_id != aktif_kullanici.id:
        raise HTTPException(
            status_code=403,
            detail="Bu işlem için yetkin yok"
        )
    session.delete(film)
    session.commit()
    return film

@router.put("/{film_id}", response_model=FilmPublic)
def film_guncelle(
        film_id: int,
        yeni_film: FilmCreate,
        session: Session = Depends(get_session),
        aktif_kullanici: KullaniciDB = Depends(
            aktif_kullanici_getir
        )
):
    film = session.get(FilmDB, film_id)

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="film bulunamadı"
        )
    if film.kullanici_id != aktif_kullanici.id:
        raise HTTPException(
            status_code=403,
            detail="Bu işlem için yetkin yok"
        )
    film.ad = yeni_film.ad
    film.yonetmen_id = yeni_film.yonetmen_id
    film.yil = yeni_film.yil

    session.add(film)
    session.commit()
    session.refresh(film)
    return film

@router.patch(
    "/{film_id}",
    response_model=FilmPublic
)
def filmi_kismi_guncelle(
        film_id: int,
        yeni_film: FilmUpdate,
        session: Session = Depends(get_session),
        aktif_kullanici: KullaniciDB = Depends(
            aktif_kullanici_getir
        )
):
    film = session.get(FilmDB, film_id)

    if film is None:
        raise HTTPException(
            status_code=404,
            detail="film bulunamadı"
        )
    if film.kullanici_id != aktif_kullanici.id:
        raise HTTPException(
            status_code=403,
            detail="buy işlem için yetkin yok"
        )

    guncelleme_verisi = yeni_film.model_dump(
        exclude_unset=True
    )

    if "yonetmen_id" in guncelleme_verisi:
        yonetmen = session.get(
            YonetmenDB,
            guncelleme_verisi["yonetmen_id"]
        )

        if yonetmen is None:
            raise HTTPException(
                status_code=404,
                detail="Yönetmen bulunamadı"
            )

    film.sqlmodel_update(guncelleme_verisi)

    session.add(film)
    session.commit()
    session.refresh(film)
    return film