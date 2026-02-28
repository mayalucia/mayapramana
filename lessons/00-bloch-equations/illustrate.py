# [[file:illustrate.org::illustrate-init][illustrate-init]]
"""
Lesson 00 — Bloch Equations: chalkboard illustrations.

Tangled from illustrate.org.  Do not edit directly.

Each function draws one chalkboard figure and saves it to the given path.
Import from the lesson notebook::

    import illustrate as ill
    ill.setup()                  # default figure
    ill.precession_cone(theta=60)  # customised
"""

import numpy as np
from mayapramana.chalkboard import Chalkboard, chalk
# illustrate-init ends here


# [[file:illustrate.org::illustrate-setup][illustrate-setup]]
def setup(out='chalkboard_setup.png', *, T2_ms=10.0, f_visual=0.8):
    """Bell-Bloom magnetometer overview + free induction decay.

    Parameters
    ----------
    out : str
        Output file path.
    T2_ms : float
        Transverse relaxation time in ms (controls envelope decay).
    f_visual : float
        Compressed oscillation frequency for visibility (Hz-scale, not kHz).
    """
    board = Chalkboard(panels=2)
    ax_main = board.panel(0, title='Bell-Bloom Magnetometer')
    ax_signal = board.panel(1, title='free induction decay')

    # --- Left panel: experimental setup ---
    ax_main.set_xlim(-0.5, 10.5)
    ax_main.set_ylim(-1, 9)
    ax_main.set_aspect('equal')
    ax_main.axis('off')

    # Rubidium vapour cell
    cell_x, cell_y = 3.5, 3.5
    cell_w, cell_h = 3, 2
    chalk.chalk_box(ax_main, cell_x, cell_y, cell_w, cell_h)
    chalk.chalk_text(ax_main, cell_x + cell_w/2, cell_y + cell_h/2 + 0.3,
                     'Rb vapour', color=chalk.DIM, fontsize=10,
                     ha='center', va='center')
    chalk.chalk_text(ax_main, cell_x + cell_w/2, cell_y + cell_h/2 - 0.2,
                     'cell', color=chalk.DIM, fontsize=10,
                     ha='center', va='center')

    # Precessing spins inside the cell
    np.random.seed(42)
    for _ in range(8):
        ax_ = cell_x + 0.4 + np.random.random() * (cell_w - 0.8)
        ay_ = cell_y + 0.3 + np.random.random() * (cell_h - 0.6)
        angle = np.random.uniform(0, 2 * np.pi)
        dx, dy = 0.2 * np.cos(angle), 0.2 * np.sin(angle)
        chalk.chalk_arrow(ax_main, ax_, ay_, ax_ + dx, ay_ + dy,
                          color=chalk.YELLOW, lw=1.0, head=8)

    # Pump laser (from left)
    chalk.chalk_arrow(ax_main, 0.5, 4.5, cell_x, 4.5,
                      color=chalk.RED, lw=2.5, head=15)
    chalk.chalk_text(ax_main, 0.3, 5.0, 'pump', color=chalk.RED, fontsize=10)
    chalk.chalk_text(ax_main, 0.3, 4.7, 'laser', color=chalk.RED, fontsize=10)
    chalk.chalk_circle(ax_main, 1.8, 4.5, 0.25, color=chalk.RED)
    chalk.chalk_arrow(ax_main, 1.95, 4.35, 2.05, 4.6,
                      color=chalk.RED, lw=0.8, head=8)

    # Probe laser (from bottom)
    chalk.chalk_arrow(ax_main, 5, 1.0, 5, cell_y,
                      color=chalk.BLUE, lw=2.5, head=15)
    chalk.chalk_text(ax_main, 5.4, 1.5, 'probe', color=chalk.BLUE, fontsize=10)
    chalk.chalk_arrow(ax_main, 5, cell_y + cell_h, 5, 7.5,
                      color=chalk.BLUE, lw=2.0, head=12)

    # Photodetector
    det_x, det_y = 4.3, 7.3
    chalk.chalk_box(ax_main, det_x, det_y, 1.4, 0.6, lw=1.2, pad=0.08)
    chalk.chalk_text(ax_main, det_x + 0.7, det_y + 0.3, 'PD',
                     fontsize=9, ha='center', va='center', style='normal')

    # Wire from detector to signal panel
    chalk.chalk_line(ax_main, [det_x + 1.4, 8.5, 8.5],
                     [det_y + 0.3, det_y + 0.3, 7.0],
                     color=chalk.DIM, lw=0.8, linestyle='--')
    chalk.chalk_text(ax_main, 8.7, 7.5, 'signal', color=chalk.DIM,
                     fontsize=9, rotation=90, va='center')

    # Magnetic field
    chalk.chalk_arrow(ax_main, 7.5, 4.5, 9.5, 4.5,
                      color=chalk.YELLOW, lw=3, head=20)
    chalk.chalk_text(ax_main, 8.5, 5.1, r'$\mathbf{B}$',
                     color=chalk.YELLOW, fontsize=16, ha='center', style='normal')
    chalk.chalk_text(ax_main, 8.5, 3.8, '50 μT',
                     color=chalk.DIM, fontsize=9, ha='center')

    # Precession frequency
    chalk.chalk_text(ax_main, cell_x + cell_w + 0.3, cell_y + cell_h - 0.2,
                     r'$\omega_L = \gamma |B|$',
                     color=chalk.YELLOW, fontsize=11, style='normal')
    chalk.chalk_text(ax_main, cell_x + cell_w + 0.3, cell_y + cell_h - 0.7,
                     '= 175 kHz', color=chalk.DIM, fontsize=10, style='normal')

    # --- Right panel: free induction decay ---
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

    ax_signal.annotate('$T_2$', xy=(T2_ms, np.exp(-1)), xytext=(18, 0.7),
                       fontsize=12, color=chalk.RED, fontfamily='serif',
                       arrowprops=dict(arrowstyle='->', color=chalk.RED, lw=1.0))

    chalk.chalk_text(ax_signal, 35, -0.9, r'$f = \omega_L / 2\pi$',
                     color=chalk.YELLOW, fontsize=10, style='normal')
    chalk.chalk_text(ax_signal, 35, -1.05, '= 175 kHz',
                     color=chalk.DIM, fontsize=9, style='normal')
    chalk.chalk_text(ax_signal, 35, -0.55, '(compressed',
                     color=chalk.DIM, fontsize=7)
    chalk.chalk_text(ax_signal, 35, -0.68, ' for visibility)',
                     color=chalk.DIM, fontsize=7)

    board.save(out)
    board.close()
    return out
