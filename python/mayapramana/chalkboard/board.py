"""
Chalkboard — the drawing surface for MāyaPramāṇa illustrations.

Models the large sliding chalkboards in physics lecture halls:
a wooden frame holding N vertically-sliding panels. The rightmost
panel has a permanent square grid (like the graph-paper section of
a real lecture board). A chalk tray runs along the bottom.

Usage
-----
    from mayapramana.chalkboard import Chalkboard

    board = Chalkboard(panels=2)          # two sliding panels
    ax = board.panel(0)                   # get axes for left panel
    ax.plot(...)                          # draw with matplotlib
    board.panel(0, title='Setup')         # optional panel title
    board.save('figure.png')
    board.close()

The permanent grid, chalk tray, frame, and dust are drawn
automatically.  All coordinates within a panel are in the panel's
own data space — set xlim/ylim as you would on any axes.
"""

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

from . import chalk


# --- Layout constants (figure-fraction coordinates) ---

# Vertical layout: frame top | panels | tray | frame bottom
_FRAME_TOP = 0.97
_PANEL_TOP = 0.93
_PANEL_BOT = 0.12
_TRAY_TOP = 0.11
_TRAY_BOT = 0.04
_FRAME_BOT = 0.00

# Horizontal: frame left | panels | frame right
_FRAME_LEFT = 0.02
_FRAME_RIGHT = 0.98
_PANEL_GAP = 0.02  # gap between adjacent panels


