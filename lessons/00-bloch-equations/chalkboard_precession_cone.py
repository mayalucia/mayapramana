"""
Chalkboard illustration: Larmor precession — a spin tracing a cone around B.

The magnetic moment M precesses around the static field B (along z),
tracing a cone. The cone angle is the tip angle theta. This is the
gyroscope picture, drawn on a chalkboard.

Usage:
    python chalkboard_precession_cone.py
"""

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', 'python'))

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk


# --- Single-panel board ---
board = Chalkboard(panels=1, figsize=(8, 7), grid_panels=set())
ax = board.panel(0, title='Larmor precession')

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.2, 1.8)
ax.set_aspect('equal')
ax.axis('off')

# --- Draw the B field arrow (vertical, along z) ---
chalk.chalk_arrow(ax, 0, -0.8, 0, 1.6, color=chalk.YELLOW, lw=2.5, head=18)
chalk.chalk_text(ax, 0.08, 1.55, r'$\mathbf{B}$',
                 color=chalk.YELLOW, fontsize=16, style='normal')

# --- The precession cone ---
# Cone parameters
theta = np.radians(40)   # half-angle of the cone
M_len = 1.2              # length of M vector

# The spin vector M at a particular azimuthal angle phi
phi_snapshot = np.radians(30)  # frozen instant

# Tip of M in 3D (projected to 2D: x horizontal, z vertical)
# We use a simple oblique projection
def project(x3, y3, z3, oblique=0.35):
    """Project 3D (x, y, z) onto 2D chalkboard (horizontal, vertical).

    z -> vertical, x -> horizontal, y foreshortened diagonally.
    """
    px = x3 - oblique * y3 * 0.5
    pz = z3 + oblique * y3 * 0.3
    return px, pz

# Draw the cone surface as an ellipse at the base
# The cone's circular cross-section at height M_len * cos(theta)
cone_z = M_len * np.cos(theta)
cone_r = M_len * np.sin(theta)

# Draw the circular orbit (ellipse in projection)
phi_vals = np.linspace(0, 2 * np.pi, 200)
orbit_x = []
orbit_z = []
for phi in phi_vals:
    x3 = cone_r * np.cos(phi)
    y3 = cone_r * np.sin(phi)
    px, pz = project(x3, y3, cone_z)
    orbit_x.append(px)
    orbit_z.append(pz)

# Draw back half of orbit (dashed, behind)
back_x, back_z = [], []
front_x, front_z = [], []
for i, phi in enumerate(phi_vals):
    if np.sin(phi) > 0:  # "behind" the board
        back_x.append(orbit_x[i])
        back_z.append(orbit_z[i])
    else:
        front_x.append(orbit_x[i])
        front_z.append(orbit_z[i])

if back_x:
    ax.plot(back_x, back_z, color=chalk.DIM, linewidth=0.8,
            linestyle='--', alpha=0.5, zorder=1)
if front_x:
    ax.plot(front_x, front_z, color=chalk.WHITE, linewidth=1.2, zorder=2)

# Draw the cone edges (two lines from origin to the orbit extremes)
# Left and right extremes of the projected ellipse
left_x3 = cone_r * np.cos(np.pi)
left_y3 = cone_r * np.sin(np.pi)
lx, lz = project(left_x3, left_y3, cone_z)
chalk.chalk_line(ax, [0, lx], [0, lz], color=chalk.DIM, lw=0.6,
                 linestyle=':', alpha=0.5)

right_x3 = cone_r * np.cos(0)
right_y3 = cone_r * np.sin(0)
rx, rz = project(right_x3, right_y3, cone_z)
chalk.chalk_line(ax, [0, rx], [0, rz], color=chalk.DIM, lw=0.6,
                 linestyle=':', alpha=0.5)

# --- The spin vector M (frozen at phi_snapshot) ---
mx3 = cone_r * np.cos(phi_snapshot)
my3 = cone_r * np.sin(phi_snapshot)
mz3 = cone_z
tip_x, tip_z = project(mx3, my3, mz3)

chalk.chalk_arrow(ax, 0, 0, tip_x, tip_z,
                  color=chalk.RED, lw=2.5, head=16)
chalk.chalk_text(ax, tip_x + 0.08, tip_z + 0.05, r'$\mathbf{M}$',
                 color=chalk.RED, fontsize=14, style='normal')

# --- Precession direction arrow (curved arc near tip of M) ---
# Arc slightly outside the orbit to show rotation direction
arc_scale = 1.08  # just outside the orbit
arc_phi = np.linspace(phi_snapshot + 0.15, phi_snapshot + 1.2, 50)
arc_xs, arc_zs = [], []
for p in arc_phi:
    x3 = cone_r * arc_scale * np.cos(p)
    y3 = cone_r * arc_scale * np.sin(p)
    px, pz = project(x3, y3, cone_z)
    arc_xs.append(px)
    arc_zs.append(pz)

ax.plot(arc_xs, arc_zs, color=chalk.BLUE, linewidth=1.2, alpha=0.9, zorder=3)
chalk.chalk_arrow(ax, arc_xs[-2], arc_zs[-2], arc_xs[-1], arc_zs[-1],
                  color=chalk.BLUE, lw=1.0, head=12)

chalk.chalk_text(ax, arc_xs[-1] - 0.22, arc_zs[-1] + 0.1,
                 r'$\omega_L$', color=chalk.BLUE, fontsize=12, style='normal')

# --- Angle annotation (theta) ---
# Draw a small arc near the z-axis showing the cone half-angle
angle_r = 0.4
angle_phi = np.linspace(0, theta, 30)
angle_xs = [angle_r * np.sin(a) for a in angle_phi]
angle_zs = [angle_r * np.cos(a) for a in angle_phi]
ax.plot(angle_xs, angle_zs, color=chalk.DIM, linewidth=0.8)
chalk.chalk_text(ax, 0.22, 0.35, r'$\theta$',
                 color=chalk.DIM, fontsize=11, style='normal')

# --- z-axis label ---
chalk.chalk_text(ax, -0.18, -0.85, r'$\hat{z}$',
                 color=chalk.DIM, fontsize=11, style='normal')

# --- Caption at the bottom ---
chalk.chalk_text(ax, -1.4, -1.05,
                 r'$d\mathbf{M}/dt = \gamma\,\mathbf{M} \times \mathbf{B}$'
                 '      precession, no relaxation',
                 color=chalk.WHITE, fontsize=11, style='normal')

# --- Save ---
out = os.path.join(_here, 'chalkboard_precession_cone.png')
board.save(out)
board.close()
print(f"Saved {out}")