# illustrate-setup ends here


# [[file:illustrate.org::illustrate-precession-cone][illustrate-precession-cone]]
def precession_cone(out='chalkboard_precession_cone.png', *,
                    theta_deg=40, phi_deg=30):
    """Larmor precession: spin M traces a cone around B.

    Parameters
    ----------
    theta_deg : float
        Half-angle of the precession cone in degrees.
    phi_deg : float
        Azimuthal snapshot angle of M in degrees.
    """
    board = Chalkboard(panels=1, figsize=(8, 7), grid_panels=set())
    ax = board.panel(0, title='Larmor precession')
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.2, 1.8)
    ax.set_aspect('equal'); ax.axis('off')

    # B field along z
    chalk.chalk_arrow(ax, 0, -0.8, 0, 1.6, color=chalk.YELLOW, lw=2.5, head=18)
    chalk.chalk_text(ax, 0.08, 1.55, r'$\mathbf{B}$',
                     color=chalk.YELLOW, fontsize=16, style='normal')

    theta = np.radians(theta_deg)
    M_len = 1.2
    phi_snapshot = np.radians(phi_deg)

    # Oblique 3D → 2D projection
    def project(x3, y3, z3, oblique=0.35):
        return x3 - oblique * y3 * 0.5, z3 + oblique * y3 * 0.3

    cone_z = M_len * np.cos(theta)
    cone_r = M_len * np.sin(theta)

    # Precession orbit (ellipse in projection)
    phi_vals = np.linspace(0, 2 * np.pi, 200)
    orbit_x, orbit_z = [], []
    for phi in phi_vals:
        px, pz = project(cone_r * np.cos(phi), cone_r * np.sin(phi), cone_z)
        orbit_x.append(px); orbit_z.append(pz)

    # Split into front (solid) and back (dashed)
    back_x, back_z, front_x, front_z = [], [], [], []
    for i, phi in enumerate(phi_vals):
        if np.sin(phi) > 0:
            back_x.append(orbit_x[i]); back_z.append(orbit_z[i])
        else:
            front_x.append(orbit_x[i]); front_z.append(orbit_z[i])
    if back_x:
        ax.plot(back_x, back_z, color=chalk.DIM, linewidth=0.8,
                linestyle='--', alpha=0.5, zorder=1)
    if front_x:
        ax.plot(front_x, front_z, color=chalk.WHITE, linewidth=1.2, zorder=2)

    # Cone generators (dashed lines from origin to orbit edge)
    for ang in [0, np.pi]:
        ex, ez = project(cone_r * np.cos(ang), cone_r * np.sin(ang), cone_z)
        chalk.chalk_line(ax, [0, ex], [0, ez], color=chalk.DIM, lw=0.6,
                         linestyle=':', alpha=0.5)

    # M vector at the snapshot azimuth
    mx3 = cone_r * np.cos(phi_snapshot)
    my3 = cone_r * np.sin(phi_snapshot)
    tip_x, tip_z = project(mx3, my3, cone_z)
    chalk.chalk_arrow(ax, 0, 0, tip_x, tip_z,
                      color=chalk.RED, lw=2.5, head=16)
    chalk.chalk_text(ax, tip_x + 0.08, tip_z + 0.05, r'$\mathbf{M}$',
                     color=chalk.RED, fontsize=14, style='normal')

    # ω_L precession arc (just outside the orbit)
    arc_scale = 1.08
    arc_phi = np.linspace(phi_snapshot + 0.15, phi_snapshot + 1.2, 50)
    arc_xs, arc_zs = [], []
    for p in arc_phi:
        px, pz = project(cone_r * arc_scale * np.cos(p),
                         cone_r * arc_scale * np.sin(p), cone_z)
        arc_xs.append(px); arc_zs.append(pz)
    ax.plot(arc_xs, arc_zs, color=chalk.BLUE, linewidth=1.2, alpha=0.9, zorder=3)
    chalk.chalk_arrow(ax, arc_xs[-2], arc_zs[-2], arc_xs[-1], arc_zs[-1],
                      color=chalk.BLUE, lw=1.0, head=12)
    chalk.chalk_text(ax, arc_xs[-1] - 0.22, arc_zs[-1] + 0.1,
                     r'$\omega_L$', color=chalk.BLUE, fontsize=12, style='normal')

    # θ angle arc
    angle_r = 0.4
    angle_phi = np.linspace(0, theta, 30)
    ax.plot([angle_r * np.sin(a) for a in angle_phi],
            [angle_r * np.cos(a) for a in angle_phi],
            color=chalk.DIM, linewidth=0.8)
    chalk.chalk_text(ax, 0.22, 0.35, r'$\theta$', color=chalk.DIM,
                     fontsize=11, style='normal')
    chalk.chalk_text(ax, -0.18, -0.85, r'$\hat{z}$', color=chalk.DIM,
                     fontsize=11, style='normal')

    # Caption
    chalk.chalk_text(ax, -1.4, -1.05,
                     r'$d\mathbf{M}/dt = \gamma\,\mathbf{M} \times \mathbf{B}$'
                     '      precession, no relaxation',
                     color=chalk.WHITE, fontsize=11, style='normal')

    board.save(out)
    board.close()
    return out
