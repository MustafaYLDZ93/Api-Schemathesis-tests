#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=== Schemathesis Kurulumu ==="

# 1. Python virtual environment (Schemathesis için)
if [ ! -d "venv" ]; then
    echo "[1/2] Sanal ortam (venv) oluşturuluyor..."
    python3 -m venv venv
else
    echo "[1/2] Sanal ortam zaten mevcut, atlanıyor."
fi

echo "[2/2] Schemathesis indiriliyor..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================"
echo "          KURULUM TAMAMLANDI          "
echo "======================================"
echo "Test aracınızı aşağıdaki dosyayla çalıştırabilirsiniz:"
echo "- ./schemathesis/run.sh"
echo "======================================"
