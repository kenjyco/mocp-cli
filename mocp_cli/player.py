import moc
import input_helper as ih
from os import remove
from functools import partial
from collections import OrderedDict
from chloop import GetCharLoop
from mocp_cli import logger
try:
    from yt_helper import AUDIO_COMMENTS as COMMENTS, FILES, get_real_basename
    if COMMENTS is None:
        raise ImportError

except ImportError:
    input_hook = None
    pre_input_hook = None

    def mark_it():
        logger.debug(moc.info_string('{currentsec} seconds into {file}'))

    def get_comments(**kwargs):
        pass

    def show_comments(**kwargs):
        #
        # Maybe try to grep for `moc.get_info_dict().get('file')` in logger file
        #
        pass

    def select_comments(**kwargs):
        pass

    def jump_to_select():
        pass

    def jumploop(**kwargs):
        pass

    def get_paths_from_basenames(*args):
        pass

    def play_basenames(*args):
        pass

    def delete(**kwargs):
        pass

    def recent_files_play_select(**kwargs):
        pass

    def most_commented_files_play_select(**kwargs):
        pass

    def edit_comment_timestamp_select():
        pass

    def delete_comments_select():
        pass
else:
    def get_current_basename():
        """Return basename of current playing file"""
        return get_real_basename(moc.get_info_dict().get('file'))

    def input_hook(**kwargs):
        basename = get_current_basename()
        COMMENTS.add(
            basename=basename,
            **kwargs
        )

    def pre_input_hook():
        return {
            'timestamp': moc.get_info_dict().get('currentsec')
        }

    def mark_it():
        input_hook(text='mark', **pre_input_hook())

    def get_comments(**kwargs):
        """Get comments for current file playing

        - kwargs: passed to `COMMENTS.find`
            - if no 'item_format' or 'get_fields' passed in, use `all_fields=True`
            - if no 'ts_fmt' or 'ts_tz' passed in, and 'include_meta=False' not
              passed in use `admin_fmt=True`
        """
        if 'ts_fmt' not in kwargs and 'ts_tz' not in kwargs:
            if 'include_meta' in kwargs and kwargs.get('include_meta') is True:
                kwargs['admin_fmt'] = True
        if 'item_format' not in kwargs and 'get_fields' not in kwargs:
            kwargs['all_fields'] = True
        basename = get_current_basename()
        return COMMENTS.find(
            'basename:{}'.format(basename),
            **kwargs
        )

    def show_comments(item_format=' - {timestamp} -> {text} .::. {_ts}', admin_fmt=True, **kwargs):
        """Show comments for current file playing

        - item_format: passed along to `COMMENTS.find` via `get_comments` func
        - admin_fmt: passed along to `COMMENTS.find` via `get_comments` func
        - kwargs: also passed along to `COMMENTS.find` via `get_comments` func
        """
        print('\n'.join(get_comments(item_format=item_format, admin_fmt=admin_fmt, **kwargs)))


    def select_comments(item_format='{timestamp} -> {text}',
                        prompt='Select mark/comment', unbuffered=None, **kwargs):
        """Select comments for current file playing

        - item_format: passed along to ih.make_selections func
        - prompt: passed along to ih.make_selections func
        - unbuffered: if False is explicitly passed in, don't use unbuffered
          when number of comments is less than 62
        - kwargs: passed along to `COMMENTS.find` via `get_comments` func
            - if no 'post_fetch_sort_key' passed in, use
              `post_fetch_sort_key='timestamp', sort_key_default_val=0`
            - if no 'limit' pass in, use 75 by default
        """
        if 'post_fetch_sort_key' not in kwargs:
            kwargs.update({
                'post_fetch_sort_key': 'timestamp',
                'sort_key_default_val': 0
            })

        if 'limit' not in kwargs:
            kwargs.update({'limit': 75})

        comments = get_comments(**kwargs)
        if unbuffered is None:
            if len(comments) > 62:
                unbuffered = False
            else:
                unbuffered = True

        return ih.make_selections(
            comments,
            item_format=item_format,
            prompt=prompt,
            wrap=False,
            unbuffered=unbuffered
        )

    def jump_to_select():
        """Use select_comments to select a mark/comment for the current file

        Jump immediately to timestamp and prompt for a note if the mark has no note
        """
        selected = select_comments()
        if selected:
            moc.go(selected[0]['timestamp'])
            if selected[0]['text'] in ('mark', ''):
                comment = ih.user_input_fancy('note for mark')
                if comment != {'text': ''}:
                    COMMENTS.update(
                        selected[0]['_id'],
                        **comment
                    )

    def jumploop(choose_all=False):
        """Loop an unbuffered input session, jumping between selected marks (up to 62)"""
        num_comments = get_comments(count=True)
        if choose_all:
            selected = get_comments(
                post_fetch_sort_key='timestamp',
                sort_key_default_val=0
            )
        else:
            selected = select_comments(
                prompt='Select up to 62 comments for jumploop (or type "all")',
                unbuffered=False,
                get_fields='text,timestamp',
                include_meta=False
            )
        if selected:
            basename = get_current_basename()
            selected = selected[:62]
            while True:
                print('\n{}\n'.format(basename))
                try:
                    idx = ih.make_selections(
                        selected,
                        item_format='{timestamp} -> {text}',
                        prompt='Select mark/comment or ctrl+c to break loop',
                        wrap=False,
                        unbuffered=True,
                        raise_interrupt=True,
                        raise_exception_chars=[' ']
                    )
                    if idx:
                        if basename not in moc.info_string():
                            play_basenames(basename)
                            moc.go(idx[0]['timestamp'])
                        else:
                            moc.go(idx[0]['timestamp'])
                except KeyboardInterrupt:
                    print()
                    break
                except Exception:
                    moc.toggle_pause()

    def get_paths_from_basenames(*basenames):
        """Return a list of path globs for basenames (determined from FILES)"""
        return [
            '{}/{}*'.format(FILES[basename].get('dirname', ''), basename)
            for basename in basenames
        ]

    def play_basenames(*basenames):
        """Use FILES to generate path globs to basenames and play"""
        paths = get_paths_from_basenames(*basenames)
        if paths:
            moc.find_and_play(*paths)

    def delete(basename=None):
        """Delete audio file and remove related data from COMMENTS

        In FILES, the item will be updated to 'audio=False' in case there is a
        related video file of the same name (which this will not delete)
        """
        if basename is None:
            basename = get_current_basename()
            if not basename:
                return
        paths = get_paths_from_basenames(basename)
        if paths:
            files = moc.find_audio(*paths)
            if files:
                file_id = FILES[basename].get('_id')
                comment_ids = [
                    x['_id']
                    for x in COMMENTS.find('basename:{}'.format(basename), get_fields='_id')
                ]
                print('For {}, found {} file(s) and {} comment(s)'.format(
                    repr(basename),
                    len(files),
                    len(comment_ids)
                ))
                yn = ih.user_input('\nAre you sure you want to delete? (y/n)')
                if yn.lower().startswith('y'):
                    for f in files:
                        try:
                            remove(f.strip('\'"'))
                        except Exception as e:
                            logger.error('Could not delete {}... {}'.format(repr(f), repr(e)))
                        else:
                            logger.info('Deleted {}'.format(repr(f)))
                    if file_id:
                        FILES.update(file_id, audio=False)
                    if comment_ids:
                        COMMENTS.delete_many(*comment_ids)

    def recent_files_play_select(limit=62):
        """Select files that were most recently added and play"""
        selected = ih.make_selections(
            FILES.find('audio:True', get_fields='basename', admin_fmt=True, limit=limit),
            item_format='{basename} .::. {_ts}',
            prompt='Select basenames to play',
            wrap=False
        )
        if selected:
            play_basenames(*[x['basename'] for x in selected])

    def most_commented_files_play_select(limit=62):
        """Select files that have been most commented and play"""
        selected = ih.make_selections(
            COMMENTS.top_values_for_index('basename', limit=limit),
            prompt='Select basenames to play',
            item_format='{} ({})',
            wrap=False
        )
        if selected:
            play_basenames(*[s[0] for s in selected])

    def edit_comment_timestamp_select():
        """Use select_comments to select a mark/comment for the current file

        Prompt for a new timestamp (usually +/-1 from current timestamp)
        """
        selected = select_comments(prompt='Select mark/comment to edit timestamp')
        if selected:
            prompt = 'Enter new timestamp (old was {})'.format(selected[0].get('timestamp', ''))
            timestamp = ih.user_input(prompt)
            if timestamp:
                try:
                    timestamp = int(timestamp)
                except ValueError:
                    print('{} is not an integer'.format(timestamp))
                else:
                    _id = selected[0]['_id']
                    COMMENTS.update(_id, timestamp=timestamp)
        else:
            print()

    def delete_comments_select():
        """Use COMMENTS.select_and_modify to choose which comments to delete
        """
        basename = get_current_basename()
        return COMMENTS.select_and_modify(
            action='delete',
            terms='basename:{}'.format(basename),
            prompt='Select comments to delete (separate by space)',
            menu_item_format='{timestamp} -> {text} .::. {_ts}'
        )


