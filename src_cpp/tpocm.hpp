#ifndef TPOCM_HPP
#define TPOCM_HPP

#include <cmath>
#include <iostream>

namespace tpocm {

    struct Point3D {
        double x1; // Timur-Barat
        double x2; // Utara-Selatan
        double y;  // Atas-Bawah
    };

    class Engine {
    private:
        Point3D current_pos;

    public:
        Engine(double x1, double x2, double y) : current_pos{x1, x2, y} {}

        // Getters untuk "Three Papers"
        Point3D get_position() const { return current_pos; }
        
        double get_r() const {
            return std::sqrt(current_pos.x1*current_pos.x1 + 
                             current_pos.x2*current_pos.x2 + 
                             current_pos.y*current_pos.y);
        }

        // Canonical Angles
        double get_yaw() const { return std::atan2(current_pos.x2, current_pos.x1); }
        double get_pitch() const { return std::atan2(current_pos.y, current_pos.x2); }
        double get_roll() const { return std::atan2(current_pos.y, current_pos.x1); }

        // High-Speed Rotation (Optimized Matrix Multiplication)
        void rotate(double d_yaw, double d_pitch, double d_roll) {
            double c, s;
            double nx1, nx2, ny;

            // 1. YAW (Horizontal Plane Rotation)
            if (std::abs(d_yaw) > 1e-9) {
                c = std::cos(d_yaw); s = std::sin(d_yaw);
                nx1 = current_pos.x1 * c - current_pos.x2 * s;
                nx2 = current_pos.x1 * s + current_pos.x2 * c;
                current_pos.x1 = nx1;
                current_pos.x2 = nx2;
            }

            // 2. PITCH (Sagital Plane Rotation)
            if (std::abs(d_pitch) > 1e-9) {
                c = std::cos(d_pitch); s = std::sin(d_pitch);
                ny = current_pos.y * c - current_pos.x2 * s;
                nx2 = current_pos.y * s + current_pos.x2 * c; // Update x2
                current_pos.y = ny;
                current_pos.x2 = nx2;
            }

            // 3. ROLL (Frontal Plane Rotation)
            if (std::abs(d_roll) > 1e-9) {
                c = std::cos(d_roll); s = std::sin(d_roll);
                nx1 = current_pos.x1 * c - current_pos.y * s;
                ny = current_pos.x1 * s + current_pos.y * c; // Update y
                current_pos.x1 = nx1;
                current_pos.y = ny;
            }
        }
    };
}

#endif // TPOCM_HPP