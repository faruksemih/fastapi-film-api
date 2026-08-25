from fastapi.testclient import TestClient

from tests.conftest import client

def kullanici_olustur_ve_token_al(
    client: TestClient,
    kullanici_adi: str
):
    kayit_response = client.post(
        "/kullanici/kayit",
        json={
            "kullanici_adi": kullanici_adi,
            "sifre": "Test12345"
        }
    )

    giris_response = client.post(
        "/kullanici/giris",
        data={
            "username": kullanici_adi,
            "password": "Test12345"
        }
    )

    return {
        "id": kayit_response.json()["id"],
        "token": giris_response.json()["access_token"]
    }

def test_swagger_aciliyor(client: TestClient):
    response = client.get("/docs")

    assert response.status_code == 200

def test_token_olmadan_film_silinmez(client: TestClient):
    response = client.delete("/filmler/1")
    assert response.status_code == 401

def test_kullanici_kayit_ve_giris(client: TestClient):
    kayit_response = client.post(
        "/kullanici/kayit",
        json={
            "kullanici_adi": "test_kullanici",
            "sifre": "Test12345"
        }
    )
    assert kayit_response.status_code == 201

    kayit_verisi = kayit_response.json()

    assert kayit_verisi["kullanici_adi"] == "test_kullanici"
    assert "sifre" not in kayit_verisi
    assert "sifre_hash" not in kayit_verisi

    giris_response = client.post(
        "/kullanici/giris",
        data={
            "username": "test_kullanici",
            "password": "Test12345",
        }
    )

    assert giris_response.status_code == 200

    token_verisi = giris_response.json()

    assert token_verisi["token_type"] == "bearer"
    assert token_verisi["access_token"] is not None

def test_yanlis_sifreyle_giris_yapilamaz(client: TestClient):
    kayit_response = client.post(
        "/kullanici/kayit",
        json={
            "kullanici_adi": "test_kullanici",
            "sifre": "DogruSifre123"
        }
    )

    assert kayit_response.status_code == 201

    giris_response = client.post(
        "/kullanici/giris",
        data={
            "username": "test_kullanici",
            "password": "yanlis_sifre"
        }
    )
    assert giris_response.status_code == 401

def test_gecerli_token_kabul_edilir(client: TestClient):
    client.post(
        "/kullanici/kayit",
        json={
           "kullanici_adi": "token_test",
            "sifre": "Test12345"
        }
    )

    giris_response = client.post(
        "/kullanici/giris",
        data={
            "username": "token_test",
            "password": "Test12345"
        }
    )
    token = giris_response.json()["access_token"]

    response = client.delete(
        "/kullanici/999",
        headers={
            "Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

def test_kullanici_kendi_filmini_ekler(client: TestClient):
    kayit_response = client.post(
        "/kullanici/kayit",
        json={
            "kullanici_adi": "film_test",
            "sifre": "Test12345"
        }
    )

    assert kayit_response.status_code == 201

    kullanici_id = kayit_response.json()["id"]

    giris_response = client.post(
        "/kullanici/giris",
        data={
            "username": "film_test",
            "password": "Test12345"
        }
    )

    assert giris_response.status_code == 200

    token = giris_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    yonetmen_response = client.post(
        "/yonetmenler",
        json={
            "ad": "Christopher Nolan"
        },
        headers=headers
    )

    assert yonetmen_response.status_code == 201

    yonetmen_id = yonetmen_response.json()["id"]

    film_response = client.post(
        "/filmler",
        json={
            "ad": "Inception",
            "yil": 2010,
            "puan": 8.8,
            "aciklama": "Bilim kurgu filmi",
            "yonetmen_id": yonetmen_id
        },
        headers=headers
    )

    assert film_response.status_code == 201

    film = film_response.json()

    assert film["ad"] == "Inception"
    assert film["yonetmen_id"] == yonetmen_id
    assert film["kullanici_id"] == kullanici_id

def test_baska_kullanici_filmi_silemez(client: TestClient):
    kullanici_a = kullanici_olustur_ve_token_al(
        client,
        "kullanici_a"
    )

    kullanici_b = kullanici_olustur_ve_token_al(
        client,
        "kullanici_b"
    )

    a_headers = {
        "Authorization": f"Bearer {kullanici_a['token']}"
    }

    b_headers = {
        "Authorization": f"Bearer {kullanici_b['token']}"
    }

    yonetmen_response = client.post(
        "/yonetmenler",
        json={"ad": "Christopher Nolan"},
        headers=a_headers
    )

    yonetmen_id = yonetmen_response.json()["id"]

    film_response = client.post(
        "/filmler",
        json={
            "ad": "Inception",
            "yil": 2010,
            "puan": 8.8,
            "aciklama": "Bilim kurgu",
            "yonetmen_id": yonetmen_id
        },
        headers=a_headers
    )

    film_id = film_response.json()["id"]

    b_silme_response = client.delete(
        f"/filmler/{film_id}",
        headers=b_headers
    )

    assert b_silme_response.status_code == 403
    assert b_silme_response.json()["detail"] == (
        "Bu işlem için yetkin yok"
    )

    a_silme_response = client.delete(
        f"/filmler/{film_id}",
        headers=a_headers
    )

    assert a_silme_response.status_code == 200

def test_cors_izni(client: TestClient):
    response = client.options(
        "/filmler",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST"
        }
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:5173"
    )