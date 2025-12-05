# TTS-Indonesia-Gratis

![Screen Shot 2024-07-23 at 3 20 33 AM](https://github.com/user-attachments/assets/2eac1c9e-3621-43ea-b86b-c87c72883995)


[![Jalankan Aplikasi ini](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-xl-dark.svg)](https://deddy-tts-indonesiaku-gratis.hf.space)


Aplikasi ini digunakan untuk menghasilkan suara berbasis teks dengan berbagai pilihan pembicara. Teknologi yang digunakan meliputi model text-to-speech (TTS) yang canggih dengan konversi teks ke fonem (G2P). Model yang dipakai dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda.

## Data

- [Indonesian Azure TTS](https://depia.wiki/files/azure-tts.tar)

## Fitur

- Menghasilkan suara dari teks dalam berbagai bahasa dan aksen.
- Pilihan pembicara yang beragam dengan karakter suara yang unik.
- Antarmuka pengguna yang interaktif dan mudah digunakan dengan Gradio.
- Tema khusus dengan gradasi warna kuning ke putih.

## Pembicara yang Tersedia
![ardi](https://github.com/user-attachments/assets/d0b82dea-7b14-4347-91f5-27574d3bcbb1)
![gadis](https://github.com/user-attachments/assets/b016cccb-7f7c-4643-8551-597fd56252bb)
![wibowo](https://github.com/user-attachments/assets/26e29e38-c364-4bbb-b71f-028c7dfeccd1)

- **Wibowo**: Suara jantan berwibawa
- **Ardi**: Suara lembut dan hangat
- **Gadis**: Suara perempuan yang merdu
- **Juminten**: Suara perempuan jawa (bahasa jawa)
- **Asep**: Suara lelaki sunda (bahasa sunda)

## Cara Menggunakan

### 1. Menggunakan Web Interface (Online)

Cara termudah adalah menggunakan aplikasi online yang sudah tersedia:

1. Kunjungi [https://deddy-tts-indonesiaku-gratis.hf.space](https://deddy-tts-indonesiaku-gratis.hf.space)
2. Masukkan teks yang ingin diubah menjadi suara di kolom teks
3. Pilih kecepatan bicara yang diinginkan (0.1 - 1.99, default: 0.8)
4. Pilih pembicara (Wibowo, Ardi, Gadis, Juminten, atau Asep)
5. Klik tombol "Lakukan Inferensi Audio" untuk menghasilkan suara
6. Audio akan diputar secara otomatis dan dapat diunduh

### 2. Menggunakan REST API

Aplikasi ini menyediakan REST API yang dapat digunakan untuk integrasi dengan aplikasi lain.

#### Endpoint yang Tersedia:

**a. Generate TTS Audio**
```bash
POST /api/tts
Content-Type: application/json

{
  "text": "Halo, selamat pagi Indonesia!",
  "speaker": "ardi",
  "speed": 0.8,
  "language": "Indonesian"
}
```

**b. Mendapatkan Daftar Pembicara**
```bash
GET /api/speakers
```

**c. Mendapatkan Daftar Bahasa**
```bash
GET /api/languages
```

**d. Health Check**
```bash
GET /health
```

#### Contoh Penggunaan dengan cURL:

```bash
# Generate audio dari teks
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Halo, selamat pagi Indonesia!",
    "speaker": "ardi",
    "speed": 0.8
  }' \
  --output audio.wav

# Mendapatkan daftar pembicara
curl http://localhost:5000/api/speakers
```

#### Contoh Penggunaan dengan Python:

```python
import requests

url = "http://localhost:5000/api/tts"
payload = {
    "text": "Selamat datang di TTS Indonesia",
    "speaker": "gadis",
    "speed": 0.8,
    "language": "Indonesian"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    with open("output.wav", "wb") as f:
        f.write(response.content)
    print("Audio berhasil dihasilkan!")
else:
    print(f"Error: {response.json()}")
```

### 3. Instalasi dan Menjalankan Lokal

#### Prasyarat:
- Python 3.10 atau lebih tinggi
- espeak-ng (untuk text processing)
- libsndfile1 (untuk audio processing)

#### Langkah-langkah:

**a. Clone Repository**
```bash
git clone https://github.com/oclab/TTS-Indonesia-Gratis.git
cd TTS-Indonesia-Gratis
```

**b. Install Dependencies Sistem (Ubuntu/Debian)**
```bash
sudo apt-get update
sudo apt-get install -y build-essential libsndfile1 espeak-ng
```

**c. Install Dependencies Python**
```bash
pip install -r requirements.txt
```

**d. Unduh Model TTS**

Model dapat diunduh dari [Releases](https://github.com/Wikidepia/indonesian-tts/releases/). Letakkan file model di direktori `models/` dan file config di direktori `config/`.

**e. Jalankan Aplikasi**
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:3000`. Akses dokumentasi API Swagger di `http://localhost:3000/swagger/`.

### 4. Menggunakan Docker

#### Menggunakan Docker Compose (Recommended):

```bash
# Clone repository
git clone https://github.com/oclab/TTS-Indonesia-Gratis.git
cd TTS-Indonesia-Gratis

# Jalankan dengan docker-compose
docker-compose up -d

# Cek logs
docker-compose logs -f

# Stop service
docker-compose down
```

#### Menggunakan Docker Manual:

```bash
# Build image
docker build -t tts-indonesia .

# Run container
docker run -d \
  --name tts-indonesia-api \
  -p 5000:5000 \
  -e PORT=5000 \
  -e DEBUG=false \
  tts-indonesia

# Cek logs
docker logs -f tts-indonesia-api

# Stop container
docker stop tts-indonesia-api
docker rm tts-indonesia-api
```

Setelah aplikasi berjalan, Anda dapat mengakses:
- API Documentation (Swagger): `http://localhost:5000/swagger/`
- Health Check: `http://localhost:5000/health`
- API Endpoint: `http://localhost:5000/api/`

## Contoh Suara


https://github.com/user-attachments/assets/905c4d71-686d-4270-a6dd-f134fa8dbefc


https://github.com/user-attachments/assets/a0d2089b-4a92-4eb4-8f1f-02b60294ce93


https://github.com/user-attachments/assets/3601206d-3a9f-41cc-ab7a-2c36bdbbd359


https://github.com/user-attachments/assets/ce1730e2-340b-41ea-b436-d691328a07af



- [Wibowo](audio_samples/wibowo.wav)
- [Gadis](audio_samples/gadis.wav)
- [Juminten (Jawa)](audio_samples/juminten_jawa.wav)
- [Asep (Sunda)](audio_samples/asep_sunda.wav)

## Teknologi yang Digunakan

- [Gradio](https://gradio.app/) untuk antarmuka pengguna
- [G2P](https://github.com/kaldi-asr/g2p-seq2seq) untuk konversi teks ke fonem
- Model TTS yang dilatih khusus untuk bahasa Indonesia, Jawa, dan Sunda

# Unduh Model TTS Bahasa Indonesia

File Model dapat diunduh di : [Releases](https://github.com/Wikidepia/indonesian-tts/releases/) tab.

**DO NOT USE FOR COMMERCIAL PURPOSES!**

## Model changelog

### v1.2 (Aug 12, 2022)

Finetuned from v1.1 model on:

- 4 hours of Audiobook dataset
- 2000 sample of Azure TTS
- High quality TTS data for Javanese & Sundanese

### v1.1 (Aug 6, 2022)

Finetuned from LJSpeech model on:

- 4 hours of Audiobook dataset
- 2000 sample of Azure TTS

### v1.0 (Jun 23, 2022)

Trained from scratch on:

- 4 hours of Audiobook dataset.

## Lisensi

Proyek ini dilisensikan di bawah lisensi GPL-3.0. Lihat file [LICENSE](LICENSE) untuk informasi lebih lanjut.

## Kontribusi

Kami menyambut kontribusi dari siapa pun. Untuk berkontribusi, silakan buat _pull request_ atau buka _issue_ untuk mendiskusikan perubahan yang ingin Anda lakukan.

## Kontak

Untuk informasi lebih lanjut, silakan hubungi drat di : https://drat.github.io

---

Energi Semesta Digital © 2024 drat. | 🇮🇩 Untuk Indonesia Jaya!
