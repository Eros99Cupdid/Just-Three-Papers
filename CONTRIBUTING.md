# Panduan Berkontribusi pada TP-OCM

Terima kasih atas minat Anda untuk berkontribusi pada **Tri-Planar Orthogonal Complex Mapping (TP-OCM)**! Panduan ini dibuat untuk memastikan kontribusi berjalan lancar, koheren dengan filosofi sistem, dan sesuai dengan arsitektur lisensi yang telah ditetapkan.

## 🧭 Prinsip Dasar Kontribusi

Sebelum mulai, pahami prinsip inti yang mendasari proyek ini:

1.  **Menghormati Arsitektur Logika**: TP-OCM dibangun di atas landasan aksiomatik formal yang dilindungi. Kontribusi tidak boleh bertentangan dengan atau mengaburkan logika inti yang telah ditetapkan dalam `PAPER_FORMAL_LOGIC.md`.
2.  **Mengikuti Segmentasi Lisensi**: Setiap jenis konten memiliki lisensi berbeda. Kontributor harus memahami dan menghormati batasan ini.
3.  **Fokus pada Kemanfaatan**: Kontribusi harus memperkuat salah satu dari tiga pilar TP-OCM: **kejelasan konseptual**, **efisiensi implementasi**, atau **kemudahan akses pendidikan**.

## 📋 Jenis Kontribusi yang Kami Cari

Kami menyambut berbagai jenis kontribusi:

| Jenis Kontribusi | Cakupan & Contoh | Repositori Sasaran | Lisensi yang Berlaku |
| :--- | :--- | :--- | :--- |
| **Perbaikan Kode** | Bug fixes, optimasi kinerja, peningkatan API di `/src/` dan `/examples/`. | Kode sumber di `/src/` | **GNU GPL v3** |
| **Contoh & Tutorial** | Contoh aplikasi baru, notebook Jupyter, skrip demonstrasi di `/examples/`. | Kode contoh di `/examples/` | **GNU GPL v3** |
| **Dokumentasi Teknis** | Perbaikan kejelasan, penambahan diagram, penerjemahan `PAPER_TEKNIS.md`. | `/docs/PAPER_TEKNIS.md` | **CC BY-SA 4.0** |
| **Materi Pendidikan** | Penyederhanaan penjelasan, soal latihan, rencana ajar berdasarkan `PAPER_PEDAGOGIS.md`. | `/docs/PAPER_PEDAGOGIS.md` | **CC BY 4.0** |
| **Penerapan Industri** | Studi kasus, benchmark, panduan integrasi dengan sistem lain (ROS, Unity, dll). | `/docs/PAPER_INDUSTRI.md` | **CC BY-SA 4.0** |
| **Pelaporan Masalah** | Melaporkan bug, ketidakjelasan, atau kesalahan konseptual. | Issue Tracker GitHub | - |

## ⚠️ Kontribusi yang **Tidak** Dapat Diterima

1.  **Modifikasi Logika Inti**: Usulan yang secara substantif mengubah, mengurangi, atau mendistorsi aksioma, teorema, atau struktur pembuktian formal yang ada dalam `PAPER_FORMAL_LOGIC.md`. Diskusi untuk memperjelas dipersilakan; modifikasi langsung tidak.
2.  **Kontribusi Berlisensi Tertutup**: Kode atau dokumen yang membawa ketergantungan pada lisensi berpemilik yang bertentangan dengan GPL v3 atau CC BY-SA.
3.  **Konten yang Tidak Relevan**: Kontribusi yang tidak terkait langsung dengan peningkatan TP-OCM sebagai sistem navigasi, rotasi, atau pendidikan geometri 3D.

## 🚀 Alur Kerja Kontribusi

Ikuti langkah-langkah berikut untuk mengajukan kontribusi:

1.  **Buka Issue (Disarankan)**: Sebelum mengerjakan perubahan besar, bicarakan ide Anda di **Issue Tracker** GitHub. Ini memastikan kerja Anda selaras dengan visi proyek dan tidak bertabrakan dengan pekerjaan lain.
2.  **Fork Repositori**: Fork repositori `Just-Three-Papers` ke akun GitHub Anda.
3.  **Buat Branch**: Buat branch baru di fork Anda dengan nama deskriptif (misal: `fix/rotation-stability`, `docs/add-unity-example`).
4.  **Lakukan Perubahan**: Lakukan perubahan Anda di branch tersebut. Pastikan untuk:
    *   Mengikuti gaya kode yang ada (contoh: gunakan `snake_case` untuk fungsi Python).
    *   Menambahkan komentar yang jelas pada kode baru.
    *   Memperbarui dokumentasi yang relevan jika perlu.
    *   **SANGAT PENTING**: Tambahkan **header lisensi dan hak cipta** yang sesuai di bagian atas setiap file baru yang Anda buat (lihat panduan di bawah).
