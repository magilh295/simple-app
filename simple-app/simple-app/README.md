# simple-app

Aplikasi Flask + MySQL untuk praktikum Komputasi Awan (Jenkins + Docker).

## Jalankan lokal
    docker compose up -d --build
    # buka http://localhost:5000  (cek koneksi DB: /health)

## Pipeline
Checkout -> Build -> Build Docker Image -> Push Docker Image -> Deploy App + Database -> Verify
