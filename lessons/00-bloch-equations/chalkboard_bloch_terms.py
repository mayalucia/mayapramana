"""
Chalkboard illustration: the three terms of the Bloch equations.

Three panels, one per term:
  1. Precession: γ M × B — rotation around B
  2. T2 decay: -M_perp / T2 — transverse components shrink
  3. T1 recovery: -(Mz - M0) / T1 — longitudinal component approaches M0

Each panel shows a Bloch sphere with the relevant motion indicated
by arrows on the vector M.

Usage:
    python chalkboard_bloch_terms.py
"""

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', 'python'))

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk


board = Chalkboard(panels=3, figsize=(21, 10),
                   grid_panels=set(), panel_weights=[1, 1, 1])


def draw_bloch_sphere(ax, title):
    """Draw a unit Bloch sphere outline on the given axes."""
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')

    # Great circle (equator)
    phi = np.linspace(0, 2 * np.pi, 200)
    # Oblique projection: show equator as an ellipse
    ax.plot(np.cos(phi), 0.3 * np.sin(phi),
            color=chalk.DIM, linewidth=0.5, linestyle=':', alpha=0.4)

    # Meridian (front half)
    ax.plot(0.3 * np.sin(phi), np.cos(phi),
            color=chalk.DIM, linewidth=0.5, linestyle=':', alpha=0.3)

    # Outer circle (sphere boundary)
    ax.plot(np.cos(phi), np.sin(phi),
            color=chalk.DIM, linewidth=0.6, alpha=0.5)

    # Coordinate axes
    chalk.chalk_arrow(ax, 0, -1.3, 0, 1.3, color=chalk.DIM, lw=0.6, head=8)
    chalk.chalk_arrow(ax, -1.3, 0, 1.3, 0, color=chalk.DIM, lw=0.6, head=8)

    # Labels
    chalk.chalk_text(ax, 0.07, 1.25, '$z$', color=chalk.DIM,
                     fontsize=9, style='normal')
    chalk.chalk_text(ax, 1.2, -0.15, '$x$', color=chalk.DIM,
                     fontsize=9, style='normal')


# ============================================================
# Panel 1: Precession — γ M × B
# ============================================================

ax1 = board.panel(0, title=r'$\gamma\,\mathbf{M} \times \mathbf{B}$')
draw_bloch_sphere(ax1, 'precession')

# B field along z
chalk.chalk_arrow(ax1, 0, 1.0, 0, 1.45, color=chalk.YELLOW, lw=2.0, head=14)
chalk.chalk_text(ax1, 0.1, 1.38, r'$\mathbf{B}$', color=chalk.YELLOW,
                 fontsize=12, style='normal')

# M vector at ~45° from z, in the xz plane
theta_m = np.radians(50)
mx = np.sin(theta_m)
mz = np.cos(theta_m)
chalk.chalk_arrow(ax1, 0, 0, mx, mz, color=chalk.RED, lw=2.5, head=14)
chalk.chalk_text(ax1, mx + 0.08, mz + 0.05, r'$\mathbf{M}$',
                 color=chalk.RED, fontsize=12, style='normal')

# Show the precession orbit (circle in the xy-plane at height mz)
# In projection: an ellipse
orbit_phi = np.linspace(0, 2 * np.pi, 200)
orbit_r = np.sin(theta_m)
orbit_x = orbit_r * np.cos(orbit_phi)
orbit_z = mz + orbit_r * 0.3 * np.sin(orbit_phi)  # oblique projection

# Back half dashed
back_mask = np.sin(orbit_phi) > 0
front_mask = ~back_mask

# Segment into contiguous runs
def plot_masked(ax, x, z, mask, **kwargs):
    """Plot contiguous runs where mask is True."""
    segs = np.diff(mask.astype(int))
    starts = np.where(segs == 1)[0] + 1
    ends = np.where(segs == -1)[0] + 1
    if mask[0]:
        starts = np.concatenate([[0], starts])
    if mask[-1]:
        ends = np.concatenate([ends, [len(mask)]])
    for s, e in zip(starts, ends):
        ax.plot(x[s:e], z[s:e], **kwargs)

plot_masked(ax1, orbit_x, orbit_z, back_mask,
            color=chalk.DIM, linewidth=0.6, linestyle='--', alpha=0.4)
plot_masked(ax1, orbit_x, orbit_z, front_mask,
            color=chalk.WHITE, linewidth=1.0, alpha=0.7)

# Circular arrow showing rotation direction
arc_phi = np.linspace(0, 1.5, 40)
arc_r = orbit_r * 0.85
arc_x = arc_r * np.cos(arc_phi)
arc_z = mz + arc_r * 0.3 * np.sin(arc_phi)
ax1.plot(arc_x, arc_z, color=chalk.BLUE, linewidth=1.2, zorder=3)
chalk.chalk_arrow(ax1, arc_x[-2], arc_z[-2], arc_x[-1], arc_z[-1],
                  color=chalk.BLUE, lw=1.0, head=10)

