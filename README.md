📘 Just-Three-Papers: Tri-Planar Orthogonal Complex Mapping (TP-OCM)
Solusi Rotasi 3D yang Lebih Cepat, Ringan, dan Intuitif daripada Quaternion.

https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/python-3.8+-blue.svg
https://img.shields.io/badge/status-aktif%2520pengembangan-brightgreen

Bahasa Indonesia | English

📖 Tentang
TP-OCM (Tri-Planar Orthogonal Complex Mapping) adalah sebuah sistem matematika dan arsitektur komputasi baru untuk rotasi dan navigasi 3D. Sistem ini menggantikan metode tradisional yang mahal secara komputasi (seperti matriks rotasi 4x4 dan Quaternion) dengan dekomposisi ke dalam tiga bidang kompleks ortogonal yang sederhana.

✨ Mengapa TP-OCM? Karena sistem ini 40-60% lebih cepat dalam operasi rotasi sekuensial, menghindari singularitas seperti Gimbal Lock, dan secara alami mudah dipahami melalui analogi "Tiga Kertas".

🎯 Fitur Utama
⚡ Performa Tinggi: Algoritma inti hanya membutuhkan 12 perkalian & 6 penjumlahan per rotasi titik.

🧠 Intuitif: Konsep dasar divisualisasikan dengan tiga bidang ortogonal (Frontal, Sagittal, Horizontal), membuatnya lebih mudah dipelajari.

🛡️ Stabil Numerik: Protokol "Stable Angle Extraction" dan "Taylor Normalization" mencegah pembagian dengan nol dan drift.

🔧 Multi-Bahasa: Implementasi tersedia dalam Python (prototipe cepat) dan C++ (untuk sistem embedded).

📚 Lengkap: Dilengkapi dengan dokumentasi formal, paper pedagogis, dan contoh aplikasi nyata.

🚀 Mulai Cepat
Prasyarat
Python 3.8 atau lebih tinggi

Git (untuk mengkloning repositori)

Instalasi
Kloning repositori ini:

bash
git clone https://github.com/Eros99Cupdid/Just-Three-Papers.git
cd Just-Three-Papers
(Opsional) Buat dan aktifkan virtual environment:

bash
python -m venv venv
# Di Windows: venv\Scripts\activate
# Di macOS/Linux: source venv/bin/activate
Instal dependensi:

bash
pip install -r requirements.txt
Penggunaan Dasar (Python)
python
from just_three_papers import TPOCM

# Inisialisasi sistem dengan posisi awal (x1, x2, y)
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

📁 Struktur Proyek
text
Just-Three-Papers/
├── src/                       # Kode sumber inti
│   ├── core.py                # Implementasi logika TP-OCM
│   ├── rotation.py            # Modul rotasi stabil
│   └── utils.py               # Fungsi pembantu
├── docs/                      # Dokumentasi lengkap
│   ├── paper_produksi.pdf     # Paper teknis untuk engineer
│   ├── paper_pedagogis.pdf    # Paper untuk pengajaran
│   ├── paper_formal_logic.pdf # Pembuktian logika formal (FOL)
│   └── API_REFERENCE.md       # Referensi API detail
├── examples/                  # Contoh penggunaan
│   ├── drone_simulation.py    # Simulasi kontrol drone
│   ├── game_character.py      # Rotasi karakter game
│   └── survey_calculation.py  # Perhitungan sudut survey
├── tests/                     # Unit test
├── requirements.txt           # Dependensi Python
├── LICENSE                    # Lisensi MIT
└── README.md                  # File ini

📚 Dokumentasi & Pembelajaran
TP-OCM didokumentasikan melalui tiga pendekatan ("Three Papers"):

🧪 Paper Produksi: Fokus pada implementasi, benchmark, dan optimasi untuk engineer.

👨‍🏫 Paper Pedagogis: Penjelasan bertahap dengan analogi visual, cocok untuk pengajar dan pemula.

⚖️ Paper Formal Logic (FOL): Landasan aksiomatik dan pembuktian matematis yang rigorous.

Mulai dengan Paper Pedagogis jika Anda baru mengenal konsep ini.

🔬 Aplikasi Nyata
✈️ Kontrol Drone & UAV: Algoritma ringan untuk flight controller mikrokontroler.

🎮 Game & Real-Time Graphics: Rotasi objek dan kamera yang lebih cepat.

📡 Sensor Fusion & Radar: Pemrosesan data orientasi berkecepatan tinggi.

🏗️ Robotika & Navigasi Otonom: Menghitung orientasi dan arah pergerakan.

📊 Edukasi STEM: Alat mengajar transformasi geometri 3D yang lebih mudah dicerna.

🤝 Berkontribusi
Kontribusi Anda sangat diterima! Baik itu melaporkan bug, menyarankan fitur, atau mengirim kode.

Fork repositori ini.

Buat branch untuk fitur Anda (git checkout -b fitur/ajaib).

Commit perubahan Anda (git commit -m 'Menambahkan fitur ajaib').

Push ke branch (git push origin fitur/ajaib).

Buat Pull Request.

Silakan baca Panduan Kontribusi untuk detail lebih lanjut.

📄 Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT - lihat file LICENSE untuk detailnya.

👨‍💻 Penemu
Nur Rohmat Hidayatulloh - Penemu dan Arsitek Utama TP-OCM.

Konsep lahir di Magelang, 6 Desember 1999.

Visi: Membuat komputasi 3D yang kuat menjadi lebih mudah diakses dan efisien.

🙏 Ucapan Terima Kasih
Kepada semua pendukung awal dan pemberi masukan.

Komunitas open-source yang menginspirasi.

Anda, untuk mengeksplorasi repositori ini!

💬 Dukungan & Komunitas
Laporkan Issue: Gunakan GitHub Issues.

Diskusi: Bergabunglah di [Discord Server] (tautan akan tersedia) atau diskusikan di bagian Discussions GitHub.

Email: Untuk pertanyaan mendalam atau kolaborasi, hubungi: [alamat-email-Anda]

Dibuat dengan ❤️ untuk memajuan teknologi yang lebih ringan dan cerdas.

🇬🇧 Just-Three-Papers: Tri-Planar Orthogonal Complex Mapping (TP-OCM)
A faster, lighter, and more intuitive 3D rotation solution than quaternions.

📖 About
TP-OCM (Tri-Planar Orthogonal Complex Mapping) is a novel mathematical and computational architecture for 3D rotation and navigation. It replaces computationally expensive traditional methods (like 4x4 rotation matrices and Quaternions) with a simple decomposition into three orthogonal complex planes.

✨ Why TP-OCM? Because it is 40-60% faster in sequential rotation operations, avoids singularities like Gimbal Lock, and is naturally easier to understand through the "Three Papers" analogy.

(The rest of the English translation would follow the same structure as above...)
