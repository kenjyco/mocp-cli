import moc
import input_helper as ih
from functools import partial
from collections import OrderedDict
from chloop import GetCharLoop
from mocp_cli import logger
try:
    from yt_helper import COMMENTS, get_real_basename
    if COMMENTS is None:
        raise ImportError

except ImportError:
    input_hook = None

    def mark_it():
        logger.debug(moc.info_string('{currentsec} seconds into {file}'))

    def show_comments():
        #
        # Maybe try to grep for `moc.get_info_dict().get('file')` in logger file
        #
        pass
else:
    def input_hook(**kwargs):
        basename = get_real_basename(moc.get_info_dict().get('file'))
        COMMENTS.add(
            basename=basename,
            **kwargs
        )

    def mark_it():
        input_hook(text='mark', **pre_input_hook())

    def show_comments():
        basename = get_real_basename(moc.get_info_dict().get('file'))
        print('\n'.join(COMMENTS.find(
            'basename:{}'.format(basename),
            item_format=' - {timestamp} -> {text}'
        )))


def pre_input_hook():
    return {
        'timestamp': moc.get_info_dict().get('currentsec')
    }


chfunc = OrderedDict([
    (' ', (moc.toggle_pause, 'pause/unpause')),
    ('i', (lambda: print(moc.info_string()), 'show info about currently playing file')),
    ('c', (show_comments, 'show comments/marks (requires yt_helper package)')),
    ('m', (mark_it, 'mark the current timestamp')),
    ('q', (lambda: None, 'quit')),
    ('Q', (moc.stop_server, 'stop MOC server and quit')),
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


Player = _Player(chfunc_dict=chfunc, name='mocp', prompt='mocplayer> ',
                 input_hook=input_hook, pre_input_hook=pre_input_hook,
                 break_chars=['q', 'Q'])
