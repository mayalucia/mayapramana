"""
Chalkboard illustration: relaxation — T2 dephasing and T1 recovery.

Left panel: top-down view of the xy-plane. The transverse magnetisation
M_perp spirals inward as atoms dephase (T2 decay). Individual spin
arrows fan out; the average shrinks.

Right panel: M_z vs time. Starting from zero (or depleted), M_z
recovers exponentially toward M_0 with time constant T1.

Usage:
    python chalkboard_relaxation.py
"""

import sys, os

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, '..', '..', 'python'))

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk


board = Chalkboard(panels=2, figsize=(14, 7))
ax_t2 = board.panel(0, title='transverse decay ($T_2$)')
ax_t1 = board.panel(1, title='longitudinal recovery ($T_1$)')


# ============================================================
# Left panel: T2 — spiral in the xy-plane (top-down view)
# ============================================================

ax_t2.set_xlim(-1.4, 1.4)
ax_t2.set_ylim(-1.4, 1.4)
ax_t2.set_aspect('equal')
ax_t2.axis('off')

# Axes: x and y
chalk.chalk_arrow(ax_t2, -1.2, 0, 1.2, 0, color=chalk.DIM, lw=0.8, head=10)
chalk.chalk_arrow(ax_t2, 0, -1.2, 0, 1.2, color=chalk.DIM, lw=0.8, head=10)
chalk.chalk_text(ax_t2, 1.15, -0.15, '$M_x$', color=chalk.DIM,
                 fontsize=10, style='normal')
chalk.chalk_text(ax_t2, 0.08, 1.15, '$M_y$', color=chalk.DIM,
                 fontsize=10, style='normal')

# Unit circle (Bloch sphere equator)
theta = np.linspace(0, 2 * np.pi, 200)
ax_t2.plot(np.cos(theta), np.sin(theta), color=chalk.DIM,
           linewidth=0.5, linestyle=':', alpha=0.4)

# The spiral: M_perp(t) = exp(-t/T2) * [cos(wt), sin(wt)]
# Use normalised time: let omega*T2 ~ 8 full turns
n_turns = 6
t_spiral = np.linspace(0, n_turns * 2 * np.pi, 2000)
decay = np.exp(-t_spiral / (n_turns * 2 * np.pi) * 3)  # decay over ~3 T2
spiral_x = decay * np.cos(t_spiral)
spiral_y = decay * np.sin(t_spiral)

# Draw the spiral — fade from white to dim as it decays
n_seg = 20
seg_len = len(t_spiral) // n_seg
for i in range(n_seg):
    i0 = i * seg_len
    i1 = min((i + 1) * seg_len + 1, len(t_spiral))
    alpha = 0.9 - 0.6 * (i / n_seg)
    lw = 1.5 - 0.8 * (i / n_seg)
    color = chalk.WHITE if i < n_seg // 2 else chalk.DIM
    ax_t2.plot(spiral_x[i0:i1], spiral_y[i0:i1],
               color=color, linewidth=lw, alpha=alpha, zorder=2)

# Current M vector (at the start of the spiral)
chalk.chalk_arrow(ax_t2, 0, 0, spiral_x[0], spiral_y[0],
                  color=chalk.RED, lw=2.5, head=14)

# Ghost M vectors at later times (fading)
ghost_indices = [len(t_spiral) // 5, 2 * len(t_spiral) // 5,
                 3 * len(t_spiral) // 5]
for gi in ghost_indices:
    gx, gy = spiral_x[gi], spiral_y[gi]
    alpha_g = 0.4 * (1 - gi / len(t_spiral))
    chalk.chalk_arrow(ax_t2, 0, 0, gx, gy,
                      color=chalk.RED, lw=1.0, head=8)

# Individual spins fanning out (at a later time)
# Show 6 spins that were coherent but have drifted apart
fan_t = len(t_spiral) // 3
base_angle = t_spiral[fan_t]
fan_r = decay[fan_t]
np.random.seed(7)
for k in range(6):
    delta_phi = np.random.uniform(-0.8, 0.8)
    sx = fan_r * np.cos(base_angle + delta_phi)
    sy = fan_r * np.sin(base_angle + delta_phi)
    chalk.chalk_arrow(ax_t2, 0, 0, sx, sy,
                      color=chalk.YELLOW, lw=0.6, head=6)

# Annotation
chalk.chalk_text(ax_t2, -1.3, -1.3,
                 r'$M_\perp(t) = M_\perp(0)\, e^{-t/T_2}$',
                 color=chalk.WHITE, fontsize=11, style='normal')

# Label: "individual spins dephase"
chalk.chalk_text(ax_t2, 0.4, -1.1, 'spins dephase',
                 color=chalk.YELLOW, fontsize=9)


# ============================================================
# Right panel: T1 — longitudinal recovery
# ============================================================

# M_z(t) = M_0 * (1 - exp(-t/T1))  starting from M_z=0
# Also show the case starting from M_z = -M_0 (inversion recovery)

T1 = 1.0  # normalised
t = np.linspace(0, 5 * T1, 500)

mz_from_zero = 1.0 * (1 - np.exp(-t / T1))
mz_from_neg = 1.0 * (1 - 2 * np.exp(-t / T1))

ax_t1.plot(t, mz_from_zero, color=chalk.WHITE, linewidth=1.5,
           label=r'from $M_z = 0$', zorder=2)
ax_t1.plot(t, mz_from_neg, color=chalk.BLUE, linewidth=1.2,
           linestyle='--', label=r'from $M_z = -M_0$', zorder=2)

# Equilibrium line
ax_t1.axhline(y=1.0, color=chalk.YELLOW, linewidth=0.8, linestyle=':',
              alpha=0.6)
chalk.chalk_text(ax_t1, 4.2, 1.05, '$M_0$', color=chalk.YELLOW,
                 fontsize=11, style='normal')

# Zero line
ax_t1.axhline(y=0, color=chalk.DIM, linewidth=0.5, linestyle=':',
              alpha=0.3)

# T1 marker
t1_mz = 1.0 * (1 - np.exp(-1))
ax_t1.plot(T1, t1_mz, 'o', color=chalk.RED, markersize=5, zorder=3)
ax_t1.annotate('$T_1$', xy=(T1, t1_mz), xytext=(1.8, 0.3),
               fontsize=12, color=chalk.RED, fontfamily='serif',
               arrowprops=dict(arrowstyle='->', color=chalk.RED, lw=1.0))

ax_t1.set_xlim(0, 5)
ax_t1.set_ylim(-1.15, 1.25)
ax_t1.set_xlabel('$t / T_1$', fontsize=11, color=chalk.DIM,
                 fontfamily='serif')
ax_t1.set_ylabel('$M_z$', fontsize=12, color=chalk.WHITE,
                 fontfamily='serif')

# Annotation
chalk.chalk_text(ax_t1, 2.5, -0.85,
                 r'$M_z(t) \to M_0\,(1 - e^{-t/T_1})$',
                 color=chalk.WHITE, fontsize=10, style='normal')

chalk.chalk_text(ax_t1, 2.5, -1.0,
                 'system thermalises',
                 color=chalk.DIM, fontsize=9)


# --- Save ---
out = os.path.join(_here, 'chalkboard_relaxation.png')
board.save(out)
board.close()
print(f"Saved {out}")
