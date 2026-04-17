from upload_to_youtube import get_youtube_client


def delete_previous_batch(count: int = 10):
    youtube = get_youtube_client()

    channels_response = youtube.channels().list(
        part="contentDetails",
        mine=True
    ).execute()

    uploads_playlist_id = channels_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_items = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=count
    ).execute()

    items = playlist_items.get("items", [])
    if not items:
        print("No previous videos found to delete.")
        return

    video_ids = [item["contentDetails"]["videoId"] for item in items]
    print(f"Deleting last {len(video_ids)} videos: {video_ids}")

    for vid in video_ids:
        youtube.videos().delete(id=vid).execute()
        print(f"Deleted video {vid}")
