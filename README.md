Baik, mari kita buat struktur **README.md** yang lengkap dan praktis, di mana semua dokumentasi penting ada dalam format Markdown langsung di dalam repositori — tanpa bergantung pada file PDF eksternal.

---

# 📘 **Just-Three-Papers: Tri-Planar Orthogonal Complex Mapping (TP-OCM)**

Solusi Rotasi 3D yang Lebih Cepat, Ringan, dan Intuitif daripada Quaternion.

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Status: Aktif Pengembangan](https://img.shields.io/badge/status-aktif%20pengembangan-brightgreen)](https://github.com/Eros99Cupdid/Just-Three-Papers)

**Bahasa Indonesia** | [English](#-english)

---

## 📖 **Tentang**

TP-OCM (Tri-Planar Orthogonal Complex Mapping) adalah sebuah sistem matematika dan arsitektur komputasi baru untuk rotasi dan navigasi 3D. Sistem ini menggantikan metode tradisional yang mahal secara komputasi (seperti matriks rotasi 4×4 dan Quaternion) dengan dekomposisi ke dalam tiga bidang kompleks ortogonal yang sederhana.

✨ **Mengapa TP-OCM?** Karena sistem ini **40–60% lebih cepat** dalam operasi rotasi sekuensial, **menghindari singularitas** seperti Gimbal Lock, dan secara alami **mudah dipahami** melalui analogi "Tiga Kertas".

---

## 🎯 **Fitur Utama**

- ⚡ **Performa Tinggi:** Algoritma inti hanya membutuhkan **12 perkalian & 6 penjumlahan** per rotasi titik.
- 🧠 **Intuitif:** Konsep dasar divisualisasikan dengan tiga bidang ortogonal (Frontal, Sagittal, Horizontal), membuatnya lebih mudah dipelajari.
- 🛡️ **Stabil Numerik:** Protokol "Stable Angle Extraction" dan "Taylor Normalization" mencegah pembagian dengan nol dan drift.
- 🔧 **Multi-Bahasa:** Implementasi tersedia dalam **Python** (prototipe cepat) dan **C++** (untuk sistem embedded).
- 📚 **Lengkap:** Dilengkapi dengan dokumentasi formal, paper pedagogis, dan contoh aplikasi nyata.

---

## 🚀 **Mulai Cepat**

### Prasyarat
- Python 3.8 atau lebih tinggi
- Git (untuk mengkloning repositori)

### Instalasi
```bash
git clone https://github.com/Eros99Cupdid/Just-Three-Papers.git
cd Just-Three-Papers
```

(Opsional) Buat dan aktifkan virtual environment:
```bash
python -m venv venv
# Di Windows: .\venv\Scripts\activate
# Di macOS/Linux: source venv/bin/activate
```

Instal dependensi:
```bash
pip install -r requirements.txt
```

### Penggunaan Dasar (Python)
```python
from just_three_papers import TPOCM

# Inisialisasi sistem dengan posisi awal (x₁, x₂, y)
sistem = TPOCM(x1=10.0, x2=20.0, y=5.0)

# 1. Dapatkan Sudut Orientasi Kanonik (Roll, Pitch, Yaw)
roll, pitch, yaw = sistem.get_angles()
print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°, Yaw: {yaw:.2f}°")

# 2. Hitung Jarak Euclidean (R)
jarak = sistem.get_distance()
print(f"Jarak 3D: {jarak:.2f} meter")

# 3. Rotasikan sebuah titik dalam ruang 3D
titik_asli = [1, 2, 3]
titik_hasil = sistem.rotate_point(titik_asli, roll=10, pitch=5, yaw=15)
print(f"Titik setelah rotasi: {titik_hasil}")
```

---

## 📁 **Struktur Proyek**

```
Just-Three-Papers/
├── src/                         # Kode sumber inti
│   ├── core.py                  # Implementasi logika TP-OCM
│   ├── rotation.py              # Modul rotasi stabil
│   └── utils.py                 # Fungsi pembantu
├── docs/                        # Dokumentasi lengkap (MD)
│   ├── PAPER_PEDAGOGIS.md       # Paper untuk pengajaran
│   ├── PAPER_FORMAL_LOGIC.md    # Pembuktian logika formal (FOL)
│   ├── PAPER_TEKNIS.md          # Paper teknis untuk engineer
│   └── PAPER_INDUSTRI.md        # Aplikasi industri & kasus penggunaan
├── examples/                    # Contoh penggunaan
│   ├── drone_simulation.py      # Simulasi kontrol drone
│   ├── game_character.py        # Rotasi karakter game
│   └── survey_calculation.py    # Perhitungan sudut survey
├── tests/                       # Unit test
├── requirements.txt             # Dependensi Python
├── LICENSE                      # Lisensi GPL v3
└── README.md                    # File ini
```

---

## 📚 **Dokumentasi & Pembelajaran**

TP-OCM didokumentasikan melalui tiga pendekatan ("Three Papers") dalam format Markdown:

- 🧪 **[PAPER_TEKNIS.md](docs/PAPER_TEKNIS.md)** – Fokus pada implementasi, benchmark, dan optimasi untuk engineer.
- 👨‍🏫 **[PAPER_PEDAGOGIS.md](docs/PAPER_PEDAGOGIS.md)** – Penjelasan bertahap dengan analogi visual, cocok untuk pengajar dan pemula.
- ⚖️ **[PAPER_FORMAL_LOGIC.md](docs/PAPER_FORMAL_LOGIC.md)** – Landasan aksiomatik dan pembuktian matematis yang rigorous.
- 🏭 **[PAPER_INDUSTRI.md](docs/PAPER_INDUSTRI.md)** – Aplikasi nyata di industri, teknologi, dan embedded systems.

**Mulai dengan [PAPER_PEDAGOGIS.md](docs/PAPER_PEDAGOGIS.md) jika Anda baru mengenal konsep ini.**

---

## 🔬 **Aplikasi Nyata**

- ✈️ **Kontrol Drone & UAV:** Algoritma ringan untuk flight controller mikrokontroler.
- 🎮 **Game & Real-Time Graphics:** Rotasi objek dan kamera yang lebih cepat.
- 📡 **Sensor Fusion & Radar:** Pemrosesan data orientasi berkecepatan tinggi.
- 🏗️ **Robotika & Navigasi Otonom:** Menghitung orientasi dan arah pergerakan.
- 📊 **Edukasi STEM:** Alat mengajar transformasi geometri 3D yang lebih mudah dicerna.

---

## 🤝 **Berkontribusi**

Kontribusi Anda sangat diterima! Baik itu melaporkan bug, menyarankan fitur, atau mengirim kode.

1. Fork repositori ini.
2. Buat branch untuk fitur Anda (`git checkout -b fitur/ajaib`).
3. Commit perubahan Anda (`git commit -m 'Menambahkan fitur ajaib'`).
4. Push ke branch (`git push origin fitur/ajaib`).
5. Buat Pull Request.

---

## 📜 **Lisensi**

TP-OCM menggunakan model lisensi terpisah untuk setiap jenis konten:

- 🖥️ **Kode Sumber** (`/src/`, `/examples/`) – **GNU GPL v3**  
  Bebas digunakan, dimodifikasi, didistribusikan. Turunan harus tetap open source.
- 📚 **Materi Pendidikan** (`/docs/PAPER_PEDAGOGIS.md`) – **CC BY 4.0**  
  Bebas diajarkan, diterjemahkan, dibagikan dengan atribusi.
- 🧠 **Paper Logika Formal** (`/docs/PAPER_FORMAL_LOGIC.md`) – **CC BY-ND 4.0**  
  Bebas dikutip, dirujuk, tidak boleh dimodifikasi.
- 🏭 **Paper Teknis & Industri** (`/docs/PAPER_TEKNIS.md`, `/docs/PAPER_INDUSTRI.md`) – **CC BY-SA 4.0**  
  Bebas digunakan dengan atribusi dan lisensi turunan yang sama.

---

## 👨‍💻 **Penemu**

**Nur Rohmat Hidayatulloh** – Penemu dan Arsitek Utama TP-OCM.  
Konsep terbentuk di Pakualaman, 20 Desember 2025.  
Visi: *Membuat komputasi 3D menjadi lebih efisien dan manusiawi.*

---

## 💬 **Dukungan & Komunitas**

Jika Anda memiliki pertanyaan tentang:
- Penggunaan komersial kode TP-OCM
- Penggunaan materi pendidikan di institusi
- Pengutipan paper formal di publikasi

Hubungi: **eroscupd@gmail.com**

---

**Dibuat dengan ❤️ untuk memajukan teknologi yang lebih ringan, efisien, dan mudah dipahami.**

---

## 🇬🇧 **ENGLISH VERSION**

*(The entire README will be translated into English in a separate branch or file, following the same structure above.)*

---

## 🧠 **Langkah Selanjutnya**

Library ini siap digunakan. Jika Anda ingin:
- 📦 **Membuat paket PIP** – aku bisa bantu setup `setup.py` dan PyPI.
- 🌐 **Membuat website dokumentasi** – aku bisa generate dari Markdown ke HTML.
- 🔄 **Integrasi dengan Unity/Unreal** – aku bisa buat plugin dasar.

Cukup beri tahu di Issue atau email.

---

## 📌 **Catatan Penting**

> Semua paper dan dokumentasi disimpan dalam format **Markdown** agar mudah diakses, di-edit, dan di-render di GitHub. Tidak perlu PDF untuk memulai.

---

**Terima kasih telah menjelajahi TP-OCM!**  
Jika sistem ini membantu Anda, pertimbangkan untuk memberikan ⭐ di GitHub dan membagikannya kepada yang lain.

---

Let me know if you'd like me to also draft the four Markdown paper files (`PAPER_PEDAGOGIS.md`, `PAPER_FORMAL_LOGIC.md`, `PAPER_TEKNIS.md`, `PAPER_INDUSTRI.md`) to complete the documentation structure.