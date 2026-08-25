# FastAPI Film API

FastAPI kullanılarak geliştirilmiş; kullanıcı doğrulama, yetkilendirme ve ilişkisel veritabanı işlemleri içeren bir Film REST API projesidir.

## Özellikler

- Film ve yönetmen CRUD işlemleri
- Kullanıcı kayıt ve giriş sistemi
- JWT tabanlı kimlik doğrulama
- Şifrelerin hashlenerek saklanması
- Kullanıcıların yalnızca kendi filmlerini değiştirebilmesi
- SQLModel ile veritabanı işlemleri
- Alembic ile veritabanı migration yönetimi
- Pydantic ile veri doğrulama
- Otomatik Swagger dokümantasyonu
- Pytest ile API testleri
- CORS yapılandırması

## Kullanılan Teknolojiler

- Python
- FastAPI
- SQLModel
- SQLAlchemy
- SQLite
- Alembic
- Pydantic
- JWT
- Pytest
- uv

## Proje Yapısı

```text
film_api/
├── routers/
│   ├── filmler.py
│   ├── kullanicilar.py
│   └── yonetmenler.py
├── app.py
├── config.py
├── database.py
├── dependencies.py
├── models.py
└── security.py

migrations/
tests/
.env.example
alembic.ini
pyproject.toml
```

## Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/faruksemih/fastapi-film-api.git
cd fastapi-film-api
```

Bağımlılıkları kurun:

```bash
uv sync
```

`.env.example` dosyasını `.env` olarak kopyalayın:

```bash
cp .env.example .env
```

`.env` dosyasındaki `SECRET_KEY` değerini güvenli bir değerle değiştirin.

Veritabanı migrationlarını çalıştırın:

```bash
uv run alembic upgrade head
```

Uygulamayı başlatın:

```bash
uv run uvicorn film_api.app:app --reload
```

## API Dokümantasyonu

Uygulama çalışırken Swagger arayüzü:

```text
http://127.0.0.1:8000/docs
```

Alternatif ReDoc dokümantasyonu:

```text
http://127.0.0.1:8000/redoc
```

## Temel Endpointler

| Metot | Endpoint | Açıklama |
|---|---|---|
| POST | `/kullanicilar/kayit` | Yeni kullanıcı oluşturur |
| POST | `/kullanicilar/giris` | Giriş yapar ve token döndürür |
| GET | `/filmler` | Filmleri listeler |
| POST | `/filmler` | Yeni film ekler |
| GET | `/filmler/{film_id}` | Bir filmi getirir |
| PATCH | `/filmler/{film_id}` | Filmi kısmen günceller |
| DELETE | `/filmler/{film_id}` | Filmi siler |
| GET | `/yonetmenler` | Yönetmenleri listeler |
| POST | `/yonetmenler` | Yeni yönetmen ekler |

Korunan endpointleri kullanmak için Swagger üzerindeki **Authorize** düğmesinden giriş yapılmalıdır.

## Testler

Testleri çalıştırmak için:

```bash
uv run pytest -v
```

Testlerde ayrı bir veritabanı kullanılarak kullanıcı kaydı, giriş, JWT doğrulaması ve yetkilendirme işlemleri kontrol edilmektedir.

## Ortam Değişkenleri

Örnek `.env` yapılandırması:

```env
SECRET_KEY=change-this-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///filmler.db
```

Gerçek `.env` dosyası güvenlik nedeniyle GitHub’a yüklenmez.

## Geliştirici

**Faruk Semih**

GitHub: [@faruksemih](https://github.com/faruksemih)
