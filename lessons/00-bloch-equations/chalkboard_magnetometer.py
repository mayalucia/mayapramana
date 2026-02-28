"""
Chalkboard illustration: the three steps of an atomic magnetometer.

Three panels:
  1. PUMP — circularly polarised laser creates spin polarisation (M along z)
  2. PRECESS — spins precess around B at ω_L (transverse oscillation)
  3. READ — probe beam measures M_x via Faraday rotation → signal

Each panel shows the Bloch vector state and the relevant optical element.

Usage:
    python chalkboard_magnetometer.py
"""

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', 'python'))

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk


board = Chalkboard(panels=3, figsize=(21, 10),
                   grid_panels=set(), panel_weights=[1, 1, 1])


# ============================================================
# Common: draw a simplified cell + Bloch vector in each panel
# ============================================================

def draw_cell(ax, label=None):
    """Draw the vapour cell outline."""
    chalk.chalk_box(ax, 1.5, 2.0, 4.0, 3.5, lw=1.2, pad=0.1)
    if label:
        chalk.chalk_text(ax, 3.5, 5.7, label, color=chalk.DIM,
                         fontsize=9, ha='center')


def draw_B_field(ax):
    """Draw the B field arrow (along x, horizontal)."""
    chalk.chalk_arrow(ax, 6.0, 3.75, 7.5, 3.75,
                      color=chalk.YELLOW, lw=2.0, head=14)
    chalk.chalk_text(ax, 6.8, 4.15, r'$\mathbf{B}$',
                     color=chalk.YELLOW, fontsize=13, style='normal',
                     ha='center')


def draw_bloch_inset(ax, mx, my, mz, x0=2.5, y0=0.2, size=1.5):
    """Draw a small Bloch sphere inset with M vector.

    The inset is placed at (x0, y0) in data coordinates, with given size.
    mz maps to vertical, mx to horizontal (side view).
    """
    cx, cy = x0 + size / 2, y0 + size / 2

    # Circle
    phi = np.linspace(0, 2 * np.pi, 100)
    r = size * 0.45
    ax.plot(cx + r * np.cos(phi), cy + r * np.sin(phi),
            color=chalk.DIM, linewidth=0.5, alpha=0.4)

    # Equator ellipse
    ax.plot(cx + r * np.cos(phi), cy + 0.25 * r * np.sin(phi),
            color=chalk.DIM, linewidth=0.4, linestyle=':', alpha=0.3)

    # Axes
    chalk.chalk_line(ax, [cx, cx], [cy - r * 1.1, cy + r * 1.1],
                     color=chalk.DIM, lw=0.4, alpha=0.3)
    chalk.chalk_line(ax, [cx - r * 1.1, cx + r * 1.1], [cy, cy],
                     color=chalk.DIM, lw=0.4, alpha=0.3)

    # M vector (normalise to fit in sphere)
    m_norm = np.sqrt(mx**2 + mz**2) or 1.0
    scale = r * 0.85
    tip_x = cx + mx / m_norm * scale
    tip_y = cy + mz / m_norm * scale

    chalk.chalk_arrow(ax, cx, cy, tip_x, tip_y,
                      color=chalk.RED, lw=2.0, head=10)

    return cx, cy


# ============================================================
# Panel 1: PUMP
# ============================================================

ax1 = board.panel(0, title='1.  pump')
ax1.set_xlim(-0.5, 8.5)
ax1.set_ylim(-0.5, 7.5)
ax1.set_aspect('equal')
ax1.axis('off')

draw_cell(ax1, 'Rb cell')
draw_B_field(ax1)

# Pump laser from the left
chalk.chalk_arrow(ax1, -0.3, 3.75, 1.5, 3.75,
                  color=chalk.RED, lw=3.0, head=18)
chalk.chalk_text(ax1, 0.0, 4.5, 'pump', color=chalk.RED, fontsize=11)
chalk.chalk_text(ax1, 0.0, 4.1, 'laser', color=chalk.RED, fontsize=11)

# Circular polarisation symbol
chalk.chalk_circle(ax1, 0.7, 3.75, 0.2, color=chalk.RED)
chalk.chalk_arrow(ax1, 0.82, 3.6, 0.9, 3.85,
                  color=chalk.RED, lw=0.7, head=7)

# Spin arrows inside cell: mostly aligned along z (pumped)
np.random.seed(42)
for _ in range(10):
    sx = 1.8 + np.random.random() * 3.4
    sy = 2.3 + np.random.random() * 2.8
    # Mostly pointing up (along B direction = to the right here)
    # In the magnetometer, pump creates Mz along propagation = left-right
    # But conceptually: pump creates polarisation along pump direction
    angle = np.random.uniform(-0.3, 0.3)  # nearly aligned
    dx = 0.25 * np.cos(angle)
    dy = 0.25 * np.sin(angle)
    chalk.chalk_arrow(ax1, sx, sy, sx + dx, sy + dy,
                      color=chalk.YELLOW, lw=0.8, head=6)

# Bloch vector inset: M along z (fully pumped)
draw_bloch_inset(ax1, mx=0, my=0, mz=1, x0=5.5, y0=0.0)
chalk.chalk_text(ax1, 6.4, 0.0, r'$M_z = M_0$',
                 color=chalk.RED, fontsize=9, style='normal')

# Annotation
chalk.chalk_text(ax1, 0.5, 0.5, 'create polarisation',
                 color=chalk.WHITE, fontsize=10)


