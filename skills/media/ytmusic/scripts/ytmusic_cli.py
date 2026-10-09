import sys
import json
import argparse
import webbrowser
import ctypes

def trigger_media_key(key_code):
    try:
        # Virtual key codes:
        # VK_MEDIA_NEXT_TRACK = 0xB0
        # VK_MEDIA_PREV_TRACK = 0xB1
        # VK_MEDIA_STOP = 0xB2
        # VK_MEDIA_PLAY_PAUSE = 0xB3
        if hasattr(ctypes, 'windll'):
            ctypes.windll.user32.keybd_event(key_code, 0, 0, 0)
            ctypes.windll.user32.keybd_event(key_code, 0, 2, 0) # Key up
            return {"success": True, "message": f"Media key {hex(key_code)} triggered successfully."}
        else:
            return {"success": False, "error": "Media key simulation is only supported natively on Windows."}
    except Exception as e:
        return {"success": False, "error": f"Failed to trigger media key: {e}"}

def main():
    parser = argparse.ArgumentParser(description="YouTube Music CLI Integration Script")
    parser.add_argument("--auth", help="Path to auth JSON file (e.g. oauth.json)")
    parser.add_argument("--action", required=True, help="Action to perform: search, get_playlists, get_artist, get_album, get_song, get_lyrics, get_playlist, create_playlist, add_playlist_item, remove_playlist_item, play, pause, stop, next, prev")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--filter", help="Search filter (songs, videos, albums, artists, playlists)")
    parser.add_argument("--channel-id", help="Artist channel ID")
    parser.add_argument("--album-id", help="Album ID")
    parser.add_argument("--video-id", help="Video/Track ID")
    parser.add_argument("--playlist-id", help="Playlist ID")
    parser.add_argument("--lyrics-id", help="Lyrics ID")
    parser.add_argument("--title", help="Playlist title")
    parser.add_argument("--description", help="Playlist description")
    parser.add_argument("--privacy", default="PRIVATE", help="Playlist privacy (PUBLIC, PRIVATE, UNLISTED)")

    args = parser.parse_args()

    action = args.action.lower()

    # Handle native Windows playback control actions first (no ytmusicapi package needed)
    if action == "pause":
        print(json.dumps(trigger_media_key(0xB3)))
        sys.exit(0)
    elif action == "stop":
        print(json.dumps(trigger_media_key(0xB2)))
        sys.exit(0)
    elif action == "next":
        print(json.dumps(trigger_media_key(0xB0)))
        sys.exit(0)
    elif action == "prev":
        print(json.dumps(trigger_media_key(0xB1)))
        sys.exit(0)
    elif action == "play":
        if args.video_id:
            url = f"https://music.youtube.com/watch?v={args.video_id}"
            webbrowser.open(url)
            print(json.dumps({"success": True, "url": url, "message": "Opened song in browser."}))
            sys.exit(0)
        elif args.playlist_id:
            url = f"https://music.youtube.com/playlist?list={args.playlist_id}"
            webbrowser.open(url)
            print(json.dumps({"success": True, "url": url, "message": "Opened playlist in browser."}))
            sys.exit(0)
        else:
            print(json.dumps({"error": "Either --video-id or --playlist-id is required for play action."}))
            sys.exit(1)

    # Initialize ytmusicapi library for data-fetching actions
    try:
        from ytmusicapi import YTMusic
    except ImportError:
        print(json.dumps({
            "error": "The 'ytmusicapi' library is not installed.",
            "recommendation": "Please run 'pip install ytmusicapi' to use data-fetching actions."
        }))
        sys.exit(1)

    try:
        if args.auth:
            yt = YTMusic(args.auth)
        else:
            yt = YTMusic()
    except Exception as e:
        print(json.dumps({"error": f"Failed to initialize YTMusic: {e}"}))
        sys.exit(1)

    try:
        if action == "search":
            if not args.query:
                print(json.dumps({"error": "--query is required for search action."}))
                sys.exit(1)
            results = yt.search(args.query, filter=args.filter)
            print(json.dumps(results))

        elif action == "get_playlists":
            results = yt.get_library_playlists()
            print(json.dumps(results))

        elif action == "get_artist":
            if not args.channel_id:
                print(json.dumps({"error": "--channel-id is required for get_artist action."}))
                sys.exit(1)
            results = yt.get_artist(args.channel_id)
            print(json.dumps(results))

        elif action == "get_album":
            if not args.album_id:
                print(json.dumps({"error": "--album-id is required for get_album action."}))
                sys.exit(1)
            results = yt.get_album(args.album_id)
            print(json.dumps(results))

        elif action == "get_song":
            if not args.video_id:
                print(json.dumps({"error": "--video-id is required for get_song action."}))
                sys.exit(1)
            results = yt.get_song(args.video_id)
            print(json.dumps(results))

        elif action == "get_lyrics":
            # Support both direct lyrics_id or fetching from watch playlist
            if args.lyrics_id:
                results = yt.get_lyrics(args.lyrics_id)
                print(json.dumps(results))
            elif args.video_id:
                watch = yt.get_watch_playlist(args.video_id)
                lyrics_id = watch.get("lyrics")
                if lyrics_id:
                    results = yt.get_lyrics(lyrics_id)
                    print(json.dumps(results))
                else:
                    print(json.dumps({"error": "No lyrics available for this song."}))
            else:
                print(json.dumps({"error": "--lyrics-id or --video-id is required for get_lyrics action."}))
                sys.exit(1)

        elif action == "get_playlist":
            if not args.playlist_id:
                print(json.dumps({"error": "--playlist-id is required for get_playlist action."}))
                sys.exit(1)
            results = yt.get_playlist(args.playlist_id)
            print(json.dumps(results))

        elif action == "create_playlist":
            if not args.title:
                print(json.dumps({"error": "--title is required for create_playlist action."}))
                sys.exit(1)
            playlist_id = yt.create_playlist(args.title, args.description or "", privacy_status=args.privacy.upper())
            print(json.dumps({"success": True, "playlist_id": playlist_id}))

        elif action == "add_playlist_item":
            if not (args.playlist_id and args.video_id):
                print(json.dumps({"error": "--playlist-id and --video-id are required for add_playlist_item action."}))
                sys.exit(1)
            status = yt.add_playlist_items(args.playlist_id, [args.video_id])
            print(json.dumps({"status": status}))

        elif action == "remove_playlist_item":
            if not (args.playlist_id and args.video_id):
                print(json.dumps({"error": "--playlist-id and --video-id are required for remove_playlist_item action."}))
                sys.exit(1)
            # Find the track object inside the playlist to get its setID if possible,
            # or pass the videoId directly if supported by ytmusicapi
            playlist_details = yt.get_playlist(args.playlist_id)
            tracks = playlist_details.get("tracks", [])
            target_track = None
            for t in tracks:
                if t.get("videoId") == args.video_id:
                    target_track = t
                    break
            if target_track:
                status = yt.remove_playlist_items(args.playlist_id, [target_track])
                print(json.dumps({"status": status}))
            else:
                print(json.dumps({"error": f"Track '{args.video_id}' not found in playlist."}))

        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

    except Exception as e:
        print(json.dumps({"error": f"Execution failed: {e}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
