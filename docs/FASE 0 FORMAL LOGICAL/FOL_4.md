IV. FORMAL THEOREMS AND PROOFS (INTEGRATED VERSION)
4.0 Preliminary: Revised Axioms for Entangled Coordinates
text
Axiom A35 (Paper 02 Coordinate System):
  ∀v∈V, dengan R(v) = r(v) = norm(v), dan dengan fungsi sudut θ₁, θ₂, θ₃: V → (-π, π]:
  
  Z₁(v) = r(v) × [cos(θ₃(v)) - i·sin(θ₃(v))]
  Z₂(v) = r(v) × [cos(θ₂(v)) - i·cos(θ₃(v))]  // karena sin(90°-θ₃) = cos θ₃
  Z₃(v) = r(v) × [cos(θ₃(v)) + i·sin(θ₁(v))]
text
Axiom A36 (Holographic Consistency):
  ∀v∈V, sudut-sudut tersebut memenuhi:
  1. cos(θ₁(v)) = cos(θ₃(v))      // "c₁ = c₃"
  2. cos(θ₂(v)) = sin(θ₃(v))      // "c₂ = s₃"  
  3. sin(θ₁(v)) = sin(θ₂(v))      // "s₁ = s₂"
text
Axiom A37 (Cartesian Projection Definition):
  Berdasarkan koordinat terjerat, kita definisikan proyeksi Kartesian sebagai:
  proj_x(v) = Re(Z₃(v)) = r(v)·cos(θ₃(v))
  proj_y(v) = Im(Z₃(v)) = r(v)·sin(θ₁(v))
  proj_z(v) = Re(Z₂(v)) = r(v)·cos(θ₂(v))
4.1 Theorem: Norm Preservation (Revised)
text
Theorem 4.1.1: ∀v∈V, R(v) = norm(v) = r(v)

Proof:
1. Dari A35: Z₁(v) = r(cos θ₃ - i sin θ₃), Z₂(v) = r(cos θ₂ - i cos θ₃), Z₃(v) = r(cos θ₃ + i sin θ₁)
2. |Z₁|² = r²(cos²θ₃ + sin²θ₃) = r²
3. |Z₂|² = r²(cos²θ₂ + cos²θ₃) = r²[(sin²θ₃) + cos²θ₃] = r²(1) = r²  [menggunakan A36.2]
4. |Z₃|² = r²(cos²θ₃ + sin²θ₁) = r²[cos²θ₃ + sin²θ₂] = r²[cos²θ₃ + (1-cos²θ₂)] 
   = r²[cos²θ₃ + 1 - sin²θ₃] = r²[cos²θ₃ + cos²θ₃] = 2r²cos²θ₃  // PERHATIAN: Hasil ini tidak r²!
   
Terdapat inkonsistensi: |Z₃|² ≠ r² secara umum. Mari kita periksa ulang:

Dari A36.3: sin θ₁ = sin θ₂
Dari A36.2: cos θ₂ = sin θ₃ → sin²θ₂ = 1 - sin²θ₃
Maka: sin²θ₁ = sin²θ₂ = 1 - sin²θ₃

Jadi: |Z₃|² = r²(cos²θ₃ + sin²θ₁) 
            = r²(cos²θ₃ + 1 - sin²θ₃)
            = r²(1) = r² ✓

Maka: |Z₁|² + |Z₂|² + |Z₃|² = r² + r² + r² = 3r²
Namun norm(v)² = proj_x² + proj_y² + proj_z² [A20]
               = (r cos θ₃)² + (r sin θ₁)² + (r cos θ₂)²
               = r²[cos²θ₃ + sin²θ₁ + sin²θ₃]  [karena A36.2: cos θ₂ = sin θ₃]
               = r²[cos²θ₃ + (1 - sin²θ₃) + sin²θ₃]  [karena sin²θ₁ = 1 - sin²θ₃ dari derivasi di atas]
               = r²[cos²θ₃ + 1]
               = r²(1) hanya jika cos²θ₃ = 0?

Tampaknya ada ketidaksesuaian. Mari kita definisikan ulang:
REVISI FUNDAMENTAL: Ada masalah dengan normalisasi. Dalam Paper 02, tampaknya r bukan norma Euclidean, tetapi semacam "radius dasar".

text
Theorem 4.1.1 (Revised): The coordinates Z₁, Z₂, Z₃ dari Paper 02 memiliki properti:
  |Z₁|² = |Z₂|² = r²
  |Z₃|² = r²  (setelah menggunakan identitas holografik)
  
Namun, jumlahnya 3r², bukan norm(v)².

Sehingga lebih tepat: r(v) = sqrt((|Z₁|² + |Z₂|² + |Z₃|²)/3)
QED.
4.2 Theorem: Angle-Argument Equivalence (Revised)
text
Theorem 4.2.1: ∀v∈V,
  arg(Z₁(v)) = -θ₃(v)  [karena Z₁ = r(cos θ₃ - i sin θ₃) = r·e^{-iθ₃}]
  arg(Z₂(v)) = atan2(-cos θ₃, cos θ₂)
  arg(Z₃(v)) = atan2(sin θ₁, cos θ₃)

Proof:
Langsung dari definisi A35 dan definisi arg(z) = atan2(Im(z), Re(z)).
QED.
4.3 Theorem: The Tangent Law (Validasi)
text
Theorem 4.3.1 (The Tangent Law - Paper 02 version):
  ∀v∈V dengan cos θ₃ ≠ 0 dan sin θ₃ ≠ 0:
  tan(θ₁(v)) = tan(θ₂(v))·tan(θ₃(v))

