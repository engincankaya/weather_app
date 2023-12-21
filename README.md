# Weather App

Weather App, Python dilinde geliştirilmiş bir hava durumu uygulamasıdır. Uygulama, OpenWeatherMap API'sini kullanarak belirli şehirlerin günlük hava durumu tahminlerini sağlar.

## MVC (Model-View-Controller) Mimari

Bu proje, MVC mimarisini temel alır. MVC, yazılım geliştirme sürecini organize etmek için kullanılan bir tasarım desenidir. Bu desen, uygulamayı veri (Model), kullanıcı arayüzü (View) ve iş mantığı (Controller) olarak üç ana bileşene ayırarak düzenler.

### MVC'nin Faydaları

- **Modülerlik:** Her bir bileşen kendi sorumluluk alanına sahiptir ve bağımsız olarak geliştirilebilir.
- **Bakım Kolaylığı:** Her bileşen kendi bağımsız modülünde olduğu için bakım ve güncelleme işlemleri daha etkili bir şekilde gerçekleştirilebilir.
- **Yeniden Kullanılabilirlik:** Aynı model veya view, farklı bir controller ile kullanılabilir.
- **Ekip Çalışması:** Geliştirme sürecini farklı ekipler arasında daha iyi koordine etmeyi sağlar.

## Proje Yapısı

Proje kaynak kodları `src` klasörü içindedir. Proje, ana başlangıç noktası olan `main.py` dosyası ile çalıştırılabilir.

```bash
cd src
python main.py
```

## Kullanılan Teknolojiler

- Python 3
- wxPython (GUI için)
- WebSocket (Asenkron haberleşme için)
- bcrypt (Kullanıcı şifresini hashlemek için)

## İleride Yapılabilecek İşler

- Kullanıcı verileri MongoDB veritabanına eklenebilir. (Şuan lokalde saklanıyor.)
- Proje, Docker konteyneri haline getirilecek ve Docker Compose ile ayağa kaldırılabilecek.
- AWS üzerinden bir instance kiralanıp kullanıcı veritabanımızı ve Websocket server'ını oraya aktarabiliriz.
