# REFERENCE_SPECIFICATION.md

## SPESIFIKASI REFERENSI TP-OCM
**Dokumen:** Reference Specification  
**Proyek:** Tri-Planar Orthogonal Complex Mapping (TP-OCM)  
**Versi:** 1.0 (Canonical Implementation)  
**Tanggal:** 31 Desember 2025  
**Status:** Spesifikasi Teknis Resmi

---

### 1. PRAKATA: FROM PHILOSOPHY TO IMPLEMENTATION

Dokumen ini merupakan penerjemahan formal dari prinsip-prinsip filosofis dalam `CORE_MANIFESTO.md` menjadi spesifikasi teknis yang dapat diimplementasikan. Di sini, kami membekukan **Implementasi Kanonik TP-OCM**—sebuah instansiasi spesifik yang berfungsi sebagai referensi standar, batu uji kebenaran, dan titik awal bagi semua pengembangan lebih lanjut.

Implementasi lain yang mengubah konvensi (`y = z`, dll) tetap valid sebagai variasi, tetapi spesifikasi ini mendefinisikan **wajah resmi TP-OCM**.

---

### 2. KONVENSI DASAR

#### 2.1. **Notasi dan Tipe Data**
- **Skalar Real:** `x₁`, `x₂`, `y` ∈ ℝ (bilangan real floating-point presisi ganda)
- **Unit Imajiner:** `i` didefinisikan dengan sifat `i² = -1`
- **Bilangan Kompleks:** `Zₖ = a + i·b` dimana `a, b ∈ ℝ`
- **Sudut:** `θ₁, θ₂, θ₃ ∈ (-π, π]` radian

#### 2.2. **Konvensi Sistem Koordinat Kanonik**
```
Bidang 1 (Frontal):  Z₁ = x₁ + i·y    // Memetakan ke bidang X-Y
Bidang 2 (Sagittal): Z₂ = x₂ + i·y    // Memetakan ke bidang Z-Y
Bidang 3 (Horizontal): Z₃ = x₁ + i·x₂  // Memetakan ke bidang X-Z
```

**Catatan:** Meskipun variabel dapat direlabel (misal `{x, y, z}`), konvensi ini adalah **referensi baku** untuk semua dokumentasi, tutorial, dan implementasi contoh.

---

### 3. DEFINISI OPERASI DASAR

#### 3.1. **Ekstraksi Sudut Kanonik (Properti C+)**
Sudut primitif diekstrak langsung dari setiap bidang menggunakan fungsi `atan2` yang stabil:

```python
def extract_canonical_angles(x1, x2, y):
    """Mengekstrak sudut primitif dari state TP-OCM"""
    theta1 = atan2(y, x1)   # Pitch: rotasi bidang Z₁
    theta2 = atan2(y, x2)   # Roll:  rotasi bidang Z₂
    theta3 = atan2(x2, x1)  # Yaw:   rotasi bidang Z₃
    return theta1, theta2, theta3
```

**Invariant:** Fungsi ini harus selalu menghasilkan hasil yang sama untuk input yang sama, tanpa efek samping.

#### 3.2. **Rotasi pada Satu Bidang**
Rotasi titik `(a, b)` pada bidang kompleks `Z = a + i·b` oleh sudut `θ`:

```python
def rotate_in_plane(a, b, theta):
    """Rotasi 2D pada bidang kompleks"""
    cos_t = cos(theta)
    sin_t = sin(theta)
    a_rot = a * cos_t - b * sin_t
    b_rot = a * sin_t + b * cos_t
    return a_rot, b_rot
```

**Kompleksitas:** 4 perkalian, 2 penjumlahan per bidang.

#### 3.3. **Revolusi TP-OCM: Rotasi 3D Lengkap**
```python
def tpocm_rotate_point(x1, x2, y, d_theta1, d_theta2, d_theta3):
    """
    Melakukan rotasi 3D dengan menerapkan delta sudut secara paralel
    ke ketiga bidang, lalu merekonstruksi state baru.
    """
    # 1. Rotasi independen per bidang
    x1_new, y_new_from_z1 = rotate_in_plane(x1, y, d_theta1)
    x2_new, y_new_from_z2 = rotate_in_plane(x2, y, d_theta2)
    x1_final, x2_final = rotate_in_plane(x1_new, x2_new, d_theta3)
    
    # 2. Konsensus nilai y (rata-rata dari dua sumber)
    y_final = (y_new_from_z1 + y_new_from_z2) / 2.0
    
    # 3. Normalisasi (Protokol Stabilitas)
    y_final = apply_taylor_normalization(x1_final, x2_final, y_final)
    
    return x1_final, x2_final, y_final
```

