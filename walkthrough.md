# API Akıllı Test Ortamı: Kurulum Özeti

Başarılı bir şekilde **Schemathesis** aracı için altyapıyı tamamladık.

## Neler Yapıldı?

1. **Python Sanal Ortamı (`venv`)**:
   - `schemathesis` aracının çalışması için diğer projelerinizle çakışmayacak izole bir Python ortamı kuruldu (`setup.sh` tarafından çalıştırıldı).

2. **Örnek API Taslağı (`openapi.yaml`)**:
   - *Stateful* çalışan fuzzer'ların etkisini görebilmeniz adına; önce "Kullanıcı oluşturulması" *sonra* "Sipariş oluşturulması" zorunluluğunu gösteren, bağımlılıkları barındıran basit bir OpenAPI v3 dökümanı yarattık.

## Komut Dosyaları (Scripts) Nasıl Kullanılır?

Testlerinizi her seferinde uzun parametrelerle uğraşarak konsola yazmanızı engellemek üzere 1 adet hazır şablon komut dosyası oluşturduk.

> [!TIP]
> Artık yapmanız gereken tek şey, `./openapi.yaml` dosyasını kendi test etmek istediğiniz servisin API tanımı ile değiştirmektir!

#### 1. Schemathesis (Statik / Property-Based Fuzzing)
Sadece çalıştırılabilir komutu çağırmanız yeterli:
```bash
./schemathesis/run.sh
```
*[openapi.yaml](file:///Users/musti/Desktop/api-test-types/openapi.yaml) dosyasındaki formatları okuyarak rastgele tiplerde geçersiz/geçerli tüm verileri API'a gönderir.*
