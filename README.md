#### Install

```
% pip install mocp-cli
```

#### Usage

Calling `mocplayer` will start a REPL that will send commands to the running
instance of `mocp --server`. Any arguments passed to `mocplayer` are assumed to
be glob patterns that should be passed to the `moc.find_and_play` function.

```
% mocplayer
mocplayer> :docstrings
======================================================================
Loop forever, receiving character input from user and performing actions

    - ^d or ^c to break the loop
    - ':' to enter a command (and any arguments)
        - the name of the command should be monkeypatched on the GetCharLoop
          instance, or be a defined method on a GetCharLoop sub-class
        - the function bound to `:command` should accept `*args` only
    - '-' to receive an input line from user (a note)

.:: docstrings ::.
Print/return the docstrings of methods defined on this class

.:: errors ::.
Print/return any colon commands that raised exceptions (w/ traceback)

.:: go ::.
Jump to a particular timestamp

.:: history ::.
Print/return successful colon commands used

.:: ipython ::.
Start ipython shell. To continue back to the input loop, use 'ctrl + d'

.:: pdb ::.
Start pdb (debugger). To continue back to the input loop, use 'c'

.:: seek ::.
Seek forward or backward

.:: shortcuts ::.
Print/return any hotkey shortcuts defined on this class


mocplayer> :shortcuts
'\x1b[A' -- (up arrow) raise volume
'\x1b[B' -- (down arrow) lower volume
'\x1b[C' -- (right arrow) fast foward 1 second
'\x1b[D' -- (left arrow) rewind 1 second
' ' -- pause/unpause
'H' -- rewind 30 seconds
'L' -- fast foward 30 seconds
'h' -- rewind 5 seconds
'i' -- show info about currently playing file
'j' -- lower volume
'k' -- raise volume
'l' -- fast foward 5 seconds
'n' -- next file in playlist
'p' -- previous file in playlist

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