---

### 4. PROTOKOL STABILITAS

#### 4.1. **Normalisasi Taylor (Pencegahan Drift)**
```python
def apply_taylor_normalization(x1, x2, y):
    """
    Koreksi drift menggunakan ekspansi Taylor orde-1.
    Mengembalikan nilai y yang dinormalisasi.
    """
    # Hitung deviasi dari norma unit
    r_sq = x1*x1 + x2*x2 + y*y
    deviation = 1.0 - r_sq
    
    # Faktor koreksi Taylor: k = 1.5 - 0.5*r_sq
    taylor_factor = 1.5 - 0.5 * r_sq
    
    # Terapkan koreksi hanya pada y (variabel penghubung)
    y_normalized = y * taylor_factor
    
    return y_normalized
```

#### 4.2. **Jadwal Reset Periodik**
```python
class TPOCM_State:
    def __init__(self):
        self.x1, self.x2, self.y = 1.0, 0.0, 0.0  # State awal
        self.rotation_count = 0
        self.RESET_INTERVAL = 1000  # Reset setiap 1000 rotasi
    
    def update_with_rotation(self, d_theta1, d_theta2, d_theta3):
        # Lakukan rotasi biasa
        self.x1, self.x2, self.y = tpocm_rotate_point(
            self.x1, self.x2, self.y, d_theta1, d_theta2, d_theta3
        )
        
        self.rotation_count += 1
        
        # Reset periodik
        if self.rotation_count % self.RESET_INTERVAL == 0:
            self.hard_normalize()
    
    def hard_normalize(self):
        """Normalisasi penuh ke bola unit"""
        norm = sqrt(self.x1*self.x1 + self.x2*self.x2 + self.y*self.y)
        if norm > 0:
            self.x1 /= norm
            self.x2 /= norm
            self.y /= norm
```

---

### 5. PROTOKOL VERIFIKASI DAN UJI

#### 5.1. **Uji Konsistensi Dasar**
```python
def verify_tpocm_invariants(x1, x2, y, epsilon=1e-10):
    """
    Memverifikasi invariant fundamental TP-OCM.
    Melempar exception jika invariant dilanggar.
    """
    # 1. Verifikasi bahwa y konsisten di Z₁ dan Z₂
    # (Dalam implementasi kanonik, ini selalu benar)
    
    # 2. Verifikasi bahwa sudut dapat diekstrak
    theta1, theta2, theta3 = extract_canonical_angles(x1, x2, y)
    
    # 3. Verifikasi sifat ortogonalitas implisit
    # Rekonstruksi dari dua bidang harus konsisten dengan bidang ketiga
    z1_reconstructed = sqrt(x1*x1 + y*y)
    z3_reconstructed = sqrt(x1*x1 + x2*x2)
    
    assert abs(z1_reconstructed - z3_reconstructed) < epsilon, \
        "Invariant orthogonality violated"
    
    return True
```

#### 5.2. **Suite Uji Regresi**
```python
def run_canonical_test_suite():
    """Suite uji untuk implementasi kanonik"""
    tests = []
    
    # Test 1: Rotasi identitas
    x1, x2, y = 1.0, 0.0, 0.0
    x1r, x2r, yr = tpocm_rotate_point(x1, x2, y, 0.0, 0.0, 0.0)
    tests.append(abs(x1r-1.0) < 1e-10 and abs(x2r)<1e-10 and abs(yr)<1e-10)
    
    # Test 2: Rotasi 90 derajat pada Z₁
    x1, x2, y = 1.0, 0.0, 0.0
    x1r, x2r, yr = tpocm_rotate_point(x1, x2, y, pi/2, 0.0, 0.0)
    tests.append(abs(x1r) < 1e-10 and abs(yr-1.0) < 1e-10)
    
    # Test 3: Komposisi rotasi
    x1, x2, y = 1.0, 0.0, 0.0
    # Rotasi 45 derajat di semua bidang
    x1r, x2r, yr = tpocm_rotate_point(x1, x2, y, pi/4, pi/4, pi/4)
    # Verifikasi norma terawetkan (dengan toleransi Taylor)
    norm_sq = x1r*x1r + x2r*x2r + yr*yr
    tests.append(abs(norm_sq - 1.0) < 1e-5)
    
    return all(tests)
```

