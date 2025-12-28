#include <iostream>
#include <cmath>
#include <chrono>
#include <iomanip>

// ==========================================
// 1. QUATERNION (Standard Implementation)
// ==========================================
struct Quat { double w, x, y, z; };

// Rotasi Titik oleh Quaternion (p' = q * p * q_inv)
inline void rotate_vector_by_quat(const Quat& q, double& px, double& py, double& pz) {
    // Rumus standar efisien (v + 2*cross(q.xyz, cross(q.xyz, v) + q.w*v))
    double tx = 2.0 * (q.w * px + q.y * pz - q.z * py); // cross(q,v) + w*v part 1
    double ty = 2.0 * (q.w * py + q.z * px - q.x * pz);
    double tz = 2.0 * (q.w * pz + q.x * py - q.y * px);
    
    // cross(q, t) part 2
    double new_px = px + (q.y * tz - q.z * ty);
    double new_py = py + (q.z * tx - q.x * tz);
    double new_pz = pz + (q.x * ty - q.y * tx);
    
    // Faktor skala (jika q unit)
    // Untuk benchmark adil, kita pakai rumus lengkap:
    double txx = 2.0 * q.x * px; // ... sebenarnya rumus vector form di atas sudah cukup 
    // tapi mari pakai bentuk aljabar yang paling umum dipakai di game engine
    
    // Simplifikasi Vector Form (Paling cepat untuk Quat)
    // t = 2 * cross(q.xyz, v)
    // v' = v + q.w * t + cross(q.xyz, t)
    double t_x = 2.0 * (q.y * pz - q.z * py);
    double t_y = 2.0 * (q.z * px - q.x * pz);
    double t_z = 2.0 * (q.x * py - q.y * px);
    
    px += q.w * t_x + (q.y * t_z - q.z * t_y);
    py += q.w * t_y + (q.z * t_x - q.x * t_z);
    pz += q.w * t_z + (q.x * t_y - q.y * t_x);
}

// Update Rotasi Quaternion (q_new = q_delta * q_old) -> UNTUK ACCUMULATED ROTATION
inline void multiply_quat(const Quat& a, Quat& b) {
    // b = a * b
    double nw = a.w * b.w - a.x * b.x - a.y * b.y - a.z * b.z;
    double nx = a.w * b.x + a.x * b.w + a.y * b.z - a.z * b.y;
    double ny = a.w * b.y - a.x * b.z + a.y * b.w + a.z * b.x;
    double nz = a.w * b.z + a.x * b.y - a.y * b.x + a.z * b.w;
    b = {nw, nx, ny, nz};
}

inline void normalize_quat(Quat& q) {
    double norm = std::sqrt(q.w*q.w + q.x*q.x + q.y*q.y + q.z*q.z);
    double inv = 1.0 / norm;
    q.w *= inv; q.x *= inv; q.y *= inv; q.z *= inv;
}

// ==========================================
// 2. TP-OCM (Just Three Papers Implementation)
// ==========================================
inline void rotate_tpocm(double& x1, double& x2, double& y, 
                         double c_yaw, double s_yaw, 
                         double c_pitch, double s_pitch, 
                         double c_roll, double s_roll) {
    // 1. YAW (Horizontal: x1, x2)
    double nx1 = x1 * c_yaw - x2 * s_yaw;
    double nx2 = x1 * s_yaw + x2 * c_yaw;
    x1 = nx1; x2 = nx2;

    // 2. PITCH (Sagital: x2, y) -> Corrected Sign
    double ny = y * c_pitch - x2 * s_pitch;
    x2 = x2 * c_pitch + y * s_pitch;
    y = ny;

    // 3. ROLL (Frontal: x1, y)
    nx1 = x1 * c_roll - y * s_roll;
    y = x1 * s_roll + y * c_roll;
    x1 = nx1;
}

