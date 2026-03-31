# Api-Schemathesis-tests

Mock E-Commerce API üzerinde Schemathesis ile property-based fuzzing testi örneği.

Schemathesis, OpenAPI şemasını okuyarak otomatik olarak yüzlerce uç durum (null değerler, yanlış tipler, silinen kaynaklar, desteklenmeyen HTTP metodları vb.) üretir ve API'nin her birinde tutarlı davranıp davranmadığını doğrular.

---

## Proje Yapısı

```
api-test-types/
├── openapi.yaml              # Mock E-Commerce API şeması (OpenAPI v3)
├── mock_server.py            # Sağlıklı Flask sunucusu (port 8080)
├── mock_server_broken.py     # Kasıtlı hatalı sunucu — Schemathesis'in ne bulduğunu görmek için
├── schemathesis_hooks.py     # Özel güvenlik kuralı (@schemathesis.check)
├── requirements.txt          # Python bağımlılıkları
├── setup.sh                  # Sanal ortam kurulumu
├── run_server.sh             # Mock sunucuyu başlatır
└── schemathesis/
    └── run.sh                # Schemathesis testlerini çalıştırır
```

---

## Kurulum

### Gereksinimler

- Python 3.10+
- pip

### Adımlar

```bash
# 1. Projeyi klonla
git clone https://github.com/MustafaYLDZ93/Api-Schemathesis-tests.git
cd Api-Schemathesis-tests

# 2. Sanal ortamı oluştur ve bağımlılıkları yükle
bash setup.sh
```

`setup.sh` şunları yapar:
- `venv/` klasörünü oluşturur
- `schemathesis` ve `flask` paketlerini yükler

---

## Çalıştırma

### 1. Mock sunucuyu başlat

```bash
bash run_server.sh
```

Flask sunucusu `http://localhost:8080` adresinde ayağa kalkar.

### 2. Schemathesis testlerini çalıştır (yeni terminal)

```bash
bash schemathesis/run.sh
```

Bu komut şunları yapar:
- Sanal ortamı aktive eder
- `SCHEMATHESIS_HOOKS=schemathesis_hooks` ortam değişkenini set eder (özel güvenlik kuralını yükler)
- `openapi.yaml` şemasına göre tüm kontroller aktif şekilde test çalıştırır
- Sonuçları `cassettes.yaml` dosyasına kaydeder

### Komut parametreleri

| Flag | Değer | Açıklama |
|---|---|---|
| `--checks all` | — | 14 yerleşik kontrolü etkinleştirir |
| `--max-response-time` | `0.5` | 500 ms üzerindeki yanıtlar başarısız sayılır |
| `--report-vcr-path` | `cassettes.yaml` | Tüm istek/yanıt çiftlerini kaydeder |

---

## API Endpoint'leri

| Method | Endpoint | Açıklama |
|---|---|---|
| `POST` | `/api/v1/users` | Yeni kullanıcı oluşturur |
| `POST` | `/api/v1/users/{userId}/orders` | Kullanıcıya sipariş ekler |
| `DELETE` | `/api/v1/users/{userId}` | Kullanıcıyı siler |

Stateful bağımlılık: Sipariş oluşturabilmek için önce kullanıcı oluşturulması gerekir. Schemathesis bu zinciri otomatik keşfeder.

---

## Özel Güvenlik Kuralı

`schemathesis_hooks.py` içindeki özel kontrol, her API yanıtında `X-Security-Protection` başlığının varlığını doğrular:

```python
@schemathesis.check
def custom_security_header_check(ctx, response, case):
    headers = {k.lower(): v for k, v in response.headers.items()}
    if "x-security-protection" not in headers:
        raise AssertionError("Güvenlik İhlali: 'X-Security-Protection' başlığı eksik!")
```

---

## Hatalı Sunucu (Demo)

`mock_server_broken.py` dosyası 3 kasıtlı hata içerir:

1. **Tip kontrolü yok** → Schemathesis `negative_data_rejection` ve `not_a_server_error` kontrollerini başarısız sayar
2. **Use-after-free** → Silinen kullanıcıya sipariş verilebiliyor, `use_after_free` kontrolü bunu yakalar
3. **Güvenlik başlığı eksik** → `custom_security_header_check` tüm endpoint'lerde başarısız olur

Hatalı sunucuyu test etmek için:

```bash
# Hatalı sunucuyu başlat
python mock_server_broken.py

# Aynı Schemathesis komutunu çalıştır
bash schemathesis/run.sh
```

Beklenen çıktı: `9 failures in ~77s`

---

## Sağlıklı Test Sonucu

Sağlıklı sunucu (`mock_server.py`) ile çalıştırıldığında:

```
1273 test case — 1273 SUCCESS — 0 FAILURE
Ortalama yanıt süresi: 0.9 ms
```

---

## Bağımlılıklar

```
schemathesis>=3.30.0
flask>=3.0.0
```
