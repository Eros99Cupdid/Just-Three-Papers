import numpy as np
from scipy.optimize import minimize
from dataclasses import dataclass
from typing import List, Tuple, Dict
import warnings

@dataclass
class TPOCM_Navigation_System:
    """Sistem Navigasi TP-OCM Lengkap sesuai Paper 07"""
    
    # Parameter Cosmic Spin (Ω) dari Paper 16
    Ω_cosmic: float = 2.47e-3  # rad/s - Cosmic Spin Frequency
    
    # Tolerance untuk konsistensi
    consistency_tolerance: float = 1e-6
    
    def __post_init__(self):
        # Cache untuk optimasi
        self.path_cache = {}
        self.manifold_cache = {}
        
    # ===== 2.1. Algoritma Proyeksi Manifold =====
    def project_to_manifold(self, raw_vector: np.ndarray, 
                           max_iter: int = 100) -> Tuple[np.ndarray, float]:
        """
        Proyeksi vektor raw ke manifold TP-OCM
        Menggunakan Least Squares Adjustment untuk memenuhi Hukum Tangensial
        """
        
        x, y, z = raw_vector
        
        # Fungsi objektif: Minimalkan jarak ke manifold
        def objective(params):
            x_adj, y_adj, z_adj = params
            
            # Hitung sudut-sudut
            if abs(x_adj) < 1e-12:
                θ1 = np.pi/2 if y_adj > 0 else -np.pi/2
            else:
                θ1 = np.arctan2(y_adj, x_adj)
                
            if abs(z_adj) < 1e-12:
                θ2 = np.pi/2 if y_adj > 0 else -np.pi/2
            else:
                θ2 = np.arctan2(y_adj, z_adj)
                
            if abs(x_adj) < 1e-12:
                θ3 = np.pi/2 if z_adj > 0 else -np.pi/2
            else:
                θ3 = np.arctan2(z_adj, x_adj)
            
            # Hitung residual Hukum Tangensial
            lhs = np.tan(θ1)
            rhs = np.tan(θ2) * np.tan(θ3)
            
            # Juga hukrum jarak dari titik asal
            distance_penalty = np.linalg.norm([x_adj - x, y_adj - y, z_adj - z])
            
            return abs(lhs - rhs)**2 + 0.1 * distance_penalty**2
        
        # Initial guess (titik asal)
        initial_guess = np.array([x, y, z])
        
        # Constraints: Tidak boleh nol semua
        constraints = [
            {'type': 'ineq', 'fun': lambda p: np.linalg.norm(p) - 0.001}
        ]
        
        # Optimization
        result = minimize(objective, initial_guess, 
                         constraints=constraints,
                         method='SLSQP',
                         options={'maxiter': max_iter, 'ftol': 1e-10})
        
        if not result.success:
            warnings.warn(f"Projection failed: {result.message}")
        
        projected_vec = result.x
        
        # Hitung residual akhir
        residual = self.calculate_tangent_residual(projected_vec)
        
        # Cache result
        key = tuple(np.round(raw_vector, 6))
        self.manifold_cache[key] = (projected_vec, residual)
        
        return projected_vec, residual
    
    def calculate_tangent_residual(self, v: np.ndarray) -> float:
        """Hitung residual Hukum Tangensial untuk vektor v"""
        x, y, z = v
        
        if abs(x) < 1e-12 or abs(z) < 1e-12:
            return 0.0  # Vacuously true pada singularitas
        
        θ1 = np.arctan2(y, x)
        θ2 = np.arctan2(y, z)
        θ3 = np.arctan2(z, x)
        
        lhs = np.tan(θ1)
        rhs = np.tan(θ2) * np.tan(θ3)
        
        return abs(lhs - rhs)
    
    # ===== 4. ZONASI TOPOLOGI =====
    def determine_zone(self, v: np.ndarray) -> str:
        """
        Tentukan zona topologi berdasarkan stabilitas Hukum Tangensial
        """
        residual = self.calculate_tangent_residual(v)
        x, y, z = v
        
        # Zona C: Singular (Event Horizon)
        if abs(x) < 1e-6 or abs(z) < 1e-6:
            return "SINGULAR"
        
        # Zona B: Turbulen (Coupled Region)
        if residual > 0.1:  # High residual
            return "TURBULENT"
        
        # Zona A: Laminar (Stable)
        return "LAMINAR"
    
    def get_zone_properties(self, zone: str) -> Dict:
        """Properti masing-masing zona navigasi"""
        properties = {
            "LAMINAR": {
                "description": "Stable Region - Newtonian physics applicable",
                "navigation_cost": "Low",
                "phase_gradient": "Gentle",
                "quantum_effects": "Negligible",
                "examples": ["Vacuum space", "Normal atmosphere", "Solid objects"]
            },
            "TURBULENT": {
                "description": "Coupled Region - Strong non-local effects",
                "navigation_cost": "Medium to High",
                "phase_gradient": "Steep",
                "quantum_effects": "Strong",
                "examples": ["Chemical reactions", "Lightning storms", 
                           "High-frequency circuits", "Living cells"]
            },
            "SINGULAR": {
                "description": "Event Horizon - Dimensional gimbal lock",
                "navigation_cost": "Infinite (No-Fly Zone)",
                "phase_gradient": "Infinite",
                "quantum_effects": "Maximal",
                "examples": ["Black holes", "Quantum foam", 
                           "Big Bang singularity", "Measurement collapse"]
            }
        }
        return properties.get(zone, {})
    
    # ===== 3. NAVIGASI GEODESIK =====
    def find_geodesic_path(self, start_vec: np.ndarray, end_vec: np.ndarray,
                          n_points: int = 50, method: str = 'phase_surfing') -> Dict:
        """
        Temukan geodesik optimal antara dua titik di manifold TP-OCM
        
        Parameters:
        -----------
        start_vec, end_vec: Vektor 3D (x,y,z)
        n_points: Jumlah titik dalam path
        method: 'phase_surfing' atau 'euclidean'
        
        Returns:
        --------
        Dict berisi path dan metadata
        """
        
        # 1. Proyeksi ke manifold
        start_proj, start_res = self.project_to_manifold(start_vec)
        end_proj, end_res = self.project_to_manifold(end_vec)
        
        # 2. Cek zona
        start_zone = self.determine_zone(start_proj)
        end_zone = self.determine_zone(end_proj)
        
        if start_zone == "SINGULAR" or end_zone == "SINGULAR":
            raise ValueError(f"Cannot navigate through singular zones. "
                           f"Start: {start_zone}, End: {end_zone}")
        
        # 3. Hitung geodesik berdasarkan metode
        if method == 'phase_surfing':
            path = self._compute_phase_surfing_path(start_proj, end_proj, n_points)
            navigation_cost = self._calculate_navigation_cost(path, method='phase')
        else:  # Euclidean
            path = self._compute_euclidean_path(start_proj, end_proj, n_points)
            navigation_cost = self._calculate_navigation_cost(path, method='euclidean')
        
        # 4. Optimasi fase (sinkronisasi dengan rotasi kosmik)
        if method == 'phase_surfing':
            optimized_path = self._synchronize_with_cosmic_spin(path)
        else:
            optimized_path = path
        
        # 5. Analisis zona sepanjang path
        zone_analysis = self._analyze_zones_along_path(optimized_path)
        
        return {
            'raw_start': start_vec,
            'raw_end': end_vec,
            'projected_start': start_proj,
            'projected_end': end_proj,
            'start_residual': start_res,
            'end_residual': end_res,
            'start_zone': start_zone,
            'end_zone': end_zone,
            'method': method,
            'path': optimized_path,
            'navigation_cost': navigation_cost,
            'zone_analysis': zone_analysis,
            'distance_euclidean': np.linalg.norm(end_vec - start_vec),
            'distance_tpocm': self._calculate_tpocm_distance(optimized_path)
        }
    
    def _compute_phase_surfing_path(self, start: np.ndarray, end: np.ndarray, 
                                   n_points: int) -> np.ndarray:
        """
        Hitung path Phase Surfing - mengikuti gradien fase
        """
        # Parameterize dengan spline yang mengikuti garis equipotensial
        t = np.linspace(0, 1, n_points)
        
        # Linear interpolation sebagai baseline
        path_linear = start + t[:, np.newaxis] * (end - start)
        
        # Tambahkan komponen fase (spiral/helix)
        phase_component = np.zeros((n_points, 3))
        
        for i, ti in enumerate(t):
            # Fase bervariasi sinusoidal sepanjang path
            phase = 2 * np.pi * ti
            
            # Komponen fase tegak lurus terhadap perpindahan
            displacement = end - start
            if np.linalg.norm(displacement) > 1e-12:
                displacement_unit = displacement / np.linalg.norm(displacement)
                
                # Cari vektor tegak lurus
                if abs(displacement_unit[0]) > 0.1:
                    perpendicular = np.array([-displacement_unit[1], 
                                            displacement_unit[0], 0])
                else:
                    perpendicular = np.array([0, -displacement_unit[2], 
                                            displacement_unit[1]])
                
                perpendicular = perpendicular / np.linalg.norm(perpendicular)
                
                # Tambahkan komponen spiral
                amplitude = 0.1 * np.linalg.norm(displacement)
                phase_component[i] = amplitude * np.sin(phase) * perpendicular
        
        path = path_linear + phase_component
        
        # Proyeksi setiap titik ke manifold
        for i in range(n_points):
            projected, _ = self.project_to_manifold(path[i])
            path[i] = projected
        
        return path
    
    def _compute_euclidean_path(self, start: np.ndarray, end: np.ndarray,
                               n_points: int) -> np.ndarray:
        """Path Euclidean lurus"""
        t = np.linspace(0, 1, n_points)
        path = start + t[:, np.newaxis] * (end - start)
        
        # Proyeksi setiap titik
        for i in range(n_points):
            projected, _ = self.project_to_manifold(path[i])
            path[i] = projected
        
        return path
    
    def _synchronize_with_cosmic_spin(self, path: np.ndarray) -> np.ndarray:
        """
        Sinkronisasi path dengan rotasi kosmik Ω
        """
        n_points = len(path)
        optimized_path = path.copy()
        
        for i in range(n_points):
            # Waktu untuk mencapai titik ini (asumsi kecepatan konstan)
            t = i / n_points  # normalized time
            
            # Rotasi karena cosmic spin
            rotation_angle = self.Ω_cosmic * t
            
            # Apply rotation
            R = np.array([
                [np.cos(rotation_angle), -np.sin(rotation_angle), 0],
                [np.sin(rotation_angle), np.cos(rotation_angle), 0],
                [0, 0, 1]
            ])
            
            # Rotasikan titik (dalam basis TP-OCM)
            optimized_path[i] = R @ path[i]
        
        return optimized_path
    
    def _calculate_navigation_cost(self, path: np.ndarray, method: str) -> float:
        """
        Hitung biaya navigasi berdasarkan Paper 07:
        - Euclidean: High cost (melawan gradien fase)
        - Phase surfing: Low cost (mengikuti gradien fase)
        """
        n_points = len(path)
        
        if method == 'euclidean':
            # Cost tinggi untuk perubahan fase cepat
            phase_changes = 0
            for i in range(1, n_points):
                # Hitung perubahan fase antara titik
                phase_i = self._calculate_phase_at_point(path[i])
                phase_prev = self._calculate_phase_at_point(path[i-1])
                phase_changes += abs(phase_i - phase_prev)
            
            return 1.0 + 0.5 * phase_changes / n_points
            
        else:  # phase_surfing
            # Cost rendah untuk perubahan fase halus
            phase_changes = 0
            for i in range(1, n_points):
                phase_i = self._calculate_phase_at_point(path[i])
                phase_prev = self._calculate_phase_at_point(path[i-1])
                phase_changes += abs(phase_i - phase_prev)
            
            return 0.1 + 0.05 * phase_changes / n_points
    
    def _calculate_phase_at_point(self, point: np.ndarray) -> float:
        """Hitung fase TP-OCM di suatu titik"""
        x, y, z = point
        Z1 = x + 1j * y
        Z2 = z + 1j * y
        Z3 = x + 1j * z
        
        prod = Z1 * Z2 * Z3
        return np.angle(prod)
    
    def _analyze_zones_along_path(self, path: np.ndarray) -> Dict:
        """Analisis zona sepanjang path"""
        n_points = len(path)
        zones = {'LAMINAR': 0, 'TURBULENT': 0, 'SINGULAR': 0}
        
        for point in path:
            zone = self.determine_zone(point)
            zones[zone] += 1
        
        # Konversi ke persentase
        total = sum(zones.values())
        percentages = {k: v/total*100 for k, v in zones.items()}
        
        return {
            'counts': zones,
            'percentages': percentages,
            'dominant_zone': max(zones, key=zones.get),
            'path_safety': 'SAFE' if zones['SINGULAR'] == 0 else 'DANGEROUS'
        }
    
    def _calculate_tpocm_distance(self, path: np.ndarray) -> float:
        """
        Hitung jarak TP-OCM sepanjang path (bukan Euclidean)
        Menggunakan metrik dari Paper 02 dengan torsi intrinsik
        """
        distance = 0.0
        n_points = len(path)
        
        for i in range(1, n_points):
            p1 = path[i-1]
            p2 = path[i]
            
            # Koordinat polar
            r1 = np.linalg.norm(p1)
            r2 = np.linalg.norm(p2)
            
            # Sudut-sudut
            θ1_1 = np.arctan2(p1[1], p1[0])
            θ2_1 = np.arctan2(p1[1], p1[2])
            θ3_1 = np.arctan2(p1[2], p1[0])
            
            θ1_2 = np.arctan2(p2[1], p2[0])
            θ2_2 = np.arctan2(p2[1], p2[2])
            θ3_2 = np.arctan2(p2[2], p2[0])
            
            # Elemen garis ds² dari Paper 02
            dr = r2 - r1
            dθ1 = θ1_2 - θ1_1
            dθ2 = θ2_2 - θ2_1
            dθ3 = θ3_2 - θ3_1
            
            # Rata-rata r untuk diskritisasi
            r_avg = (r1 + r2) / 2
            
            # ds² = dr² + r²(dθ1² + dθ2² + dθ3²) + 2r²(sinθ1 dθ3 - sinθ3 dθ1)
            ds2 = (dr**2 + 
                  r_avg**2 * (dθ1**2 + dθ2**2 + dθ3**2) +
                  2 * r_avg**2 * (np.sin(θ1_1)*dθ3 - np.sin(θ3_1)*dθ1))
            
            distance += np.sqrt(abs(ds2))
        
        return distance
    
    # ===== 5. NAVIGASI RELATIVISTIK =====
    def predict_dynamic_target(self, target_position: np.ndarray, 
                              time_to_impact: float) -> np.ndarray:
        """
        Prediksi posisi target setelah rotasi kosmik Ω
        Sesuai Paper 07 Section 5.1: "Bidik ke B', bukan B"
        """
        # Rotasi target karena cosmic spin
        rotation_angle = self.Ω_cosmic * time_to_impact
        
        R = np.array([
            [np.cos(rotation_angle), -np.sin(rotation_angle), 0],
            [np.sin(rotation_angle), np.cos(rotation_angle), 0],
            [0, 0, 1]
        ])
        
        target_rotated = R @ target_position
        
        # Juga koreksi untuk proyeksi ke manifold
        target_projected, _ = self.project_to_manifold(target_rotated)
        
        return target_projected
    
    # ===== VISUALIZATION =====
    def visualize_navigation(self, start: np.ndarray, end: np.ndarray):
        """Visualisasi perbandingan navigasi Euclidean vs TP-OCM"""
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        
        # Hitung kedua path
        result_euclidean = self.find_geodesic_path(start, end, method='euclidean')
        result_tpocm = self.find_geodesic_path(start, end, method='phase_surfing')
        
        path_euc = result_euclidean['path']
        path_tpocm = result_tpocm['path']
        
        # Plot 3D
        fig = plt.figure(figsize=(15, 10))
        
        # Plot 3D
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        ax1.plot(path_euc[:, 0], path_euc[:, 1], path_euc[:, 2], 
                'r-', label='Euclidean', linewidth=2)
        ax1.plot(path_tpocm[:, 0], path_tpocm[:, 1], path_tpocm[:, 2],
                'b--', label='TP-OCM Phase Surfing', linewidth=2)
        ax1.scatter([start[0], end[0]], [start[1], end[1]], [start[2], end[2]],
                   c=['green', 'orange'], s=100, marker='o')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')
        ax1.set_title('3D Navigation Paths')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2D projections
        ax2 = fig.add_subplot(2, 3, 2)
        ax2.plot(path_euc[:, 0], path_euc[:, 1], 'r-', label='Euclidean')
        ax2.plot(path_tpocm[:, 0], path_tpocm[:, 1], 'b--', label='TP-OCM')
        ax2.scatter([start[0], end[0]], [start[1], end[1]], 
                   c=['green', 'orange'], s=100)
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_title('XY Projection')
        ax2.legend()
        ax2.grid(True)
        ax2.axis('equal')
        
        ax3 = fig.add_subplot(2, 3, 3)
        ax3.plot(path_euc[:, 0], path_euc[:, 2], 'r-', label='Euclidean')
        ax3.plot(path_tpocm[:, 0], path_tpocm[:, 2], 'b--', label='TP-OCM')
        ax3.scatter([start[0], end[0]], [start[2], end[2]], 
                   c=['green', 'orange'], s=100)
        ax3.set_xlabel('X')
        ax3.set_ylabel('Z')
        ax3.set_title('XZ Projection')
        ax3.legend()
        ax3.grid(True)
        ax3.axis('equal')
        
        # Plot phase along path
        ax4 = fig.add_subplot(2, 3, 4)
        phase_euc = [self._calculate_phase_at_point(p) for p in path_euc]
        phase_tpocm = [self._calculate_phase_at_point(p) for p in path_tpocm]
        
        ax4.plot(np.linspace(0, 1, len(phase_euc)), phase_euc, 'r-', 
                label='Euclidean Phase')
        ax4.plot(np.linspace(0, 1, len(phase_tpocm)), phase_tpocm, 'b--',
                label='TP-OCM Phase')
        ax4.set_xlabel('Path Progress')
        ax4.set_ylabel('Phase (rad)')
        ax4.set_title('Phase Evolution Along Path')
        ax4.legend()
        ax4.grid(True)
        
        # Bar chart comparison
        ax5 = fig.add_subplot(2, 3, 5)
        metrics = ['Navigation Cost', 'Distance', 'Phase Change']
        euc_values = [
            result_euclidean['navigation_cost'],
            result_euclidean['distance_tpocm'],
            np.sum(np.abs(np.diff(phase_euc)))
        ]
        tpocm_values = [
            result_tpocm['navigation_cost'],
            result_tpocm['distance_tpocm'],
            np.sum(np.abs(np.diff(phase_tpocm)))
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        ax5.bar(x - width/2, euc_values, width, label='Euclidean', color='red')
        ax5.bar(x + width/2, tpocm_values, width, label='TP-OCM', color='blue')
        ax5.set_xlabel('Metric')
        ax5.set_ylabel('Value')
        ax5.set_title('Performance Comparison')
        ax5.set_xticks(x)
        ax5.set_xticklabels(metrics)
        ax5.legend()
        ax5.grid(True, axis='y')
        
        # Zone analysis
        ax6 = fig.add_subplot(2, 3, 6)
        zones = list(result_tpocm['zone_analysis']['percentages'].keys())
        percentages = list(result_tpocm['zone_analysis']['percentages'].values())
        
        colors = ['green', 'yellow', 'red']
        bars = ax6.bar(zones, percentages, color=colors)
        ax6.set_xlabel('Zone')
        ax6.set_ylabel('Percentage (%)')
        ax6.set_title('Zone Distribution Along TP-OCM Path')
        ax6.grid(True, axis='y')
        
        # Add percentage labels
        for bar, percentage in zip(bars, percentages):
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                    f'{percentage:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.show()
        
        # Print summary
        print("="*80)
        print("NAVIGATION SUMMARY")
        print("="*80)
        print(f"\nStart: {start}")
        print(f"End: {end}")
        print(f"\nEuclidean Navigation:")
        print(f"  • Cost: {result_euclidean['navigation_cost']:.3f}")
        print(f"  • TP-OCM Distance: {result_euclidean['distance_tpocm']:.3f}")
        print(f"  • Euclidean Distance: {result_euclidean['distance_euclidean']:.3f}")
        print(f"  • Start Zone: {result_euclidean['start_zone']}")
        print(f"  • End Zone: {result_euclidean['end_zone']}")
        
        print(f"\nTP-OCM Phase Surfing Navigation:")
        print(f"  • Cost: {result_tpocm['navigation_cost']:.3f}")
        print(f"  • TP-OCM Distance: {result_tpocm['distance_tpocm']:.3f}")
        print(f"  • Euclidean Distance: {result_tpocm['distance_euclidean']:.3f}")
        print(f"  • Start Zone: {result_tpocm['start_zone']}")
        print(f"  • End Zone: {result_tpocm['end_zone']}")
        print(f"  • Path Safety: {result_tpocm['zone_analysis']['path_safety']}")
        
        print(f"\nEfficiency Improvement:")
        cost_improvement = ((result_euclidean['navigation_cost'] - 
                           result_tpocm['navigation_cost']) / 
                          result_euclidean['navigation_cost'] * 100)
        print(f"  • Cost Reduction: {cost_improvement:.1f}%")
        
        if cost_improvement > 0:
            print(f"  → TP-OCM Navigation is MORE EFFICIENT!")
        else:
            print(f"  → Euclidean Navigation is more efficient (unexpected!)")
        
        return result_euclidean, result_tpocm

# ===== DEMO DAN CONTOH PENGGUNAAN =====
def demo_tpocm_navigation():
    """Demonstrasi sistem navigasi TP-OCM"""
    
    print("="*80)
    print("DEMONSTRASI SISTEM NAVIGASI TP-OCM (PAPER 07)")
    print("="*80)
    
    # Inisialisasi sistem
    nav_system = TPOCM_Navigation_System()
    
    # Contoh 1: Navigasi normal
    print("\n1. CONTOH 1: Navigasi antara dua titik")
    start1 = np.array([1.0, 2.0, 3.0])
    end1 = np.array([4.0, 5.0, 6.0])
    
    result_euc1, result_tpocm1 = nav_system.visualize_navigation(start1, end1)
    
    # Contoh 2: Navigasi melalui zona turbulen
    print("\n\n2. CONTOH 2: Navigasi melalui zona turbulen")
    # Pilih titik dekat singularitas (z ≈ 0) untuk zona turbulen
    start2 = np.array([2.0, 3.0, 0.01])  # Hampir singular di z
    end2 = np.array([5.0, 6.0, 0.01])
    
    try:
        result_euc2, result_tpocm2 = nav_system.visualize_navigation(start2, end2)
    except ValueError as e:
        print(f"Navigation failed: {e}")
        print("This demonstrates the safety features of TP-OCM navigation!")
    
    # Contoh 3: Dynamic targeting
    print("\n\n3. CONTOH 3: Dynamic Targeting (Bidik ke B', bukan B)")
    target = np.array([10.0, 0.0, 0.0])
    time_to_impact = 5.0  # seconds
    
    predicted_target = nav_system.predict_dynamic_target(target, time_to_impact)
    print(f"Original target: {target}")
    print(f"Predicted target (after {time_to_impact}s cosmic rotation): {predicted_target}")
    
    angular_displacement = np.arccos(
        np.dot(target, predicted_target) / 
        (np.linalg.norm(target) * np.linalg.norm(predicted_target))
    )
    print(f"Angular displacement: {np.degrees(angular_displacement):.2f}°")
    
    # Contoh 4: Zona analysis
    print("\n\n4. CONTOH 4: Analisis Zona untuk berbagai titik")
    test_points = [
        np.array([1.0, 1.0, 1.0]),  # Laminar
        np.array([0.1, 1.0, 0.001]),  # Near singular
        np.array([0.5, 2.0, 0.1]),   # Turbulent
        np.array([0.0, 1.0, 0.0]),   # Singular
    ]
    
    for i, point in enumerate(test_points):
        zone = nav_system.determine_zone(point)
        props = nav_system.get_zone_properties(zone)
        print(f"\nPoint {i+1}: {point}")
        print(f"  Zone: {zone}")
        print(f"  Description: {props.get('description', 'Unknown')}")
        print(f"  Examples: {', '.join(props.get('examples', []))}")
    
    # Contoh 5: Performance benchmark
    print("\n\n5. CONTOH 5: Performance Benchmark")
    import time
    
    # Benchmark Euclidean
    start_time = time.time()
    for _ in range(100):
        nav_system.find_geodesic_path(start1, end1, method='euclidean', n_points=20)
    euc_time = time.time() - start_time
    
    # Benchmark TP-OCM
    start_time = time.time()
    for _ in range(100):
        nav_system.find_geodesic_path(start1, end1, method='phase_surfing', n_points=20)
    tpocm_time = time.time() - start_time
    
    print(f"Euclidean path computation (100x): {euc_time:.3f}s")
    print(f"TP-OCM path computation (100x): {tpocm_time:.3f}s")
    print(f"TP-OCM overhead: {(tpocm_time/euc_time - 1)*100:.1f}%")
    
    print("\n" + "="*80)
    print("KESIMPULAN DEMO:")
    print("="*80)
    print("TP-OCM Navigation System memberikan:")
    print("1. Path optimization dengan phase surfing")
    print("2. Safety analysis dengan zona topologi")
    print("3. Dynamic targeting dengan cosmic rotation")
    print("4. Energy-efficient navigation")
    print("\nSiap untuk Fase II: Aplikasi ke Fisika Nuklir, Partikel, dan Kimia!")

if __name__ == "__main__":
    # Jalankan demo
    demo_tpocm_navigation()