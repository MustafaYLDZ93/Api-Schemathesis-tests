#!/bin/bash
cd "$(dirname "$0")"

# Ortam kurulu mu kontrolü
if [ ! -d "venv" ]; then
    echo "Hata: Python venv dizini bulunamadı! Lütfen önce setup.sh çalıştırın."
    exit 1
fi

echo "================================================="
echo "   ZAFİYETLİ (BUG'LI) DENEME SUNUCUSU BAŞLIYOR   "
echo "================================================="
echo "Adres: http://localhost:8080"
echo "API Rotaları: "
echo "  - POST   /api/v1/users"
echo "  - DELETE /api/v1/users/<id>"
echo "  - POST   /api/v1/users/<id>/orders"
echo "================================================="
echo "Not: Çıkmak ve sunucuyu durdurmak için CTRL+C tuşlarına basın."

# Uvicorn, Flask v.b. yerel sunucuyu aktifleştir
source venv/bin/activate
python3 mock_server.py