chfunc = OrderedDict([
    (' ', (moc.toggle_pause, 'pause/unpause')),
    ('i', (lambda: print(moc.info_string()), 'show info about currently playing file')),
    ('m', (mark_it, 'mark the current timestamp')),
    ('c', (show_comments, 'show comments/marks (requires yt_helper package)')),
    ('C', (most_commented_files_play_select, 'select files that have been most commented and play (requires yt_helper package)')),
    ('R', (recent_files_play_select, 'select files that were most recently added and play (requires yt_helper package)')),
    ('J', (jump_to_select, 'jump to a saved comment or mark (requires yt_helper package)')),
    ('\x01', (partial(jumploop, choose_all=True), 'start jumploop session with first 62 marks selected (requires yt_helper package)')),
    ('e', (edit_comment_timestamp_select, 'select comment/mark to edit timestamp (requires yt_helper package)')),
    ('d', (delete_comments_select, 'select comments/marks to delete (requires yt_helper package)')),
    ('D', (delete, 'delete current playing file from filesystem and remove from FILES/COMMENTS (requires yt_helper package)')),
    ('f', (partial(moc.find_and_play, '.'), 'find and play audio files found in current directory')),
    ('F', (partial(moc.find_select_and_play, '.'), 'find, select, and play audio files found in current directory')),
    ('q', (lambda: None, 'quit')),
    ('Q', (moc.stop_server, 'stop MOC server and quit')),
    ('n', (moc.next, 'next file in playlist')),
    ('p', (moc.previous, 'previous file in playlist')),
    ('H', (partial(moc.seek, -30), 'rewind 30 seconds')),
    ('h', (partial(moc.seek, -5), 'rewind 5 seconds')),
    ('\x1b[D', (partial(moc.seek, -1), 'rewind 1 second')),
    ('L', (partial(moc.seek, 30), 'fast foward 30 seconds')),
    ('l', (partial(moc.seek, 5), 'fast foward 5 seconds')),
    ('\x1b[C', (partial(moc.seek, 1), 'fast foward 1 second')),
    ('j', (moc.volume_down, 'lower volume')),
    ('\x1b[B', (moc.volume_down, 'lower volume')),
    ('k', (moc.volume_up, 'raise volume')),
    ('\x1b[A', (moc.volume_up, 'raise volume')),
])