5.  **Uji Perubahan**: Pastikan perubahan Anda tidak merusak fungsionalitas yang ada. Jalankan tes yang tersedia jika ada.
6.  **Commit dan Push**: Commit perubahan Anda dengan pesan commit yang jelas dan deskriptif, lalu push ke fork Anda.
7.  **Ajukan Pull Request (PR)**: Buat Pull Request dari branch di fork Anda ke branch `main` repositori utama. Jelaskan perubahan Anda secara detail pada template PR.

## 📄 Panduan Spesifik Berdasarkan Jenis Konten

### Untuk Kontributor Kode (GPL v3)
- **Header File Wajib**: Setiap file kode sumber baru (`*.py`, `*.cpp`, dll) **harus** menyertakan header berikut di baris paling atas:
    ```python
    """
    --------------------------------------------------------------------
    Bagian dari Proyek Just-Three-Papers: TP-OCM (Tri-Planar Orthogonal Complex Mapping)
    Hak Cipta (C) 2025 Nur Rohmat Hidayatulloh
    Dilisensikan di bawah GNU General Public License v3.0 (GPL-3.0).
    Anda dapat memperoleh salinan lisensi di: https://www.gnu.org/licenses/gpl-3.0.html
    Kode ini adalah perangkat lunak bebas: Anda dapat menyebarluaskannya dan/atau memodifikasinya
    sesuai dengan ketentuan lisensi GPL v3.
    --------------------------------------------------------------------
    """
    ```
- **Kepatuhan terhadap Copyleft**: Pastikan kode Anda tidak menggabungkan pustaka dengan lisensi yang tidak kompatibel dengan GPL v3 (seperti lisensi BSD yang dimodifikasi dengan klausa iklan ketat).

### Untuk Kontributor Dokumentasi Teknis & Industri (CC BY-SA 4.0)
- **Header File Wajib**: Setiap dokumen Markdown baru di `/docs/` (kecuali logika formal) harus menyertakan:
    ```markdown
    > **Lisensi:** Dokumen ini dilisensikan di bawah Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).
    > © 2025 Nur Rohmat Hidayatulloh. Anda bebas untuk membagikan dan mengadaptasi dengan atribusi dan lisensi turunan yang sama.
    ```
- **Atribusi & ShareAlike**: Jika Anda mengadaptasi karya eksternal, pastikan karya tersebut kompatibel dengan CC BY-SA dan berikan atribusi yang sesuai. Semua turunan dari dokumen Anda harus tetap berlisensi CC BY-SA 4.0.

### Untuk Kontributor Materi Pendidikan (CC BY 4.0)
- **Header File Wajib**: Materi pedagogis baru harus menyertakan:
    ```markdown
    > **Lisensi:** Materi ini dilisensikan di bawah Creative Commons Attribution 4.0 International (CC BY 4.0).
    > © 2025 Nur Rohmat Hidayatulloh. Anda bebas untuk menggunakan, berbagi, dan beradaptasi dengan atribusi.
    ```
- **Kebebasan Adaptasi**: Anda memiliki kebebasan lebih besar untuk mengadaptasi dan menyusun ulang, tetapi **atribusi kepada penemu asli (Nur Rohmat Hidayatulloh) harus tetap disertakan**.

## ⚖️ Kebijakan Hak Cipta dan Lisensi Kontributor

Dengan mengajukan kontribusi ke repositori ini, Anda menyetujui bahwa:

1.  **Kepemilikan Anda Dipertahankan**: Anda tetap memegang hak cipta atas kontribusi kode atau dokumen yang Anda tulis.
2.  **Pemberian Lisensi**: Anda memberikan lisensi atas kontribusi Anda kepada proyek TP-OCM di bawah **lisensi yang sama dengan komponen yang Anda ubah/tambahkan** (GPL v3 untuk kode, CC BY-SA untuk dokumentasi teknis, dll).
3.  **Orisinalitas**: Anda menjamin bahwa kontribusi tersebut adalah karya orisinal Anda, atau Anda memiliki hak yang diperlukan untuk melisensikannya di bawah ketentuan di atas.

Untuk kontribusi signifikan ke kode inti, kami mungkin meminta Anda untuk menandatangani **Perjanjian Lisensi Kontributor (CLA)** elektronik sederhana di masa depan untuk memperjelas ketentuan ini. Ini akan dikomunikasikan secara transparan.

## ❓ Mendapatkan Bantuan

Jika Anda bingung tentang:
- Di mana harus memulai, lihat label `good first issue` di Issue Tracker.
- Apakah ide kontribusi Anda sesuai, ajukan diskusi di Issue.
- Detail teknis lisensi, baca `LICENSE_OVERVIEW.md`.

Terima kasih kembali atas komitmen Anda untuk membangun ekosistem TP-OCM yang lebih kuat dan terbuka! 🚀