class Chalkboard:
    """A physics lecture hall chalkboard with sliding panels."""

    def __init__(self, panels=1, figsize=None, dpi=180,
                 grid_spacing=None, grid_panels=None,
                 panel_weights=None, title=None):
        """
        Parameters
        ----------
        panels : int
            Number of side-by-side sliding panels (1-4).
        figsize : tuple, optional
            Figure size in inches.  Default uses 5:3 aspect ratio,
            width scaling with panel count.
        dpi : int
            Resolution for saved figures.
        grid_spacing : float, optional
            Grid square size as a fraction of panel height.
            Default 0.05 (≈20 squares vertically).
        grid_panels : set of int, optional
            Which panels get the permanent grid.
            Default: {last panel only} — the graph-paper section.
        panel_weights : list of float, optional
            Relative widths of the panels.  Default for 2 panels:
            [3, 2] — the drawing area is 50% wider than the plot.
        title : str, optional
            Title written on the frame above the panels.
        """
        if panels < 1 or panels > 4:
            raise ValueError("panels must be 1-4")

        self.n_panels = panels
        self.dpi = dpi
        self._grid_spacing = grid_spacing or 0.05
        self._grid_panels = grid_panels if grid_panels is not None else {panels - 1}

        if panel_weights is None:
            if panels == 1:
                panel_weights = [1]
            elif panels == 2:
                panel_weights = [3, 2]  # 60/40 — schematic gets more room
            else:
                panel_weights = [1] * panels
        self._panel_weights = panel_weights

        if figsize is None:
            # 5:3 overall aspect — wide like a real lecture board
            w = 7 * panels
            h = w * 3 / 5
            figsize = (w, h)

        self.fig = plt.figure(figsize=figsize)
        self.fig.patch.set_facecolor(chalk.BOARD_EDGE)

        self._axes = []
        self._draw_frame(title)
        self._draw_panels()
        self._draw_tray()
        chalk.chalk_dust_particles(self.fig, n=50)

    # --- Public API ---

    def panel(self, index, title=None):
        """Return the matplotlib Axes for panel *index*.

        Optionally set a chalk title at the top of the panel.
        """
        ax = self._axes[index]
        if title is not None:
            # Place title in panel coordinates, near the top
            ax.set_title(title, fontsize=13, color=chalk.WHITE,
                         fontfamily='serif', style='italic', pad=8)
        return ax

    def save(self, path, **kwargs):
        """Save the figure to *path*."""
        defaults = dict(
            dpi=self.dpi,
            facecolor=self.fig.get_facecolor(),
            bbox_inches='tight',
            pad_inches=0.2,
        )
        defaults.update(kwargs)
        self.fig.savefig(path, **defaults)

    def close(self):
        plt.close(self.fig)

    # --- Private: frame, panels, tray ---

    def _draw_frame(self, title):
        """Draw the wooden frame around the board."""
        frame_color = chalk.BOARD_EDGE

        # Top bar
        self.fig.patches.append(patches.FancyBboxPatch(
            (_FRAME_LEFT, _PANEL_TOP), _FRAME_RIGHT - _FRAME_LEFT, _FRAME_TOP - _PANEL_TOP,
            boxstyle='square,pad=0',
            facecolor=frame_color, edgecolor='none',
            transform=self.fig.transFigure, zorder=0,
        ))

        if title:
            self.fig.text(
                (_FRAME_LEFT + _FRAME_RIGHT) / 2, (_PANEL_TOP + _FRAME_TOP) / 2,
                title, fontsize=15, color=chalk.DIM,
                ha='center', va='center', fontfamily='serif', style='italic',
            )

    def _draw_panels(self):
        """Create panel axes; grid only on panels in _grid_panels."""
        total_width = _FRAME_RIGHT - _FRAME_LEFT
        gap_total = _PANEL_GAP * (self.n_panels - 1)
        usable = total_width - gap_total
        panel_h = _PANEL_TOP - _PANEL_BOT

        # Normalise weights to fractions of usable width
        wsum = sum(self._panel_weights)
        widths = [w / wsum * usable for w in self._panel_weights]

        left = _FRAME_LEFT
        for i in range(self.n_panels):
            pw = widths[i]
            ax = self.fig.add_axes([left, _PANEL_BOT, pw, panel_h])
            self._style_panel(ax)
            if i in self._grid_panels:
                self._draw_grid(ax)
            self._axes.append(ax)
            left += pw + _PANEL_GAP

    def _style_panel(self, ax):
        """Apply chalkboard styling to a panel axes."""
        ax.set_facecolor(chalk.BOARD)
        ax.tick_params(colors=chalk.DIM, labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(chalk.DIM)
            spine.set_linewidth(0.5)

    def _draw_grid(self, ax):
        """Draw the permanent square grid on a panel.

        Lines are drawn in axes-fraction coordinates (0-1) so they
        persist regardless of data xlim/ylim changes.
        """
        gs = self._grid_spacing
        trans = ax.transAxes
        # Vertical lines
        x = gs
        while x < 1.0:
            ax.plot([x, x], [0, 1], color=chalk.GRID_LINE,
                    linewidth=0.4, zorder=0, transform=trans,
                    clip_on=False)
            x += gs
        # Horizontal lines
        y = gs
        while y < 1.0:
            ax.plot([0, 1], [y, y], color=chalk.GRID_LINE,
                    linewidth=0.4, zorder=0, transform=trans,
                    clip_on=False)
            y += gs

    def _draw_tray(self):
        """Draw the chalk tray with coloured chalks and a duster."""
        tray_h = _TRAY_TOP - _TRAY_BOT
        tray_w = _FRAME_RIGHT - _FRAME_LEFT

        # Tray shelf (wood)
        self.fig.patches.append(patches.FancyBboxPatch(
            (_FRAME_LEFT, _TRAY_BOT), tray_w, tray_h,
            boxstyle='round,pad=0.003',
            facecolor=chalk.TRAY_WOOD, edgecolor=chalk.TRAY_EDGE,
            linewidth=1.5,
            transform=self.fig.transFigure, zorder=5,
        ))

        # Chalk sticks — saturated body colours, not board-mark colours
        colors = list(chalk.STICK_SET.values())
        n_chalks = len(colors)
        chalk_region_left = _FRAME_LEFT + 0.04
        chalk_region_right = _FRAME_LEFT + 0.04 + 0.06 * n_chalks
        chalk_y = _TRAY_BOT + tray_h * 0.30
        chalk_h = tray_h * 0.35
        chalk_w = 0.035

        for i, col in enumerate(colors):
            cx = chalk_region_left + i * 0.06
            # Slight random tilt for hand-placed look
            angle = np.random.uniform(-5, 5)
            stick = patches.FancyBboxPatch(
                (cx, chalk_y), chalk_w, chalk_h,
                boxstyle='round,pad=0.002',
                facecolor=col, edgecolor='none',
                linewidth=0, alpha=0.9,
                transform=self.fig.transFigure, zorder=6,
            )
            self.fig.patches.append(stick)

        # Duster — a wider block to the right
        duster_x = _FRAME_RIGHT - 0.12
        duster_w = 0.08
        duster_y = _TRAY_BOT + tray_h * 0.08
        duster_h = tray_h * 0.55

        # Felt pad
        felt = patches.FancyBboxPatch(
            (duster_x, duster_y), duster_w, duster_h,
            boxstyle='round,pad=0.003',
            facecolor=chalk.DUSTER_FELT, edgecolor=chalk.DUSTER_WOOD,
            linewidth=1.0,
            transform=self.fig.transFigure, zorder=6,
        )
        self.fig.patches.append(felt)

        # Wood handle on top of felt
        handle_h = duster_h * 0.35
        handle = patches.FancyBboxPatch(
            (duster_x + 0.005, duster_y + duster_h - handle_h),
            duster_w - 0.01, handle_h,
            boxstyle='round,pad=0.002',
            facecolor=chalk.DUSTER_WOOD, edgecolor='none',
            linewidth=0,
            transform=self.fig.transFigure, zorder=7,
        )
        self.fig.patches.append(handle)

        # Dust smear on felt
        for _ in range(15):
            dx = np.random.uniform(duster_x, duster_x + duster_w)
            dy = np.random.uniform(duster_y, duster_y + duster_h * 0.6)
            self.fig.patches.append(plt.Circle(
                (dx, dy), np.random.uniform(0.002, 0.005),
                transform=self.fig.transFigure,
                facecolor=chalk.CHALK_DUST, alpha=0.2,
                edgecolor='none', zorder=7,
            ))
