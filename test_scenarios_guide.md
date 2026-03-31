# Akıllı API Test Senaryoları Kılavuzu

Bu belgede, kurduğumuz aracın (Schemathesis) API'nizi hangi senaryolar altında test ettiğini klasik bir statik test aracı olan Hurl'den nasıl ayırdığını inceleyeceğiz.

Örnek olarak, dizinimize eklediğimiz `openapi.yaml` (E-ticaret API'si) dosyanızı kullanacağız.

---

## 🚀 1. Schemathesis (Statik ve Fuzzing Testleri)
*Slogan: "Hurl ile beklediğini doğrularsın, Schemathesis ile beklemediğinle yüzleşirsin."*

Schemathesis, OpenAPI tanımınıza bakar ve binlerce uç/sorunlu girdiyi uydurarak API'nizin çöküp çökmediğini ("500 Internal Server Error" verip vermediğini) kontrol eder. 

### Örnek Senaryo: Veri Zehirlenmesi (Data Poisoning)
`POST /users` ucu için OpenAPI spesifikasyonumuz şu kuralı dikte ediyor: `username` string tipindedir.
- **Hurl ile yapılan:** `{"username": "musti", "email": "test@test.com"}` göndeririz, dönen sonucun "201 Created" olmasına bakarız.
- **Schemathesis'in ürettiği senaryolar:** 
  1. **Boş Objeler:** Sadece `{}` gönderir. (Sunucu 400 Bad Request dönmelidir).
  2. **Anormal Değerler:** `username` alanına `"\u0000"`, `2147483648`, `null`, hatta 5 MB'lık çok uzun bir Japonca karakter listesi koyar.
  3. **Ters Tipler:** `email` beklenen yere `["array"]` koyar.

> [!TIP]
> **Beklenen Durum:** Sizin başarılı olmanız için API kodunuzun hiçbir zaman çökmemesi, beklenmeyen bu senaryolarda dahi kontrollü şekilde HTTP `400 (Bad Request)` veya `422 (Unprocessable Entity)` gibi tutarlı hatalar dönmesi gerekir.

---

## 🚀 Sonraki Adımlar

Eğer test ortamını tamamen anladıysanız, kendi projelerinizdeki `openapi.yaml` dosyalarını bu dizine kopyalayıp aynı sistem üzerinden farklı backend'leri test etmeyi deneyebilirsiniz.
