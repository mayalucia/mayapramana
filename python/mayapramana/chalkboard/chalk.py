"""
Chalk colours and drawing helpers.

The palette comes from Caltech/Fermilab-era lecture boards:
dark green surface, white/yellow/red/blue chalk, dim grid lines.
"""

import numpy as np

# --- Board surface ---
BOARD = '#2a4a2a'
BOARD_EDGE = '#1a3a1a'
GRID_LINE = '#3a5a3a'

# --- Chalk colours ---
WHITE = '#e8e4d4'
DIM = '#a8a498'
YELLOW = '#e8d878'
RED = '#d88878'
BLUE = '#88b8d8'
GREEN = '#88d8a8'
ORANGE = '#d8a868'

# Named chalk set (for the tray)
CHALK_SET = {
    'white': WHITE,
    'dim': DIM,
    'yellow': YELLOW,
    'red': RED,
    'blue': BLUE,
    'green': GREEN,
    'orange': ORANGE,
}

# --- Chalk stick body colours (more saturated than marks on the board) ---
STICK_SET = {
    'white': '#f0ece0',
    'dim': '#c0b8a8',
    'yellow': '#e8d040',
    'red': '#d05040',
    'blue': '#4088c0',
    'green': '#40b070',
    'orange': '#d08830',
}

# --- Tray and duster colours ---
TRAY_WOOD = '#5a3a1a'
TRAY_EDGE = '#3a2a10'
DUSTER_FELT = '#6a5a4a'
DUSTER_WOOD = '#7a5a3a'
CHALK_DUST = DIM


def chalk_text(ax, x, y, text, color=WHITE, fontsize=11, **kwargs):
    """Place chalk-style text on an axes.

    Defaults to serif italic — the Feynman lecture hand.
    """
    defaults = dict(
        fontfamily='serif',
        style='italic',
        ha='left',
        va='baseline',
    )
    defaults.update(kwargs)
    return ax.text(x, y, text, fontsize=fontsize, color=color, **defaults)


def chalk_arrow(ax, x0, y0, x1, y1, color=WHITE, lw=2.0, head=15):
    """Draw a chalk arrow from (x0,y0) to (x1,y1)."""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='->', color=color,
                                lw=lw, mutation_scale=head))


def chalk_line(ax, xs, ys, color=WHITE, lw=1.2, **kwargs):
    """Draw a chalk line through a sequence of points."""
    ax.plot(xs, ys, color=color, linewidth=lw, **kwargs)


def chalk_box(ax, x, y, w, h, color=WHITE, lw=1.5, pad=0.15):
    """Draw a chalk rounded rectangle."""
    import matplotlib.patches as patches
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f'round,pad={pad}',
        facecolor='none', edgecolor=color,
        linewidth=lw,
    )
    ax.add_patch(box)
    return box


def chalk_circle(ax, x, y, r, color=WHITE, lw=1.0, fill=False):
    """Draw a chalk circle."""
    import matplotlib.pyplot as plt
    c = plt.Circle((x, y), r, fill=fill,
                   facecolor='none' if not fill else color,
                   edgecolor=color, linewidth=lw)
    ax.add_patch(c)
    return c


def chalk_dust_particles(fig, n=40, color=CHALK_DUST, alpha=0.15):
    """Scatter chalk dust along the bottom edge of the figure."""
    import matplotlib.pyplot as plt
    for _ in range(n):
        cx = np.random.uniform(0.05, 0.95)
        cy = np.random.uniform(0.01, 0.04)
        r = np.random.uniform(0.001, 0.003)
        fig.patches.append(plt.Circle(
            (cx, cy), r,
            transform=fig.transFigure,
            facecolor=color, alpha=alpha,
            edgecolor='none',
        ))