class _Player(GetCharLoop):
    """A wrapper to control moc (music on console) player with vim keybindings"""
    def seek(self, num):
        """Seek forward or backward"""
        moc.seek(int(num))

    def go(self, timestamp):
        """Go to a particular timestamp"""
        moc.go(timestamp)

    def jump(self):
        """Jump to a saved comment or mark"""
        jump_to_select()

    def jumploop(self):
        """Loop an unbuffered input session, jumping between selected marks (up to 62)"""
        jumploop()

    def most_commented(self, limit=62):
        """Select files that have been most commented and play (up to 62)"""
        most_commented_files_play_select(int(limit))

    def recent_files(self, limit=62):
        """Select files that were most recently added and play (up to 62)"""
        recent_files_play_select(int(limit))

    def delete_comments(self):
        """Select comments/marks for currently playing file to delete"""
        delete_comments_select()

    def delete(self):
        """Delete current audio file and remove related data from COMMENTS"""
        delete()

    def edit_timestamp(self):
        """Select comment/mark for currently playing file to edit the timestamp"""
        edit_comment_timestamp_select()

    def find(self, *glob_patterns):
        """Find and select audio files at specified glob patterns"""
        moc.find_select_and_play(*glob_patterns)


Player = _Player(chfunc_dict=chfunc, name='mocp', prompt='mocplayer> ',
                 input_hook=input_hook, pre_input_hook=pre_input_hook,
                 break_chars=['q', 'Q'])