# illustrate-precession-cone ends here


# [[file:illustrate.org::illustrate-relaxation][illustrate-relaxation]]
def relaxation(out='chalkboard_relaxation.png'):
    """T2 transverse decay spiral + T1 longitudinal recovery."""
    board = Chalkboard(panels=2, figsize=(14, 7))
    ax_t2 = board.panel(0, title='transverse decay ($T_2$)')
    ax_t1 = board.panel(1, title='longitudinal recovery ($T_1$)')

    # --- Left panel: T2 spiral in xy-plane ---
    ax_t2.set_xlim(-1.4, 1.4); ax_t2.set_ylim(-1.4, 1.4)
    ax_t2.set_aspect('equal'); ax_t2.axis('off')
    chalk.chalk_arrow(ax_t2, -1.2, 0, 1.2, 0, color=chalk.DIM, lw=0.8, head=10)
    chalk.chalk_arrow(ax_t2, 0, -1.2, 0, 1.2, color=chalk.DIM, lw=0.8, head=10)
    chalk.chalk_text(ax_t2, 1.15, -0.15, '$M_x$', color=chalk.DIM,
                     fontsize=10, style='normal')
    chalk.chalk_text(ax_t2, 0.08, 1.15, '$M_y$', color=chalk.DIM,
                     fontsize=10, style='normal')
    theta = np.linspace(0, 2 * np.pi, 200)
    ax_t2.plot(np.cos(theta), np.sin(theta), color=chalk.DIM,
               linewidth=0.5, linestyle=':', alpha=0.4)

    # Spiral: M_perp(t) = exp(-t/T2) * [cos(wt), sin(wt)]
    n_turns = 6
    t_spiral = np.linspace(0, n_turns * 2 * np.pi, 2000)
    decay = np.exp(-t_spiral / (n_turns * 2 * np.pi) * 3)
    spiral_x = decay * np.cos(t_spiral)
    spiral_y = decay * np.sin(t_spiral)

    # Draw in segments with fading alpha
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

    # Current M (start of spiral) + ghost vectors
    chalk.chalk_arrow(ax_t2, 0, 0, spiral_x[0], spiral_y[0],
                      color=chalk.RED, lw=2.5, head=14)
    for gi in [len(t_spiral) // 5, 2 * len(t_spiral) // 5, 3 * len(t_spiral) // 5]:
        chalk.chalk_arrow(ax_t2, 0, 0, spiral_x[gi], spiral_y[gi],
                          color=chalk.RED, lw=1.0, head=8)

    # Individual spins fanning out (at t = T2/3)
    fan_t = len(t_spiral) // 3
    base_angle = t_spiral[fan_t]; fan_r = decay[fan_t]
    np.random.seed(7)
    for k in range(6):
        delta_phi = np.random.uniform(-0.8, 0.8)
        chalk.chalk_arrow(ax_t2, 0, 0,
                          fan_r * np.cos(base_angle + delta_phi),
                          fan_r * np.sin(base_angle + delta_phi),
                          color=chalk.YELLOW, lw=0.6, head=6)

    chalk.chalk_text(ax_t2, -1.3, -1.3,
                     r'$M_\perp(t) = M_\perp(0)\, e^{-t/T_2}$',
                     color=chalk.WHITE, fontsize=11, style='normal')
    chalk.chalk_text(ax_t2, 0.4, -1.1, 'spins dephase',
                     color=chalk.YELLOW, fontsize=9)

    # --- Right panel: T1 recovery ---
    T1 = 1.0
    t = np.linspace(0, 5 * T1, 500)
    ax_t1.plot(t, 1.0 * (1 - np.exp(-t / T1)), color=chalk.WHITE,
               linewidth=1.5, label=r'from $M_z = 0$', zorder=2)
    ax_t1.plot(t, 1.0 * (1 - 2 * np.exp(-t / T1)), color=chalk.BLUE,
               linewidth=1.2, linestyle='--', label=r'from $M_z = -M_0$', zorder=2)
    ax_t1.axhline(y=1.0, color=chalk.YELLOW, linewidth=0.8, linestyle=':', alpha=0.6)
    chalk.chalk_text(ax_t1, 4.2, 1.05, '$M_0$', color=chalk.YELLOW,
                     fontsize=11, style='normal')
    ax_t1.axhline(y=0, color=chalk.DIM, linewidth=0.5, linestyle=':', alpha=0.3)
    t1_mz = 1.0 * (1 - np.exp(-1))
    ax_t1.plot(T1, t1_mz, 'o', color=chalk.RED, markersize=5, zorder=3)
    ax_t1.annotate('$T_1$', xy=(T1, t1_mz), xytext=(1.8, 0.3),
                   fontsize=12, color=chalk.RED, fontfamily='serif',
                   arrowprops=dict(arrowstyle='->', color=chalk.RED, lw=1.0))
    ax_t1.set_xlim(0, 5); ax_t1.set_ylim(-1.15, 1.25)
    ax_t1.set_xlabel('$t / T_1$', fontsize=11, color=chalk.DIM, fontfamily='serif')
    ax_t1.set_ylabel('$M_z$', fontsize=12, color=chalk.WHITE, fontfamily='serif')
    chalk.chalk_text(ax_t1, 2.5, -0.85,
                     r'$M_z(t) \to M_0\,(1 - e^{-t/T_1})$',
                     color=chalk.WHITE, fontsize=10, style='normal')
    chalk.chalk_text(ax_t1, 2.5, -1.0, 'system thermalises',
                     color=chalk.DIM, fontsize=9)

    board.save(out)
    board.close()
    return out
# illustrate-relaxation ends here


# [[file:illustrate.org::illustrate-bloch-terms][illustrate-bloch-terms]]
def bloch_terms(out='chalkboard_bloch_terms.png'):
    """Three Bloch equation terms: precession, T2 dephasing, T1 recovery."""
    board = Chalkboard(panels=3, figsize=(21, 10),
                       grid_panels=set(), panel_weights=[1, 1, 1])

    def draw_bloch_sphere(ax):
        ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6)
        ax.set_aspect('equal'); ax.axis('off')
        phi = np.linspace(0, 2 * np.pi, 200)
        ax.plot(np.cos(phi), 0.3 * np.sin(phi),
                color=chalk.DIM, linewidth=0.5, linestyle=':', alpha=0.4)
        ax.plot(0.3 * np.sin(phi), np.cos(phi),
                color=chalk.DIM, linewidth=0.5, linestyle=':', alpha=0.3)
        ax.plot(np.cos(phi), np.sin(phi),
                color=chalk.DIM, linewidth=0.6, alpha=0.5)
        chalk.chalk_arrow(ax, 0, -1.3, 0, 1.3, color=chalk.DIM, lw=0.6, head=8)
        chalk.chalk_arrow(ax, -1.3, 0, 1.3, 0, color=chalk.DIM, lw=0.6, head=8)
        chalk.chalk_text(ax, 0.07, 1.25, '$z$', color=chalk.DIM,
                         fontsize=9, style='normal')
        chalk.chalk_text(ax, 1.2, -0.15, '$x$', color=chalk.DIM,
                         fontsize=9, style='normal')

    def plot_masked(ax, x, z, mask, **kwargs):
        segs = np.diff(mask.astype(int))
        starts = np.where(segs == 1)[0] + 1
        ends = np.where(segs == -1)[0] + 1
        if mask[0]: starts = np.concatenate([[0], starts])
        if mask[-1]: ends = np.concatenate([ends, [len(mask)]])
        for s, e in zip(starts, ends):
            ax.plot(x[s:e], z[s:e], **kwargs)

    # --- Panel 1: Precession ---
    ax1 = board.panel(0, title=r'$\gamma\,\mathbf{M} \times \mathbf{B}$')
    draw_bloch_sphere(ax1)
    chalk.chalk_arrow(ax1, 0, 1.0, 0, 1.45, color=chalk.YELLOW, lw=2.0, head=14)
    chalk.chalk_text(ax1, 0.1, 1.38, r'$\mathbf{B}$', color=chalk.YELLOW,
                     fontsize=12, style='normal')
    theta_m = np.radians(50)
    mx, mz = np.sin(theta_m), np.cos(theta_m)
    chalk.chalk_arrow(ax1, 0, 0, mx, mz, color=chalk.RED, lw=2.5, head=14)
    chalk.chalk_text(ax1, mx + 0.08, mz + 0.05, r'$\mathbf{M}$',
                     color=chalk.RED, fontsize=12, style='normal')
    orbit_phi = np.linspace(0, 2 * np.pi, 200)
    orbit_r = np.sin(theta_m)
    orbit_x = orbit_r * np.cos(orbit_phi)
    orbit_z = mz + orbit_r * 0.3 * np.sin(orbit_phi)
    back_mask = np.sin(orbit_phi) > 0
    plot_masked(ax1, orbit_x, orbit_z, back_mask,
                color=chalk.DIM, linewidth=0.6, linestyle='--', alpha=0.4)
    plot_masked(ax1, orbit_x, orbit_z, ~back_mask,
                color=chalk.WHITE, linewidth=1.0, alpha=0.7)
    arc_phi = np.linspace(0, 1.5, 40)
    arc_r = orbit_r * 0.85
    arc_x = arc_r * np.cos(arc_phi)
    arc_z = mz + arc_r * 0.3 * np.sin(arc_phi)
    ax1.plot(arc_x, arc_z, color=chalk.BLUE, linewidth=1.2, zorder=3)
    chalk.chalk_arrow(ax1, arc_x[-2], arc_z[-2], arc_x[-1], arc_z[-1],
                      color=chalk.BLUE, lw=1.0, head=10)
    chalk.chalk_text(ax1, -1.4, -1.45, 'rotation',
                     color=chalk.WHITE, fontsize=10)
    chalk.chalk_text(ax1, -1.4, -1.55, r'$|\mathbf{M}|$ preserved',
                     color=chalk.DIM, fontsize=8, style='normal')

    # --- Panel 2: T2 decay ---
    ax2 = board.panel(1, title=r'$-M_x/T_2,\; -M_y/T_2$')
    draw_bloch_sphere(ax2)
    theta_m2 = np.radians(60)
    mx2, mz2 = np.sin(theta_m2), np.cos(theta_m2)
    chalk.chalk_arrow(ax2, 0, 0, mx2, mz2, color=chalk.RED, lw=2.5, head=14)
    chalk.chalk_text(ax2, mx2 + 0.08, mz2 + 0.05, r'$\mathbf{M}$',
                     color=chalk.RED, fontsize=12, style='normal')
    chalk.chalk_arrow(ax2, mx2, mz2, mx2 - 0.35 * np.sin(theta_m2), mz2,
                      color=chalk.BLUE, lw=2.0, head=12)
    chalk.chalk_line(ax2, [0, mx2], [mz2, mz2], color=chalk.DIM, lw=0.6,
                     linestyle='--', alpha=0.5)
    chalk.chalk_line(ax2, [mx2, mx2], [0, mz2], color=chalk.DIM, lw=0.6,
                     linestyle='--', alpha=0.5)
    chalk.chalk_arrow(ax2, 0, 0, 0, mz2, color=chalk.DIM, lw=1.5, head=10)
    chalk.chalk_text(ax2, -0.35, mz2 / 2, '$M_z$', color=chalk.DIM,
                     fontsize=9, style='normal')
    chalk.chalk_text(ax2, mx2 / 2 - 0.05, mz2 + 0.1, '$M_\\perp$',
                     color=chalk.RED, fontsize=9, style='normal')
    chalk.chalk_text(ax2, -1.4, -1.45, 'dephasing',
                     color=chalk.WHITE, fontsize=10)
    chalk.chalk_text(ax2, -1.4, -1.55, r'$|\mathbf{M}|$ shrinks',
                     color=chalk.DIM, fontsize=8, style='normal')

    # --- Panel 3: T1 recovery ---
    ax3 = board.panel(2, title=r'$-(M_z - M_0)/T_1$')
    draw_bloch_sphere(ax3)
    mz_current = 0.15
    chalk.chalk_arrow(ax3, 0, 0, 0, mz_current, color=chalk.RED, lw=2.5, head=14)
    chalk.chalk_text(ax3, 0.1, mz_current - 0.05, r'$\mathbf{M}$',
                     color=chalk.RED, fontsize=12, style='normal')
    m0_z = 0.85
    chalk.chalk_arrow(ax3, 0, mz_current, 0, m0_z,
                      color=chalk.BLUE, lw=2.0, head=12)
    ax3.plot(0, m0_z, 'o', color=chalk.YELLOW, markersize=6, zorder=3)
    chalk.chalk_text(ax3, 0.12, m0_z, '$M_0$', color=chalk.YELLOW,
                     fontsize=11, style='normal')
    for frac in [0.3, 0.5, 0.7]:
        ax3.plot(0, mz_current + frac * (m0_z - mz_current), 'o',
                 color=chalk.DIM, markersize=3, alpha=0.4, zorder=2)
    chalk.chalk_text(ax3, -1.4, -1.45, 'thermalisation',
                     color=chalk.WHITE, fontsize=10)
    chalk.chalk_text(ax3, -1.4, -1.55, r'$M_z \to M_0$',
                     color=chalk.DIM, fontsize=8, style='normal')

    board.save(out)
    board.close()
    return out
