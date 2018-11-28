from moviepy.editor import *
import settings
import logging


def fix_final_clip(final_clip):
    return final_clip.set_audio(final_clip.audio.set_fps(final_clip.fps))

def edit_video(broadcasters):
    clips = []
    # audio_iterator = 0
    logging.info('Starting video edit')
    for i in range(len(broadcasters)):
        clip = VideoFileClip(settings.DOWNLOADS_DIRECTORY + str(i) + '.mp4').resize(width=1920)
        if clip.duration > 194:
            continue
        text_clip = TextClip(txt=broadcasters[i], font='Burbank Big Condensed Black',
                             fontsize=200, color='white', stroke_color='black',
                             stroke_width=5).set_position(('right', 'top')).set_duration(clip.duration)
        clip = CompositeVideoClip([clip, text_clip])

        # audio_clip = AudioFileClip('music/' + str(audio_iterator) + '.mp3')
        # while audio_clip.duration < clip.duration:
        #     audio_iterator = audio_iterator + 1 if audio_iterator < 9 else 0
        #     audio_clip = AudioFileClip('music/' + str(audio_iterator) + '.mp3')
        # audio_clip = audio_clip.subclip(0, clip.duration)
        # audio_iterator = audio_iterator + 1 if audio_iterator < 9 else 0

        # composed_audio = CompositeAudioClip([clip.audio, audio_clip.volumex(0.2)])
        # fusion_clip = clip.set_audio(composed_audio)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips, method='compose')
    outro = VideoFileClip(settings.UTILS_DIRECTORY + 'outro.mp4')
    final_clip = concatenate_videoclips([final_clip, outro], method='compose')



    # subscribe_clip = VideoFileClip('widgets/GrnScrn.mp4').subclip(0,3)
    # subscribe_masked = vfx.mask_color(subscribe_clip, color=[1, 253, 0])
    # final_clip = CompositeVideoClip([final_clip, subscribe_masked])

    final_clip = fix_final_clip(final_clip)

    final_clip.write_videofile(settings.RESULT_DIRECTORY + 'result.mp4', codec='libx264', threads=4)
    logging.info('Render finished')
    # final_clip.preview()
