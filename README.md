## Install

Install the actual [MOC player/server](https://moc.daper.net/)

```
% sudo apt-get install -y moc

or

% brew install moc
% jackd -d coreaudio
```

> Note: if using a Mac, you need to run [jack](http://www.jackaudio.org/) in
> another terminal EVERY TIME (i.e. `jackd -d coreaudio`).

Verify that the MOC server can start

```
% mocp
```

> Press `q` to quit.

Install with `pip`
```
% pip3 install mocp-cli
```

## Optional Installs

### yt-helper

A lot of what powers the cool interactive features are provided by the
`COMMENTS` and `FILES` collections defined in `yt_helper`.

Install system av tools

```
% sudo apt-get install -y libav-tools sox rtmpdump

or

% brew install libav sox rtmpdump
```

Install with `pip`

```
% pip3 install yt-helper
```

### yt-search

In order to use the `yt-search` command (that was installed with `yt-helper`),
you must also install the `parse-helper` package and it's dependencies.

Install system requirements for `lxml`

```
% sudo apt-get install -y libxml2 libxslt1.1 libxml2-dev libxslt1-dev zlib1g-dev

or

% brew install libxml2
```

Install with `pip`

```
% pip3 install parse-helper
```

## Usage

The `mocplayer` script is provided

```
$ venv/bin/mocplayer --help
Usage: mocplayer [OPTIONS] [GLOB_PATTERNS]...

  Start a REPL to control music on console player (mocp)

Options:
  --help  Show this message and exit.
```

Calling `mocplayer` will start a REPL that will send commands to the running
instance of `mocp --server`. Any arguments passed to `mocplayer` are assumed to
be glob patterns that should be passed to the `moc.find_and_play` function.

```
% venv/bin/mocplayer
:docstrings to see all colon commands
:shortcuts to see all hotkeys

mocplayer> ?
 Loop forever, receiving character input from user and performing actions

    - ^d or ^c to break the loop
    - ':' to enter a command (and any arguments)
        - any method defined on GetCharLoop (or a sub-class) will be callable
          as a "colon command" (if its name does not start with '_')
        - the method for the `:command` should only accept `*args`
    - '-' to allow user to provide input that will be processed by the `input_hook`
    - '?' to show the class docstring(s) and the startup message

A wrapper to control moc (music on console) player with vim keybindings

:docstrings to see all colon commands
:shortcuts to see all hotkeys

mocplayer> :docstrings
.:: delete_comments ::.
Select comments/marks for currently playing file to delete

.:: docstrings ::.
Print/return the docstrings of methods defined on this class

.:: edit_timestamp ::.
Select comment/mark for currently playing file to edit the timestamp

.:: errors ::.
Print/return any colon commands that raised exceptions (w/ traceback)

.:: find ::.
Find and select audio files at specified glob patterns

.:: go ::.
Go to a particular timestamp

.:: history ::.
Print/return successful colon commands used

.:: ipython ::.
Start ipython shell. To continue back to the input loop, use 'ctrl + d'

.:: jump ::.
Jump to a saved comment/mark

.:: jumploop ::.
Loop an unbuffered input session, jumping between selected marks (up to 10)

.:: most_commented ::.
Select files that have been most commented and play

.:: pdb ::.
Start pdb (debugger). To continue back to the input loop, use 'c'

.:: recent_files ::.
Select files that were most recently added and play

.:: seek ::.
Seek forward or backward

.:: shortcuts ::.
Print/return any hotkey shortcuts defined on this class


mocplayer> :shortcuts
' ' -- pause/unpause
'i' -- show info about currently playing file
'm' -- mark the current timestamp
'c' -- show comments/marks (requires yt_helper package)
'C' -- select files that have been most commented and play (requires yt_helper package)
'R' -- select files that were most recently added and play (requires yt_helper package)
'J' -- jump to a saved comment or mark (requires yt_helper package)
'e' -- select comment/mark to edit timestamp (requires yt_helper package)
'd' -- select comments/marks to delete (requires yt_helper package)
'f' -- find and play audio files found in current directory
'F' -- find, select, and play audio files found in current directory
'q' -- quit
'Q' -- stop MOC server and quit
'n' -- next file in playlist
'p' -- previous file in playlist
'H' -- rewind 30 seconds
'h' -- rewind 5 seconds
'\x1b[D' -- rewind 1 second (left arrow)
'L' -- fast foward 30 seconds
'l' -- fast foward 5 seconds
'\x1b[C' -- fast foward 1 second (right arrow)
'j' -- lower volume
'\x1b[B' -- lower volume (down arrow)
'k' -- raise volume
'\x1b[A' -- raise volume (up arrow)

mocplayer> i
00:55 (55) of 43:03 into /tmp/Samurai_Champloo_-_Lofi_HipHop_Mix_Nujabes_inspired-kq7cQNO0gYc.mp3
mocplayer> :go 12:00
mocplayer> i
12:00 (720) of 43:03 into /tmp/Samurai_Champloo_-_Lofi_HipHop_Mix_Nujabes_inspired-kq7cQNO0gYc.mp3
mocplayer> :go 500
mocplayer> i
08:20 (500) of 43:03 into /tmp/Samurai_Champloo_-_Lofi_HipHop_Mix_Nujabes_inspired-kq7cQNO0gYc.mp3
mocplayer> :seek -45
mocplayer> i
07:42 (462) of 43:03 into /tmp/Samurai_Champloo_-_Lofi_HipHop_Mix_Nujabes_inspired-kq7cQNO0gYc.mp3
mocplayer> L
mocplayer> L
mocplayer> L
mocplayer> i
09:32 (572) of 43:03 into /tmp/Samurai_Champloo_-_Lofi_HipHop_Mix_Nujabes_inspired-kq7cQNO0gYc.mp3
```

