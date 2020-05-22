from pymediainfo import MediaInfo

# media = MediaInfo.parse('/home/jorge/IdeaProjects/autoTube/downloads/0.mp4')
media = MediaInfo.parse('/home/jorge/IdeaProjects/autoTube/downloads/1.mp4')
video_track = list(filter(lambda track: track.track_type == 'Video', media.tracks))[0]
print(video_track)


# for track in media.tracks:
#     if track.track_type == 'Video':
#         print(track.bit_rate, track.bit_rate_mode, track.codec, track.width)