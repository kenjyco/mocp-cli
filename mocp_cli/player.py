import moc
import input_helper as ih
from functools import partial
from collections import OrderedDict
from chloop import GetCharLoop


chfunc = OrderedDict([
    (' ', (moc.toggle_pause, 'pause/unpause')),
    ('i', (lambda: print(moc.info_string()), 'show info about currently playing file')),
    ('n', (moc.next, 'next file in playlist')),
    ('p', (moc.previous, 'previous file in playlist')),
    ('H', (partial(moc.seek, -30), 'rewind 30 seconds')),
    ('h', (partial(moc.seek, -5), 'rewind 5 seconds')),
    ('\x1b[D', (partial(moc.seek, -1), 'rewind 1 second (left arrow)')),
    ('L', (partial(moc.seek, 30), 'fast foward 30 seconds')),
    ('l', (partial(moc.seek, 5), 'fast foward 5 seconds')),
    ('\x1b[C', (partial(moc.seek, 1), 'fast foward 1 second (right arrow)')),
    ('j', (moc.volume_down, 'lower volume')),
    ('\x1b[B', (moc.volume_down, 'lower volume (down arrow)')),
    ('k', (moc.volume_up, 'raise volume')),
    ('\x1b[A', (moc.volume_up, 'raise volume (up arrow)')),
])


class _Player(GetCharLoop):
    """A wrapper to control moc (music on console) player with vim keybindings"""
    def seek(self, num):
        """Seek forward or backward"""
        moc.seek(int(num))

    def go(self, timestamp):
        """Jump to a particular timestamp"""
        moc.go(timestamp)


Player = _Player(chfunc_dict=chfunc, name='mocp', prompt='mocplayer> ')