# Caption
chalk.chalk_text(ax1, -1.4, -1.45, 'rotation',
                 color=chalk.WHITE, fontsize=10)
chalk.chalk_text(ax1, -1.4, -1.55, r'$|\mathbf{M}|$ preserved',
                 color=chalk.DIM, fontsize=8, style='normal')


# ============================================================
# Panel 2: T2 decay — transverse components shrink
# ============================================================

ax2 = board.panel(1, title=r'$-M_x/T_2,\; -M_y/T_2$')
draw_bloch_sphere(ax2, 'T2 decay')

# M vector with transverse component
theta_m2 = np.radians(60)
mx2 = np.sin(theta_m2)
mz2 = np.cos(theta_m2)
chalk.chalk_arrow(ax2, 0, 0, mx2, mz2, color=chalk.RED, lw=2.5, head=14)
chalk.chalk_text(ax2, mx2 + 0.08, mz2 + 0.05, r'$\mathbf{M}$',
                 color=chalk.RED, fontsize=12, style='normal')

# Show the transverse component being pulled toward z-axis
# Arrow from M tip pointing inward (toward the z-axis)
shrink_dx = -0.35 * np.sin(theta_m2)
shrink_dz = 0  # only transverse shrinks, Mz stays
chalk.chalk_arrow(ax2, mx2, mz2, mx2 + shrink_dx, mz2 + shrink_dz,
                  color=chalk.BLUE, lw=2.0, head=12)

# Dashed line showing the transverse component
chalk.chalk_line(ax2, [0, mx2], [mz2, mz2], color=chalk.DIM, lw=0.6,
                 linestyle='--', alpha=0.5)
chalk.chalk_line(ax2, [mx2, mx2], [0, mz2], color=chalk.DIM, lw=0.6,
                 linestyle='--', alpha=0.5)

# Ghost: where M ends up after T2 decay
# Just the Mz component remains
chalk.chalk_arrow(ax2, 0, 0, 0, mz2, color=chalk.DIM, lw=1.5, head=10)
chalk.chalk_text(ax2, -0.35, mz2 / 2, '$M_z$', color=chalk.DIM,
                 fontsize=9, style='normal')

# Label the transverse component
chalk.chalk_text(ax2, mx2 / 2 - 0.05, mz2 + 0.1, '$M_\\perp$',
                 color=chalk.RED, fontsize=9, style='normal')

# Caption
chalk.chalk_text(ax2, -1.4, -1.45, 'dephasing',
                 color=chalk.WHITE, fontsize=10)
chalk.chalk_text(ax2, -1.4, -1.55, r'$|\mathbf{M}|$ shrinks',
                 color=chalk.DIM, fontsize=8, style='normal')


# ============================================================
# Panel 3: T1 recovery — Mz approaches M0
# ============================================================

ax3 = board.panel(2, title=r'$-(M_z - M_0)/T_1$')
draw_bloch_sphere(ax3, 'T1 recovery')

# Current M: small, near centre (depleted state)
mz_current = 0.15
chalk.chalk_arrow(ax3, 0, 0, 0, mz_current, color=chalk.RED, lw=2.5, head=14)
chalk.chalk_text(ax3, 0.1, mz_current - 0.05, r'$\mathbf{M}$',
                 color=chalk.RED, fontsize=12, style='normal')

# Target: M0 on the z-axis (north pole region)
m0_z = 0.85
chalk.chalk_arrow(ax3, 0, mz_current, 0, m0_z,
                  color=chalk.BLUE, lw=2.0, head=12)

# M0 marker
ax3.plot(0, m0_z, 'o', color=chalk.YELLOW, markersize=6, zorder=3)
chalk.chalk_text(ax3, 0.12, m0_z, '$M_0$', color=chalk.YELLOW,
                 fontsize=11, style='normal')

# Ghost trajectory: several intermediate positions
for frac in [0.3, 0.5, 0.7]:
    gz = mz_current + frac * (m0_z - mz_current)
    ax3.plot(0, gz, 'o', color=chalk.DIM, markersize=3,
             alpha=0.4, zorder=2)

# Caption
chalk.chalk_text(ax3, -1.4, -1.45, 'thermalisation',
                 color=chalk.WHITE, fontsize=10)
chalk.chalk_text(ax3, -1.4, -1.55, r'$M_z \to M_0$',
                 color=chalk.DIM, fontsize=8, style='normal')


# --- Save ---
out = os.path.join(_here, 'chalkboard_bloch_terms.png')
board.save(out)
board.close()
print(f"Saved {out}")