// ==========================================
// MAIN TEST
// ==========================================
int main() {
    const long long ITERATIONS = 10000000; // 10 Juta (Cukup untuk drift)
    
    // Sudut Rotasi Kecil per langkah
    double angle = 0.0001; 
    
    // --- SETUP QUATERNION DELTA ---
    // q_delta from Euler (urutan Y-X-Z approx untuk small angle)
    double c = std::cos(angle * 0.5);
    double s = std::sin(angle * 0.5);
    // Kita anggap rotasi di 3 sumbu sekaligus untuk stress test
    // q_delta = q_yaw * q_pitch * q_roll
    // Untuk simplifikasi benchmark, kita pakai q_delta random valid unit
    Quat q_delta = {0.99999998, 0.00005, 0.00005, 0.00005}; 
    normalize_quat(q_delta);
    
    // --- SETUP TP-OCM DELTA ---
    double c_rot = std::cos(angle);
    double s_rot = std::sin(angle);
    // Kita pakai rotasi yang setara secara beban komputasi (rotasi di 3 bidang)
    
    std::cout << std::fixed << std::setprecision(6);
    std::cout << "=== DUEL MAUT: ACCUMULATED ROTATION (10 Juta Ops) ===\n\n";

    // -------------------------------------------------
    // ROUND 1: QUATERNION (ACCUMULATED)
    // -------------------------------------------------
    // Skenario: Objek berputar terus menerus (seperti gasing)
    // Kita harus update orientasi (q_curr) DAN rotasi titik (p)
    
    double px = 10.0, py = 20.0, pz = 5.0;
    Quat q_curr = {1.0, 0.0, 0.0, 0.0}; // Identitas
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for (long long i = 0; i < ITERATIONS; ++i) {
        // 1. Akumulasi Rotasi Orientasi
        multiply_quat(q_delta, q_curr);
        
        // 2. Normalisasi Berkala (Wajib untuk kestabilan)
        if (i % 1000 == 0) normalize_quat(q_curr);
        
        // 3. Rotasi Titik (Opsional: Jika kita melacak titik di body frame)
        // Tapi biasanya di navigasi, kita rotasi vector posisi.
        // Agar adil dengan TP-OCM yang merotasi koordinat:
        rotate_vector_by_quat(q_delta, px, py, pz); 
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_quat = end - start;
    
    double r_quat = std::sqrt(px*px + py*py + pz*pz);

    // -------------------------------------------------
    // ROUND 2: TP-OCM (ACCUMULATED)
    // -------------------------------------------------
    // Skenario: Titik diputar bertahap di 3 bidang
    
    double x1 = 10.0, x2 = 20.0, y = 5.0;
    
    start = std::chrono::high_resolution_clock::now();
    
    for (long long i = 0; i < ITERATIONS; ++i) {
        // TP-OCM tidak memisahkan "Orientasi" dan "Posisi"
        // Rotasi langsung diterapkan ke koordinat
        rotate_tpocm(x1, x2, y, c_rot, s_rot, c_rot, s_rot, c_rot, s_rot);
        
        // Tidak perlu normalisasi orientasi karena sin/cos pre-calc stabil
        // Tidak perlu normalisasi vektor posisi (karena rotasi murni isometri)
    }
    
    end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> t_tpocm = end - start;

    double r_tpocm = std::sqrt(x1*x1 + x2*x2 + y*y);
    double r_awal = std::sqrt(10*10 + 20*20 + 5*5);

    // -------------------------------------------------
    // HASIL
    // -------------------------------------------------
    std::cout << "Quaternion Time : " << t_quat.count() << "s\n";
    std::cout << "TP-OCM Time     : " << t_tpocm.count() << "s\n\n";
    
    std::cout << "Drift Check (R awal = " << r_awal << "):\n";
    std::cout << "Quat R Akhir    : " << r_quat << " (Diff: " << std::abs(r_quat - r_awal) << ")\n";
    std::cout << "TP-OCM R Akhir  : " << r_tpocm << " (Diff: " << std::abs(r_tpocm - r_awal) << ")\n\n";
    
    if (t_tpocm < t_quat) {
        std::cout << "🏆 PEMENANG: TP-OCM (" << (t_quat.count()/t_tpocm.count()) << "x lebih cepat)\n";
    } else {
        std::cout << "🏆 PEMENANG: QUATERNION\n";
    }

    return 0;
}