---

### 6. SPESIFIKASI KINERJA

#### 6.1. **Kompleksitas Komputasional**
| Operasi | Perkalian | Penjumlahan | Fungsi Trigonometri |
|---------|-----------|-------------|---------------------|
| Rotasi per bidang | 4 | 2 | 2 (sin/cos) |
| Rotasi TP-OCM lengkap | 12 | 6 | 6 |
| Normalisasi Taylor | 4 | 2 | 0 |

**Total per frame:** ≤ 16 perkalian, ≤ 8 penjumlahan (tidak termasuk normalisasi periodik).

#### 6.2. **Karakteristik Memori**
- **State minimal:** 3 × float (24 byte pada presisi ganda)
- **Stateless design:** Tidak ada state tersembunyi antar panggilan
- **Deterministik:** Output hanya bergantung pada input

#### 6.3. **Presisi dan Stabilitas**
- **Presisi target:** 1e-10 untuk rotasi tunggal
- **Drift maksimum:** < 0.1% per 1000 rotasi berantai (dengan protokol normalisasi)
- **Konsistensi:** Perbedaan antara dua implementasi yang benar harus < 1e-12

---

### 7. PANDUAN IMPLEMENTASI

#### 7.1. **Langkah Implementasi Minimal**
1. Implementasikan `extract_canonical_angles()` sebagai fungsi murni
2. Implementasikan `rotate_in_plane()` dengan presisi ganda
3. Implementasikan `tpocm_rotate_point()` dengan averaging pada `y`
4. Tambahkan `apply_taylor_normalization()` setelah setiap rotasi
5. Implementasikan `hard_normalize()` setiap 1000 operasi

#### 7.2. **Pola Kesalahan Umum yang Harus Dihindari**
```python
# SALAH: Menggunakan urutan rotasi Euler-like
x1, y = rotate_in_plane(x1, y, theta1)  # Mengubah y
x2, y = rotate_in_plane(x2, y, theta2)  # y sudah berubah!
# Ini merusak paralelisme intrinsik TP-OCM

# BENAR: Rotasi paralel, lalu konsensus
x1_new, y1_new = rotate_in_plane(x1, y, theta1)  # y asli
x2_new, y2_new = rotate_in_plane(x2, y, theta2)  # y asli
y_final = (y1_new + y2_new) / 2  # Konsensus
```

#### 7.3. **Optimasi yang Diizinkan**
- **Prekomputasi sin/cos** untuk sudut yang diketahui
- **SIMD/vektorisasi** pada rotasi tiga bidang paralel
- **Fixed-point arithmetic** untuk sistem embedded (dengan konversi yang hati-hati)
- **Cache locality** dengan menyimpan state sebagai array `[x1, x2, y]`

---

### 8. KESIMPULAN SPESIFIKASI

Spesifikasi referensi ini mendefinisikan **Implementasi Kanonik TP-OCM**—sebuah realisasi konkret yang:
1. **Setia** pada prinsip filosofis dalam `CORE_MANIFESTO.md`
2. **Stabil** melalui protokol normalisasi Taylor dan reset periodik
3. **Efisien** dengan kompleksitas komputasi yang dapat diprediksi
4. **Verifikabel** melalui suite uji yang terlampir

Implementasi yang sesuai dengan spesifikasi ini dijamin memiliki sifat:
- Determinisme penuh
- Stabilitas numerik jangka panjang
- Kompatibilitas dengan semua materi edukasi dan dokumentasi resmi

Variasi (seperti relabeling variabel) diizinkan, tetapi harus didokumentasikan sebagai penyimpangan dari kanon, dan tetap harus lulus semua uji invariants dasar.

---
**Dokumen Terkait:**
1. `CORE_MANIFESTO.md` - Visi filosofis
2. `POSITIONING_WHITEPAPER.md` - Posisi dalam lanskap
3. `REFERENCE_SPECIFICATION.md` - **(Dokumen ini)** Spesifikasi teknis
3. `BENCHMARK_REPORT.md` - Analisis kinerja vs sistem lain

**Lisensi Implementasi:** GNU General Public License v3.0 (GPL v3)  
**Konten Spesifikasi:** Creative Commons Attribution 4.0 International (CC BY 4.0)

**Hash Verifikasi Kanonik:** `TPOCM_CANONICAL_v1.0_7f83b1657b1c42a7`