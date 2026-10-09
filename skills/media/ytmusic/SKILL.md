---
name: YouTubeMusicSkill
description: Guidelines and CLI commands for searching, retrieving lyrics, managing library playlists, and controlling media playback (play, pause, stop, skip) on YouTube Music using the python helper script.
tools: [executeSessionCommand]
---

# YouTube Music CLI Skill

This skill instructs the agent on how to interact with YouTube Music by executing the helper script `ytmusic_cli.py` located in `./skills/ytmusic/scripts/`.

It supports both:

1. **Public/Authenticated Library Queries**: Search, fetching playlists, getting song lyrics, and managing playlists (requires authentication file).
2. **Global Media Playback Controls**: Playing specific tracks/playlists in the browser and sending global Windows media keyboard keys (Play/Pause, Stop, Skip).

## Setup & Authentication (Optional)

If the user requests actions involving their private library (like listing playlists, creating playlists, or getting private favorites):

1. The user must generate an authorization file `oauth.json` using the `ytmusicapi oauth` terminal setup process.
2. The agent should pass the path of the generated file via `--auth ./skills/ytmusic/oauth.json`.

If `--auth` is not passed, the script automatically accesses public YouTube Music content (such as search, charts, public albums/artists, and lyrics).

## CLI Command Actions

Invoke the helper script using the `executeSessionCommand` tool:

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --action <action> [options]
```

### Supported Actions

#### 1. Exploration & Library Mappings

- `search`: Search public files. Requires `--query`, optional `--filter` (`songs`, `videos`, `albums`, `artists`, `playlists`).
- `get_playlists`: Gets a list of library playlists (requires `--auth`).
- `get_artist`: Gets artist details. Requires `--channel-id`.
- `get_album`: Gets album details. Requires `--album-id`.
- `get_song`: Gets song metadata. Requires `--video-id`.
- `get_lyrics`: Gets lyrics for a track. Requires `--video-id` or `--lyrics-id`.
- `get_playlist`: Gets tracks in a playlist. Requires `--playlist-id`.
- `create_playlist`: Creates a new playlist. Requires `--title`, optional `--description`, `--privacy` (`PUBLIC`, `PRIVATE`, `UNLISTED`).
- `add_playlist_item`: Appends a track. Requires `--playlist-id` and `--video-id`.
- `remove_playlist_item`: Removes a track. Requires `--playlist-id` and `--video-id`.

#### 2. Local Media Playback Control

- `play`: Opens the default browser to YouTube Music to begin playing. Requires `--video-id` (song) or `--playlist-id` (playlist).
- `pause`: Toggles Windows system Play/Pause (sends `VK_MEDIA_PLAY_PAUSE`).
- `stop`: Halts Windows system playback (sends `VK_MEDIA_STOP`).
- `next`: Skips to next track (sends `VK_MEDIA_NEXT_TRACK`).
- `prev`: Skips to previous track (sends `VK_MEDIA_PREV_TRACK`).

## Examples

### 1. Searching for a Song

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --action search --query "Bohemian Rhapsody" --filter songs
```

### 2. Getting Lyrics for a Song

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --action get_lyrics --video-id "fJ9rUzIMcZQ"
```

### 3. Playing a Playlist

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --action play --playlist-id "PL7P1pWc1gGg6H2b1z"
```

### 4. Pausing Playback

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --action pause
```

### 5. Fetching Library Playlists

```bash
python ../skills/ytmusic/scripts/ytmusic_cli.py --auth ./skills/ytmusic/oauth.json --action get_playlists
```
