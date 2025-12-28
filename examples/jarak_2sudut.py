import math

def tpocm_reconstruct(r, theta3_yaw, theta2_pitch):
    """
    Mengembalikan koordinat (x1, x2, y) dari Radius dan 2 Sudut TP-OCM.
    
    Argumen:
    r            : Jarak Euclidean total (float)
    theta3_yaw   : Sudut Horizontal (radian) -> x2/x1
    theta2_pitch : Sudut Sagital (radian)    -> y/x2
    
    Return:
    (x1, x2, y)
    """
    
    # 1. Hitung Theta 1 (Roll) menggunakan Teorema Rantai Tangen
    # tan(t1) = tan(t2) * tan(t3)
    tan_t3 = math.tan(theta3_yaw)
    tan_t2 = math.tan(theta2_pitch)
    tan_t1 = tan_t2 * tan_t3
    
    # Kita perlu cos dan sin untuk proyeksi, bukan hanya tan.
    # Strategi: Proyeksi Trigonometri Bertahap (Chain Projection)
    
    # Dari Definisi: x2 = x1 * tan(t3)  dan  y = x2 * tan(t2)
    # Substitusi ke rumus modulus r^2 = x1^2 + x2^2 + y^2
    # r^2 = x1^2 + (x1*tan_t3)^2 + (x1*tan_t3*tan_t2)^2
    # r^2 = x1^2 * [1 + tan_t3^2 + (tan_t3*tan_t2)^2]
    
    # Maka x1 dapat diisolasi:
    denom = 1 + tan_t3**2 + (tan_t3 * tan_t2)**2
    x1 = r / math.sqrt(denom)
    
    # Rekonstruksi x2 dan y dari x1
    x2 = x1 * tan_t3
    y  = x2 * tan_t2
    
    # HANDLING TANDA (SIGN CORRECTION)
    # Karena kuadrat menghilangkan tanda, kita perlu cek kuadran theta3
    # Jika theta3 ada di kuadran 2 atau 3 (cos negatif), x1 harus negatif.
    if math.cos(theta3_yaw) < 0:
        x1 = -x1
        x2 = -x2 # x2 ikut berubah karena dia terikat x1
        y  = -y  # y ikut berubah karena terikat x2

    return x1, x2, y

# --- PENGUJIAN KONSISTENSI ---
if __name__ == "__main__":
    # Target Asli
    target = (10.0, 20.0, 5.0) 
    r_asli = math.sqrt(10**2 + 20**2 + 5**2)
    
    # Hitung Sudut Input (Simulasi data sensor)
    t3 = math.atan2(20, 10) # Yaw
    t2 = math.atan2(5, 20)  # Pitch
    
    print(f"Input: r={r_asli:.4f}, Yaw={math.degrees(t3):.2f}°, Pitch={math.degrees(t2):.2f}°")
    
    # Re-sintesis
    x1_rec, x2_rec, y_rec = tpocm_reconstruct(r_asli, t3, t2)
    
    print(f"\nHasil Rekonstruksi:")
    print(f"x1: {x1_rec:.4f} (Target: 10.0)")
    print(f"x2: {x2_rec:.4f} (Target: 20.0)")
    print(f"y : {y_rec:.4f}  (Target: 5.0)")
    
    error = abs(x1_rec-10) + abs(x2_rec-20) + abs(y_rec-5)
    print(f"\nTotal Error: {error:.10f}")