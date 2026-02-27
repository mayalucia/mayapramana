"""
MāyaPramāṇa chalkboard — physics lecture hall illustrations.

    from mayapramana.chalkboard import Chalkboard, chalk

    board = Chalkboard(panels=2)
    ax = board.panel(0, title='Setup')
    chalk.chalk_text(ax, 1, 8, 'Hello from the board')
    board.save('figure.png')
    board.close()
"""

from .board import Chalkboard
from . import chalk

__all__ = ['Chalkboard', 'chalk']