# illustrate-bloch-terms ends here


# [[file:illustrate.org::illustrate-magnetometer][illustrate-magnetometer]]
def magnetometer(out='chalkboard_magnetometer.png'):
    """Three-step magnetometer: pump, precess, read."""
    board = Chalkboard(panels=3, figsize=(21, 10),
                       grid_panels=set(), panel_weights=[1, 1, 1])

    def draw_cell(ax, label=None):
        chalk.chalk_box(ax, 1.5, 2.0, 4.0, 3.5, lw=1.2, pad=0.1)
        if label:
            chalk.chalk_text(ax, 3.5, 5.7, label, color=chalk.DIM,
                             fontsize=9, ha='center')

    def draw_B_field(ax):
        chalk.chalk_arrow(ax, 6.0, 3.75, 7.5, 3.75,
                          color=chalk.YELLOW, lw=2.0, head=14)
        chalk.chalk_text(ax, 6.8, 4.15, r'$\mathbf{B}$',
                         color=chalk.YELLOW, fontsize=13, style='normal', ha='center')

    def draw_bloch_inset(ax, mx, my, mz, x0=2.5, y0=0.2, size=1.5):
        cx, cy = x0 + size / 2, y0 + size / 2
        phi = np.linspace(0, 2 * np.pi, 100)
        r = size * 0.45
        ax.plot(cx + r * np.cos(phi), cy + r * np.sin(phi),
                color=chalk.DIM, linewidth=0.5, alpha=0.4)
        ax.plot(cx + r * np.cos(phi), cy + 0.25 * r * np.sin(phi),
                color=chalk.DIM, linewidth=0.4, linestyle=':', alpha=0.3)
        chalk.chalk_line(ax, [cx, cx], [cy - r * 1.1, cy + r * 1.1],
                         color=chalk.DIM, lw=0.4, alpha=0.3)
        chalk.chalk_line(ax, [cx - r * 1.1, cx + r * 1.1], [cy, cy],
                         color=chalk.DIM, lw=0.4, alpha=0.3)
        m_norm = np.sqrt(mx**2 + mz**2) or 1.0
        scale = r * 0.85
        chalk.chalk_arrow(ax, cx, cy, cx + mx / m_norm * scale,
                          cy + mz / m_norm * scale,
                          color=chalk.RED, lw=2.0, head=10)

    # --- Panel 1: PUMP ---
    ax1 = board.panel(0, title='1.  pump')
    ax1.set_xlim(-0.5, 8.5); ax1.set_ylim(-0.5, 7.5)
    ax1.set_aspect('equal'); ax1.axis('off')
    draw_cell(ax1, 'Rb cell'); draw_B_field(ax1)
    chalk.chalk_arrow(ax1, -0.3, 3.75, 1.5, 3.75, color=chalk.RED, lw=3.0, head=18)
    chalk.chalk_text(ax1, 0.0, 4.5, 'pump', color=chalk.RED, fontsize=11)
    chalk.chalk_text(ax1, 0.0, 4.1, 'laser', color=chalk.RED, fontsize=11)
    chalk.chalk_circle(ax1, 0.7, 3.75, 0.2, color=chalk.RED)
    np.random.seed(42)
    for _ in range(10):
        sx = 1.8 + np.random.random() * 3.4
        sy = 2.3 + np.random.random() * 2.8
        angle = np.random.uniform(-0.3, 0.3)
        chalk.chalk_arrow(ax1, sx, sy, sx + 0.25 * np.cos(angle),
                          sy + 0.25 * np.sin(angle),
                          color=chalk.YELLOW, lw=0.8, head=6)
    draw_bloch_inset(ax1, mx=0, my=0, mz=1, x0=5.5, y0=0.0)
    chalk.chalk_text(ax1, 6.4, 0.0, r'$M_z = M_0$', color=chalk.RED,
                     fontsize=9, style='normal')
    chalk.chalk_text(ax1, 0.5, 0.5, 'create polarisation',
                     color=chalk.WHITE, fontsize=10)

    # --- Panel 2: PRECESS ---
    ax2 = board.panel(1, title='2.  precess')
    ax2.set_xlim(-0.5, 8.5); ax2.set_ylim(-0.5, 7.5)
    ax2.set_aspect('equal'); ax2.axis('off')
    draw_cell(ax2, 'Rb cell'); draw_B_field(ax2)
    chalk.chalk_text(ax2, 0.2, 4.0, 'pump', color=chalk.DIM, fontsize=10)
    chalk.chalk_text(ax2, 0.2, 3.6, 'off', color=chalk.DIM, fontsize=10)
    np.random.seed(77)
    for _ in range(10):
        sx = 1.8 + np.random.random() * 3.4
        sy = 2.3 + np.random.random() * 2.8
        angle = np.random.uniform(0, 2 * np.pi)
        chalk.chalk_arrow(ax2, sx, sy, sx + 0.2 * np.cos(angle),
                          sy + 0.2 * np.sin(angle),
                          color=chalk.YELLOW, lw=0.8, head=6)
    chalk.chalk_text(ax2, 2.5, 6.3, r'$\omega_L = \gamma |\mathbf{B}|$',
                     color=chalk.YELLOW, fontsize=11, style='normal')
    draw_bloch_inset(ax2, mx=np.sin(np.radians(80)), my=0,
                     mz=np.cos(np.radians(80)), x0=5.5, y0=0.0)
    chalk.chalk_text(ax2, 6.4, 0.0, r'$M_x(t) \sim \cos(\omega_L t)$',
                     color=chalk.RED, fontsize=8, style='normal')
    chalk.chalk_text(ax2, 0.5, 0.5, 'frequency encodes field',
                     color=chalk.WHITE, fontsize=10)

    # --- Panel 3: READ ---
    ax3 = board.panel(2, title='3.  read')
    ax3.set_xlim(-0.5, 8.5); ax3.set_ylim(-0.5, 7.5)
    ax3.set_aspect('equal'); ax3.axis('off')
    draw_cell(ax3); draw_B_field(ax3)
    chalk.chalk_arrow(ax3, 3.5, 0.0, 3.5, 2.0, color=chalk.BLUE, lw=3.0, head=18)
    chalk.chalk_text(ax3, 3.9, 0.3, 'probe', color=chalk.BLUE, fontsize=11)
    chalk.chalk_line(ax3, [3.1, 3.9], [1.3, 1.3], color=chalk.BLUE, lw=1.5)
    chalk.chalk_arrow(ax3, 3.5, 5.5, 3.5, 6.3, color=chalk.BLUE, lw=2.0, head=14)
    chalk.chalk_line(ax3, [3.15, 3.85], [5.8, 6.1], color=chalk.BLUE, lw=1.5)
    chalk.chalk_text(ax3, 4.1, 5.8, r'$\theta_F \propto M_x$',
                     color=chalk.BLUE, fontsize=9, style='normal')
    chalk.chalk_box(ax3, 2.8, 6.3, 1.4, 0.5, lw=1.0, pad=0.06)
    chalk.chalk_text(ax3, 3.5, 6.55, 'PD', fontsize=9,
                     ha='center', va='center', style='normal')
    chalk.chalk_line(ax3, [4.2, 5.0], [6.55, 6.55],
                     color=chalk.WHITE, lw=0.8, linestyle='--')
    sig_t = np.linspace(5.0, 8.0, 120)
    sig_y = 6.55 + 0.25 * np.cos(8 * (sig_t - 5.0)) * np.exp(-(sig_t - 5.0) * 0.4)
    ax3.plot(sig_t, sig_y, color=chalk.WHITE, linewidth=1.0, zorder=3)
    chalk.chalk_text(ax3, 5.8, 7.0, 'signal at $\\omega_L$',
                     color=chalk.WHITE, fontsize=9, style='normal')
    np.random.seed(99)
    for _ in range(10):
        sx = 1.8 + np.random.random() * 3.4
        sy = 2.3 + np.random.random() * 2.8
        angle = np.random.uniform(-0.5, 0.5)
        chalk.chalk_arrow(ax3, sx, sy, sx + 0.18 * np.cos(angle),
                          sy + 0.18 * np.sin(angle),
                          color=chalk.YELLOW, lw=0.8, head=6)
    chalk.chalk_text(ax3, 0.5, 0.5, 'measure $\\omega_L$, know $|B|$',
                     color=chalk.WHITE, fontsize=10, style='normal')
    chalk.chalk_text(ax3, 0.5, 0.0, r'$\delta B \sim 1/(\gamma \sqrt{n\, T_2})$',
                     color=chalk.DIM, fontsize=9, style='normal')

    board.save(out)
    board.close()
    return out
# illustrate-magnetometer ends here
