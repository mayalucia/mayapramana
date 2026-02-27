"""
Chalkboard illustration: the Bell-Bloom magnetometer setup.

Drawn on a physics lecture hall chalkboard — dark green surface,
chalk lines, permanent grid, chalk tray with coloured chalks.

This is the opening figure of Lesson 00: "Look at this."

Usage:
    python chalkboard_setup.py

Requires the mayapramana.chalkboard package (../python/mayapramana/chalkboard).
"""

import sys, os

# Add the python/ tree to the path so the package is importable
_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', 'python'))

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk

# --- Create the board: two sliding panels ---
# Grid only on the right panel (default). 5:3 aspect ratio (default).
board = Chalkboard(panels=2)

ax_main = board.panel(0, title='Bell-Bloom Magnetometer')
ax_signal = board.panel(1, title='free induction decay')

# ============================================================
# Left panel: experimental setup
# ============================================================
ax_main.set_xlim(-0.5, 10.5)
ax_main.set_ylim(-1, 9)
ax_main.set_aspect('equal')
ax_main.axis('off')

# The cell — a rounded rectangle
cell_x, cell_y = 3.5, 3.5
cell_w, cell_h = 3, 2
chalk.chalk_box(ax_main, cell_x, cell_y, cell_w, cell_h)
chalk.chalk_text(ax_main, cell_x + cell_w/2, cell_y + cell_h/2 + 0.3,
                 'Rb vapour', color=chalk.DIM, fontsize=10, ha='center', va='center')
chalk.chalk_text(ax_main, cell_x + cell_w/2, cell_y + cell_h/2 - 0.2,
                 'cell', color=chalk.DIM, fontsize=10, ha='center', va='center')

# Precessing spins inside the cell
np.random.seed(42)
for _ in range(8):
    ax_ = cell_x + 0.4 + np.random.random() * (cell_w - 0.8)
    ay_ = cell_y + 0.3 + np.random.random() * (cell_h - 0.6)
    angle = np.random.uniform(0, 2 * np.pi)
    dx = 0.2 * np.cos(angle)
    dy = 0.2 * np.sin(angle)
    chalk.chalk_arrow(ax_main, ax_, ay_, ax_ + dx, ay_ + dy,
                      color=chalk.YELLOW, lw=1.0, head=8)

# Pump laser (from left)
chalk.chalk_arrow(ax_main, 0.5, 4.5, cell_x, 4.5,
                  color=chalk.RED, lw=2.5, head=15)
chalk.chalk_text(ax_main, 0.3, 5.0, 'pump', color=chalk.RED, fontsize=10)
chalk.chalk_text(ax_main, 0.3, 4.7, 'laser', color=chalk.RED, fontsize=10)

# Circular polarisation symbol
chalk.chalk_circle(ax_main, 1.8, 4.5, 0.25, color=chalk.RED)
chalk.chalk_arrow(ax_main, 1.95, 4.35, 2.05, 4.6,
                  color=chalk.RED, lw=0.8, head=8)

# Probe laser (from bottom)
chalk.chalk_arrow(ax_main, 5, 1.0, 5, cell_y,
                  color=chalk.BLUE, lw=2.5, head=15)
chalk.chalk_text(ax_main, 5.4, 1.5, 'probe', color=chalk.BLUE, fontsize=10)

# Probe exits top, hits detector
chalk.chalk_arrow(ax_main, 5, cell_y + cell_h, 5, 7.5,
                  color=chalk.BLUE, lw=2.0, head=12)

# Detector box
det_x, det_y = 4.3, 7.3
chalk.chalk_box(ax_main, det_x, det_y, 1.4, 0.6, lw=1.2, pad=0.08)
chalk.chalk_text(ax_main, det_x + 0.7, det_y + 0.3, 'PD',
                 fontsize=9, ha='center', va='center', style='normal')

# Wire from detector to signal panel
chalk.chalk_line(ax_main,
                 [det_x + 1.4, 8.5, 8.5],
                 [det_y + 0.3, det_y + 0.3, 7.0],
                 color=chalk.DIM, lw=0.8, linestyle='--')
chalk.chalk_text(ax_main, 8.7, 7.5, 'signal', color=chalk.DIM,
                 fontsize=9, rotation=90, va='center')

# Magnetic field
chalk.chalk_arrow(ax_main, 7.5, 4.5, 9.5, 4.5,
                  color=chalk.YELLOW, lw=3, head=20)
chalk.chalk_text(ax_main, 8.5, 5.1, r'$\mathbf{B}$',
                 color=chalk.YELLOW, fontsize=16, ha='center', style='normal')
chalk.chalk_text(ax_main, 8.5, 3.8, '50 \u03bcT',
                 color=chalk.DIM, fontsize=9, ha='center')

# Precession annotation
chalk.chalk_text(ax_main, cell_x + cell_w + 0.3, cell_y + cell_h - 0.2,
                 r'$\omega_L = \gamma |B|$',
                 color=chalk.YELLOW, fontsize=11, style='normal')
chalk.chalk_text(ax_main, cell_x + cell_w + 0.3, cell_y + cell_h - 0.7,
                 '= 175 kHz', color=chalk.DIM, fontsize=10, style='normal')

# ============================================================
# Right panel: free induction decay signal
# ============================================================

# The signal: Mx(t) = cos(omega * t) * exp(-t/T2)
T2_ms = 10.0
f_visual = 0.8  # compressed frequency for visibility
t = np.linspace(0, 50, 2000)
envelope = np.exp(-t / T2_ms)
signal = envelope * np.cos(2 * np.pi * f_visual * t)

ax_signal.plot(t, signal, color=chalk.WHITE, linewidth=1.2, zorder=2)
ax_signal.plot(t, envelope, color=chalk.RED, linewidth=0.8,
               linestyle='--', zorder=2, alpha=0.7)
ax_signal.plot(t, -envelope, color=chalk.RED, linewidth=0.8,
               linestyle='--', zorder=2, alpha=0.7)

ax_signal.set_xlim(0, 50)
ax_signal.set_ylim(-1.15, 1.15)
ax_signal.set_xlabel('time (ms)', fontsize=10, color=chalk.DIM,
                     fontfamily='serif')
ax_signal.set_ylabel('$M_x(t)$', fontsize=12, color=chalk.WHITE,
                     fontfamily='serif')

# T2 annotation
ax_signal.annotate('$T_2$', xy=(T2_ms, np.exp(-1)), xytext=(18, 0.7),
                   fontsize=12, color=chalk.RED, fontfamily='serif',
                   arrowprops=dict(arrowstyle='->', color=chalk.RED, lw=1.0))

# Frequency annotation
chalk.chalk_text(ax_signal, 35, -0.9, r'$f = \omega_L / 2\pi$',
                 color=chalk.YELLOW, fontsize=10, style='normal')
chalk.chalk_text(ax_signal, 35, -1.05, '= 175 kHz',
                 color=chalk.DIM, fontsize=9, style='normal')
chalk.chalk_text(ax_signal, 35, -0.55, '(compressed',
                 color=chalk.DIM, fontsize=7)
chalk.chalk_text(ax_signal, 35, -0.68, ' for visibility)',
                 color=chalk.DIM, fontsize=7)

# --- Save ---
out = os.path.join(_here, 'chalkboard_setup.png')
board.save(out)
board.close()
print(f"Saved {out}")
