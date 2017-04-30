import moc
import input_helper as ih
from functools import partial
from chloop import GetCharLoop


chfunc = {
    'H': (partial(moc.seek, -30), 'rewind 30 seconds'),
    'h': (partial(moc.seek, -5), 'rewind 5 seconds'),
    '\x1b[D': (partial(moc.seek, -1), '(left arrow) rewind 1 second'),
    'L': (partial(moc.seek, 30), 'fast foward 30 seconds'),
    'l': (partial(moc.seek, 5), 'fast foward 5 seconds'),
    '\x1b[C': (partial(moc.seek, 1), '(right arrow) fast foward 1 second'),
    ' ': (moc.toggle_pause, 'pause/unpause'),
    'i': (lambda: print(moc.info_string()), 'show info about currently playing file'),
    'n': (moc.next, 'next file in playlist'),
    'p': (moc.previous, 'previous file in playlist'),
    'j': (moc.volume_down, 'lower volume'),
    '\x1b[B': (moc.volume_down, '(down arrow) lower volume'),
    'k': (moc.volume_up, 'raise volume'),
    '\x1b[A': (moc.volume_up, '(up arrow) raise volume'),
}


class _Player(GetCharLoop):
    def seek(self, num):
        """Seek forward or backward"""
        moc.seek(int(num))

    def go(self, timestamp):
        """Jump to a particular timestamp"""
        moc.go(timestamp)


Player = _Player(chfunc_dict=chfunc, name='mocp', prompt='mocplayer> ')
