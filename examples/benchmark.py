import time
import math
from tpocm import TPOCM
import random

def benchmark_tpocm(iterations=1_000_000):
    print(f"🚀 Memulai Benchmark TP-OCM ({iterations} iterasi)...")
    
    # Setup data acak untuk menghindari branch prediction optimization
    inputs = []
    for _ in range(1000):
        inputs.append((random.random()*100, random.random()*100, random.random()*100))
    
    start_time = time.perf_counter()
    
    # --- CORE LOOP ---
    # Simulasi: Ambil titik, rotasi sedikit, ambil sudut baru
    p = TPOCM(10.0, 20.0, 5.0)
    rot_step = 0.01
    
    for i in range(iterations):
        # Operasi Rotasi + Akses Properti Kompleks
        # TP-OCM sangat cepat karena properti z1,z2,z3 dihitung 'on-demand' (lazy)
        # atau sangat murah biayanya.
        p = p.rotate(d_yaw=rot_step, d_pitch=0.001)
        _ = p.yaw # Akses data
        
    # -----------------
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    ops_per_sec = iterations / duration
    
    print(f"✅ Selesai!")
    print(f"⏱️ Waktu Total: {duration:.4f} detik")
    print(f"⚡ Throughput : {ops_per_sec:,.0f} operasi/detik")
    print("-" * 30)

if __name__ == "__main__":
    benchmark_tpocm()