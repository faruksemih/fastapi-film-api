from pydantic import BaseModel, Field as PydanticField
from sqlmodel import SQLModel, Field as SQLField, Relationship

class YonetmenCreate(BaseModel):
    ad: str = PydanticField(min_length=2, max_length=100)

class YonetmenDB(SQLModel, table=True):
    __tablename__ = "yonetmenler"

    id: int | None = SQLField(default=None, primary_key=True)
    ad: str
    filmler: list["FilmDB"] = Relationship(
        back_populates="yonetmen"
    )

class YonetmenPublic(SQLModel):
    id: int
    ad: str

class FilmCreate(BaseModel):
    ad: str = PydanticField(min_length=1, max_length=100)
    yil: int = PydanticField(ge=1888, le=2100)
    puan: float = PydanticField(ge=0, le=10)
    yonetmen_id: int
    aciklama: str | None = None

class FilmDB(SQLModel, table=True):
    __tablename__ = "filmler"
    id: int | None = SQLField(default=None, primary_key=True)
    ad: str
    yil: int
    puan: float
    aciklama: str | None = SQLField(default=None)

    yonetmen_id: int = SQLField(
        foreign_key="yonetmenler.id"
    )
    yonetmen: YonetmenDB | None = Relationship(
        back_populates="filmler"
    )
    kullanici_id: int | None = SQLField(
        default=None,
        foreign_key="kullanicilar.id"
    )

class FilmUpdate(BaseModel):
    ad: str | None = PydanticField(
        min_length=1, max_length=100
    )
    yil: int | None = PydanticField(
        ge=1888, le=2100
    )
    puan: float | None= PydanticField(
        ge=0, le=10
    )
    aciklama: str | None = None
    yonetmen_id: int | None = None

class FilmPublic(SQLModel):
    id: int
    ad: str
    yil: int
    puan: float
    yonetmen_id: int
    aciklama: str | None = None
    kullanici_id: int | None

class FilmDetay(FilmPublic):
    yonetmen: YonetmenPublic | None = None

class KullaniciCreate(BaseModel):
    kullanici_adi: str = PydanticField(
        min_length=1,
        max_length=100
    )
    sifre: str = PydanticField(
        min_length=8,
        max_length=100
    )

class KullaniciDB(SQLModel, table=True):
    __tablename__ = "kullanicilar"

    id: int | None = SQLField(
        default=None,
        primary_key=True
    )
    kullanici_adi: str = SQLField(
        index=True,
        unique=True
    )
    sifre_hash: str

class KullaniciPublic(SQLModel):
    id: int
    kullanici_adi: str

class Token(BaseModel):
    access_token: str
    token_type: str