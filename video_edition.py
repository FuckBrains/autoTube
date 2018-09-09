from moviepy.editor import *


def fix_final_clip(final_clip):
    return final_clip.set_audio(final_clip.audio.set_fps(final_clip.fps))

def edit_video(positions_and_broadcaster):
    clips = []
    # audio_iterator = 0
    for i in range(len(positions_and_broadcaster)):
        clip = VideoFileClip('downloads/' + str(i) + '.mp4').resize(width=1920)
        if clip.duration > 194:
            continue
        text_clip = TextClip(txt=positions_and_broadcaster[i], font='Burbank Big Condensed Black',
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
    outro = VideoFileClip('utils/outro.mp4')
    final_clip = concatenate_videoclips([final_clip, outro], method='compose')



    # subscribe_clip = VideoFileClip('widgets/GrnScrn.mp4').subclip(0,3)
    # subscribe_masked = vfx.mask_color(subscribe_clip, color=[1, 253, 0])
    # final_clip = CompositeVideoClip([final_clip, subscribe_masked])

    final_clip = fix_final_clip(final_clip)

    final_clip.write_videofile('result.mp4', codec='libx264', threads=4)
    # final_clip.preview()
