# Yüz Tanıma Giriş Sistemi

Bu proje, kamera üzerinden yüz tanıma teknolojisi kullanarak kullanıcı kimlik doğrulama sistemi sunar.

## Özellikler

- Kamera ile yüz tanıma
- Kullanıcı kaydı oluşturma
- Yüz tanıma ile giriş yapma
- Kullanıcı verilerini yerel olarak saklama

## Kurulum

1. Projeyi bilgisayarınıza indirin
2. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

### Windows için Ek Kurulum Adımları

Windows'ta face_recognition kütüphanesi CMake ve Visual C++ build tools gerektirir:

1. [CMake](https://cmake.org/download/)'i indirip kurun
2. [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)'u indirip kurun (C++ build tools seçeneğini işaretleyin)

## Kullanım

Programı çalıştırmak için aşağıdaki komutu kullanın:

```bash
python main.py
```

### Yeni Kullanıcı Kaydı

1. "Kayıt Ol" butonuna tıklayın
2. Kullanıcı adınızı girin
3. Kamera açıldığında yüzünüzü kameraya gösterin
4. Kayıt işlemi tamamlandığında bir onay mesajı görünecektir

### Giriş Yapma

1. "Giriş Yap" butonuna tıklayın
2. Kamera açıldığında yüzünüzü kameraya gösterin
3. Yüzünüz tanındığında sisteme giriş yapacaksınız

## Gereksinimler

- Python 3.6 veya üzeri
- OpenCV
- NumPy
- face_recognition
- Pillow (PIL)
- Bir web kamerası 