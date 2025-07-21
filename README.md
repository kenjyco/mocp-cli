A sophisticated interactive music player built on MOC (Music on Console) and the [chloop](https://github.com/kenjyco/chloop) REPL framework that transforms audio listening into an intelligent, annotated experience. This library provides vim-style keyboard controls, timestamp marking, and persistent comment storage to help users deeply engage with audio content.

The core philosophy centers on **active listening workflows** where users can mark interesting moments, add contextual notes, and build searchable audio archives over time. Whether analyzing podcasts, studying music, reviewing recordings, or conducting audio research, mocp-cli reduces the mental overhead of navigating complex audio files by making annotation and navigation effortless.

The library integrates seamlessly with Redis-based data storage and the broader helper library ecosystem, enabling powerful audio workflow automation and cross-session persistence.

## Install

Install the actual [MOC player/server](https://moc.daper.net/)

```
sudo apt-get install -y moc
```

or

```
brew install moc
```

If you **don't have [docker](https://docs.docker.com/get-docker) installed**,
install Redis and start server

```
sudo apt-get install -y redis-server
```

or

```
brew install redis
brew services start redis
```

Install with `pip`

```
pip install mocp-cli
```

### Optional Install yt-helper

A lot of what powers the cool interactive features are provided by the `COMMENTS` and `FILES` `redis_helper.Collections` defined in `yt_helper`.

Install with `pip`

```
pip install yt-helper
```

or

```
pip install "mocp-cli[extras]"
```

## QuickStart

Calling `mocplayer` will start a REPL that will send commands to the running instance of `mocp --server`. Any arguments passed to `mocplayer` are assumed to be glob patterns that should be passed to the `moc.find_select_and_play` function.

```bash
# Start the interactive player with audio files
mocplayer ~/Music/*.mp3

# Or start with a specific directory
mocplayer ~/Podcasts/
```

**Basic Controls:**
- `space` - pause/unpause
- `m` - mark current timestamp for later reference
- `c` - show all comments/marks for current file
- `i` - show info about currently playing file
- `n` - next file in playlist
- `p` - previous file in playlist
- `h`/`l` - seek backward/forward (5 seconds)
- `H`/`L` - seek backward/forward (30 seconds)
- `←`/`→` - seek backward/forward (1 second, arrow keys)
- `j`/`k` - volume down/up
- `↓`/`↑` - volume down/up (arrow keys)
- `f` - find and play audio files in current directory
- `F` - find, select, and play audio files in current directory
- `-` - add timestamped comment with custom text
- `q` - quit
- `Q` - stop MOC server and quit

**Advanced Features:**
- `J` - jump to a previously saved mark
- `C` - browse and play most-commented files
- `R` - browse and play recently added files
- `Ctrl+a` - start jumploop with first 62 marks selected
- `e` - edit timestamp of existing comment/mark
- `d` - delete selected comments/marks
- `D` - delete current file and remove all associated data

**Colon Commands:**
- `:seek N` - seek forward/backward by N seconds
- `:go timestamp` - jump to specific timestamp (e.g., `:go 1h23m45s`, `:go 2:15:30`)
- `:jump` - jump to a saved comment or mark (same as `J`)
- `:jumploop` - start interactive mark navigation session
- `:most_commented [limit]` - browse most-commented files (default limit 62)
- `:recent_files [limit]` - browse recently added files (default limit 62)
- `:delete_comments` - select comments/marks to delete
- `:delete` - delete current file and associated data
- `:edit_timestamp` - edit timestamp of existing comment/mark
- `:find pattern1 pattern2` - find and select files by glob patterns

**What you gain:** Transform passive audio consumption into an active, searchable knowledge base. Mark key moments while listening, add contextual notes, and build a personal audio archive that becomes more valuable over time. Never lose track of important audio moments again.

## API Overview

### Interactive Player Interface

#### Core Player Class
- **`Player`** - Main interactive REPL for controlling MOC player with vim-style keybindings
  - Inherits from `GetCharLoop` for single-keystroke efficiency
  - `chfunc_dict`: Ordered dictionary mapping keys to (function, help_text) tuples
  - `name`: Collection name for Redis storage ('mocp')
  - `prompt`: Display prompt ('mocplayer> ')
  - `input_hook`: Function to handle timestamped comments via `-` input
  - `pre_input_hook`: Function to capture current timestamp context
  - `break_chars`: Characters that exit the loop (['q', 'Q'])
  - Returns: Interactive session (call with `Player()` to start)
  - Internal calls: `GetCharLoop.__init__()`, moc module functions, COMMENTS collection

### Player Control Methods (Colon Commands)

#### Navigation and Seeking
- **`seek(num)`** - Seek forward or backward by specified seconds
  - `num`: Number of seconds to seek (positive=forward, negative=backward)
  - Returns: None (updates playback position)
  - Internal calls: moc.seek

- **`go(timestamp)`** - Jump to absolute position in current file
  - `timestamp`: String in formats like '3h4m5s', '2:15:30', '300s', '300'
  - Returns: None (seeks to position)
  - Internal calls: moc.go

#### Comment and Mark Navigation
- **`jump()`** - Interactive jump to saved comment or mark
  - Returns: None (opens selection interface for saved marks)
  - Internal calls: `jump_to_select()` function

- **`jumploop()`** - Start interactive navigation session between marks
  - Returns: None (starts unbuffered navigation loop through selected marks up to 62)
  - Internal calls: `jumploop()` function

#### File Discovery and Management
- **`most_commented(limit=62)`** - Browse and play most-commented files
  - `limit`: Maximum number of files to display (default 62)
  - Returns: None (opens selection interface for frequently annotated files)
  - Internal calls: `most_commented_files_play_select()` function

- **`recent_files(limit=62)`** - Browse and play recently added files
  - `limit`: Maximum number of files to display (default 62)
  - Returns: None (opens selection interface for recently added files)
  - Internal calls: `recent_files_play_select()` function

- **`find(*glob_patterns)`** - Find and select audio files by pattern
  - `*glob_patterns`: File/directory glob patterns to search
  - Returns: None (opens selection interface for matching files)
  - Internal calls: moc.find_select_and_play

#### Comment Management
- **`delete_comments()`** - Select and delete comments/marks for current file
  - Returns: None (opens selection interface for comment deletion)
  - Internal calls: `delete_comments_select()` function

- **`edit_timestamp()`** - Edit timestamp of existing comment/mark
  - Returns: None (opens selection interface for timestamp editing)
  - Internal calls: `edit_comment_timestamp_select()` function

#### File Operations
- **`delete()`** - Delete current audio file and remove all associated data
  - Returns: None (removes file from filesystem, updates FILES collection, removes COMMENTS)
  - Internal calls: `delete()` function
