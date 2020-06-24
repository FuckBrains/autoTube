from youtube_api import upload_video as upload_video_to_youtube

game = 'lol_es'
title = 'Test title'
file_path = '/home/jorge/IdeaProjects/autoTube/test_video.mp4'
description = 'test description'
category = 20
tags = ['test tag']

upload_video_to_youtube(game, title, file_path, description, category, tags)