# ============================================================
# Panel 2: PRECESS
# ============================================================

ax2 = board.panel(1, title='2.  precess')
ax2.set_xlim(-0.5, 8.5)
ax2.set_ylim(-0.5, 7.5)
ax2.set_aspect('equal')
ax2.axis('off')

draw_cell(ax2, 'Rb cell')
draw_B_field(ax2)

# No laser — dark period or pump off
chalk.chalk_text(ax2, 0.2, 4.0, 'pump', color=chalk.DIM, fontsize=10)
chalk.chalk_text(ax2, 0.2, 3.6, 'off', color=chalk.DIM, fontsize=10)

# Spin arrows inside cell: precessing (various phases)
np.random.seed(77)
for _ in range(10):
    sx = 1.8 + np.random.random() * 3.4
    sy = 2.3 + np.random.random() * 2.8
    # Random precession angles — spins are precessing coherently
    # but at different spatial positions
    angle = np.random.uniform(0, 2 * np.pi)
    dx = 0.2 * np.cos(angle)
    dy = 0.2 * np.sin(angle)
    chalk.chalk_arrow(ax2, sx, sy, sx + dx, sy + dy,
                      color=chalk.YELLOW, lw=0.8, head=6)

# Precession frequency
chalk.chalk_text(ax2, 2.5, 6.3, r'$\omega_L = \gamma |\mathbf{B}|$',
                 color=chalk.YELLOW, fontsize=11, style='normal')

# Bloch vector inset: M in the transverse plane, precessing
theta_p = np.radians(80)  # mostly transverse
draw_bloch_inset(ax2, mx=np.sin(theta_p), my=0, mz=np.cos(theta_p),
                 x0=5.5, y0=0.0)

# Small precession arc near the inset
chalk.chalk_text(ax2, 6.4, 0.0, r'$M_x(t) \sim \cos(\omega_L t)$',
                 color=chalk.RED, fontsize=8, style='normal')

# Annotation
chalk.chalk_text(ax2, 0.5, 0.5, 'frequency encodes field',
                 color=chalk.WHITE, fontsize=10)


# ============================================================
# Panel 3: READ
# ============================================================

ax3 = board.panel(2, title='3.  read')
ax3.set_xlim(-0.5, 8.5)
ax3.set_ylim(-0.5, 7.5)
ax3.set_aspect('equal')
ax3.axis('off')

draw_cell(ax3)
draw_B_field(ax3)

# Probe laser from below
chalk.chalk_arrow(ax3, 3.5, 0.0, 3.5, 2.0,
                  color=chalk.BLUE, lw=3.0, head=18)
chalk.chalk_text(ax3, 3.9, 0.3, 'probe', color=chalk.BLUE, fontsize=11)

# Input polarisation (horizontal line below cell)
chalk.chalk_line(ax3, [3.1, 3.9], [1.3, 1.3],
                 color=chalk.BLUE, lw=1.5)

# Probe exits top → detector
chalk.chalk_arrow(ax3, 3.5, 5.5, 3.5, 6.3,
                  color=chalk.BLUE, lw=2.0, head=14)

# Output polarisation (rotated, above cell)
chalk.chalk_line(ax3, [3.15, 3.85], [5.8, 6.1],
                 color=chalk.BLUE, lw=1.5)
chalk.chalk_text(ax3, 4.1, 5.8, r'$\theta_F \propto M_x$',
                 color=chalk.BLUE, fontsize=9, style='normal')

# Photodetector box
chalk.chalk_box(ax3, 2.8, 6.3, 1.4, 0.5, lw=1.0, pad=0.06)
chalk.chalk_text(ax3, 3.5, 6.55, 'PD', fontsize=9,
                 ha='center', va='center', style='normal')

# Signal coming out of detector — wire + FID
chalk.chalk_line(ax3, [4.2, 5.0], [6.55, 6.55],
                 color=chalk.WHITE, lw=0.8, linestyle='--')

sig_t = np.linspace(5.0, 8.0, 120)
sig_y = 6.55 + 0.25 * np.cos(8 * (sig_t - 5.0)) * np.exp(-(sig_t - 5.0) * 0.4)
ax3.plot(sig_t, sig_y, color=chalk.WHITE, linewidth=1.0, zorder=3)

chalk.chalk_text(ax3, 5.8, 7.0, 'signal at $\\omega_L$',
                 color=chalk.WHITE, fontsize=9, style='normal')

# Spins inside cell (some coherence remains)
np.random.seed(99)
for _ in range(10):
    sx = 1.8 + np.random.random() * 3.4
    sy = 2.3 + np.random.random() * 2.8
    angle = np.random.uniform(-0.5, 0.5)  # partial coherence
    dx = 0.18 * np.cos(angle)
    dy = 0.18 * np.sin(angle)
    chalk.chalk_arrow(ax3, sx, sy, sx + dx, sy + dy,
                      color=chalk.YELLOW, lw=0.8, head=6)

# Annotation + sensitivity
chalk.chalk_text(ax3, 0.5, 0.5, 'measure $\\omega_L$, know $|B|$',
                 color=chalk.WHITE, fontsize=10, style='normal')
chalk.chalk_text(ax3, 0.5, 0.0,
                 r'$\delta B \sim 1/(\gamma \sqrt{n\, T_2})$',
                 color=chalk.DIM, fontsize=9, style='normal')


# --- Save ---
out = os.path.join(_here, 'chalkboard_magnetometer.png')
board.save(out)
board.close()
print(f"Saved {out}")
