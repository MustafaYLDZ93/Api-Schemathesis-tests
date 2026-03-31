#!/bin/bash
cd "$(dirname "$0")/.."

# Check if environment exists
if [ ! -d "venv" ]; then
    echo "Hata: Schemathesis (venv) kurulu değil. Lütfen önce ../setup.sh betiğini çalıştırın."
    exit 1
fi

source venv/bin/activate

# Özel python kural dosyamızı (schemathesis_hooks.py) sisteme yüklüyoruz.
export SCHEMATHESIS_HOOKS=schemathesis_hooks

echo "======================================"
echo "   SCHEMATHESIS GELİŞMİŞ MOD          "
echo "======================================"
echo "İşlem: Kurallar, Özel Eklentiler (Hooks) ve Detaylı Loglama (Cassettes) devrede."

schemathesis run openapi.yaml \
  --url http://localhost:8080/api/v1 \
  --checks all \
  --max-response-time 0.5 \
  --report-vcr-path cassettes.yaml

echo "======================================"
echo "Test tamamlandı."
echo "Not: Hata kaydedici devredeydi. Olası tüm uç denemelerin (request/response) detayları 'cassettes.yaml' dosyasına yazıldı."