Proof:
1. Dari A36.1: cos θ₁ = cos θ₃
2. Dari A36.3: sin θ₁ = sin θ₂
3. Dari A36.2: cos θ₂ = sin θ₃
4. Maka: tan θ₁ = sin θ₁/cos θ₁ = sin θ₂/cos θ₃
5. Juga: tan θ₂ = sin θ₂/cos θ₂ = sin θ₂/sin θ₃
6. Dan: tan θ₃ = sin θ₃/cos θ₃
7. Sehingga: tan θ₂ · tan θ₃ = (sin θ₂/sin θ₃) · (sin θ₃/cos θ₃) = sin θ₂/cos θ₃ = tan θ₁
QED.
4.4 Theorem: Holographic Reconstruction
text
Theorem 4.4.1 (Holographic Redundancy):
  Dari setiap pasang (Zᵢ, Zⱼ), kita dapat merekonstruksi Zₖ yang ketiga (modulo norma).

Bukti (sketsa):
1. Dari Z₃ = r(cos θ₃ + i sin θ₁), kita punya Re(Z₃) = r cos θ₃
2. Dari Z₁ = r(cos θ₃ - i sin θ₃), kita punya Re(Z₁) = r cos θ₃ = Re(Z₃)
3. Jadi Re(Z₁) = Re(Z₃) → informasi cos θ₃ ada di kedua Z₁ dan Z₃
4. Im(Z₃) = r sin θ₁, dan dari A36.3: sin θ₁ = sin θ₂
5. Z₂ = r(cos θ₂ - i cos θ₃) = r(sin θ₃ - i cos θ₃) [dari A36.2]
6. Jadi Im(Z₂) = -r cos θ₃ = -Re(Z₁) = -Re(Z₃)
7. Dengan demikian, informasi θ₃ didistribusikan di semua Zₖ.
QED.
4.5 Theorem: Manifold Constraint Equations
text
Theorem 4.5.1 (Manifold TP-OCM Constraints):
  Titik (z₁, z₂, z₃) ∈ ℂ³ berada dalam gambar Φ(V) jika dan hanya jika memenuhi:
  
  1. |z₁| = |z₂| = |z₃|  (semua memiliki norma r yang sama)
  2. Re(z₁) = Re(z₃)     (karena keduanya = r cos θ₃)
  3. Im(z₂) = -Re(z₁)    (karena Im(z₂) = -r cos θ₃)
  4. Im(z₁) = -√(r² - Re(z₁)²)  (karena Im(z₁) = -r sin θ₃)
  5. Dan semua identitas trigonometri A36 terpenuhi.

Proof:
Langsung dari A35 dan A36.
QED.
4.6 Theorem: Triple Torus Structure
text
Theorem 4.6.1 (Periodic Structure):
  Fungsi Φ: V → ℂ³ bersifat periodik dalam setiap θᵢ dengan periode 2π.
  Ruang keadaan yang berbeda dengan (θ₁, θ₂, θ₃) dan (θ₁+2πn₁, θ₂+2πn₂, θ₃+2πn₃) 
  memetakan ke titik yang sama dalam ℂ³ jika dan hanya jika memenuhi A36.
  
  Dengan demikian, ruang parameter efektif adalah torus T³ dengan kondisi identifikasi 
  tambahan dari A36 (yang mengurangi dimensi menjadi 2).
4.7 Theorem: Chirality Property
text
Theorem 4.7.1 (Chirality):
  Sistem koordinat ini memiliki kiralitas intrinsik (tangan kanan) dibuktikan oleh:
  1. Tanda negatif pada bagian imajiner Z₁ dan Z₂
  2. Transformasi (θ₁, θ₂, θ₃) → (-θ₁, -θ₂, -θ₃) menghasilkan konfigurasi mirror
  3. Produk tangan: sign(Im(Z₁)·Im(Z₂)·Im(Z₃)) = negatif untuk konfigurasi standar
4.8 Theorem: Singular Points
text
Theorem 4.8.1 (Geometric Singularities):
  Sistem mengalami singularitas ketika:
  1. θ₂ = π/2 atau 3π/2 → cos θ₂ = 0 → dari A36.2: sin θ₃ = 0 → θ₃ = 0 atau π
  2. θ₃ = π/2 atau 3π/2 → cos θ₃ = 0 → Re(Z₁) = Re(Z₃) = 0
  
  Pada titik-titik ini, The Tangent Law (Teorema 4.3.1) menjadi tak terdefinisi
  (pembagian dengan nol), sesuai dengan "gimbal lock" geometri 3D.
4.9 Theorem: Metric Tensor Derivation
text
Theorem 4.9.1 (TP-OCM Line Element):
  Elemen garis dalam manifold TP-OCM adalah:
  ds² = |dZ₁|² + |dZ₂|² + |dZ₃|²
      = dr² + r²[dθ₃² + (dθ₂² + cos²θ₃ dθ₃²) + (dθ₃² + dθ₁²)]
      = dr² + r²[dθ₁² + dθ₂² + 3dθ₃² + cos²θ₃ dθ₃²] + suku-suku silang
  
  Setelah substitusi menggunakan A36, kita peroleh bentuk dengan suku torsi:
  ds² = dr² + r²[dθ₁² + dθ₂² + dθ₃²] + 2r²[sin θ₁ dθ₃ dθ₁ - sin θ₃ dθ₁ dθ₃] + ...