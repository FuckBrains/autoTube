from moviepy.editor import *
from pymediainfo import MediaInfo
import settings
import logging


def fix_final_clip(final_clip):
    return final_clip.set_audio(final_clip.audio.set_fps(final_clip.fps))


def edit_video(broadcasters):
    clips = []
    sub_clip_path = settings.RESULT_DIRECTORY + 'sub.mov'
    sub_clip = VideoFileClip(sub_clip_path)
    masked_sub_clip = vfx.mask_color(sub_clip, color=[0,0,0])

    logging.info('Starting video edit')
    for i in range(len(broadcasters)):

        filename = settings.DOWNLOADS_DIRECTORY + str(i) + '.mp4'
        
        media = MediaInfo.parse(filename)
        video_track = list(
            filter(lambda track: track.track_type == 'Video', media.tracks))[0]
        forced_resolution = None
        if video_track.width != 1920:
            forced_resolution = (1080, 1920)

        clip = VideoFileClip(filename, target_resolution=forced_resolution)  # 6it/s
        if clip.duration > 194:
            continue
        # text_clip = TextClip(txt=broadcasters[i], font='Burbank Big Condensed Black',
        #                      fontsize=200, color='white', stroke_color='black',
        #                      stroke_width=5).set_position(('right', 'top')).set_duration(clip.duration)
        # clip = CompositeVideoClip([clip, text_clip])

        # audio_clip = AudioFileClip('music/' + str(audio_iterator) + '.mp3')
        # while audio_clip.duration < clip.duration:
        #     audio_iterator = audio_iterator + 1 if audio_iterator < 9 else 0
        #     audio_clip = AudioFileClip('music/' + str(audio_iterator) + '.mp3')
        # audio_clip = audio_clip.subclip(0, clip.duration)
        # audio_iterator = audio_iterator + 1 if audio_iterator < 9 else 0

        # composed_audio = CompositeAudioClip([clip.audio, audio_clip.volumex(0.2)])
        # fusion_clip = clip.set_audio(composed_audio)
        if i == 5:
            clip = CompositeVideoClip([clip, masked_sub_clip])
        clips.append(clip)

    outro = VideoFileClip(settings.UTILS_DIRECTORY + 'outro.mp4')
    clips.append(outro)
    final_clip = concatenate_videoclips(clips, method='compose')
    final_clip = fix_final_clip(final_clip)

    final_clip.write_videofile(
        settings.RESULT_DIRECTORY + 'result.mp4', codec='libx264', threads=4, fps=60)
    logging.info('Render finished')
