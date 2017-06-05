import boto3
import time
import uuid
import requests
import os
import textwrap
from io import BytesIO
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from moviepy.editor import *



class Video(object):

    def __init__(self, file):
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.video_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        self.perform_thumbnail()

        self.set_foreground()
        self.set_background()

        self.perfom_add_text_thumb()
        self.perform_generate_video()
        self.perform_merge()
        self.perform_upload()
        self.perform_delete()


    def perform_thumbnail(self):
        clip = VideoFileClip(self.file_path)
        clip= clip.resize( (480,640) )
        clip.save_frame(self.thumbnail_path, t=0.00)


    def perfom_add_text_thumb(self):
        self.foreground = self.foreground.resize((480, 640), Image.ANTIALIAS)
        self.foreground.paste(self.background, (0, 0), self.background)

        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', 30)  # 55
        draw = ImageDraw.Draw(self.foreground)
        lines = textwrap.wrap("Que pensez-vous de Spitch ? La nouvelle application qui dechire sa mere", width=18)  # 20
        W, H = self.foreground.size
        y_text = 150  # 400
        for line in lines:
            width, height = font.getsize(line)
            w, h = draw.textsize(line, font=font)
            m = (W - w) / 2
            draw.text((m, y_text), line, font=font, fill=(255, 255, 255))
            y_text += height + 5

        self.foreground.save(self.thumbnail_path, "JPEG")


    def perform_generate_video(self):
        print("---- perform_generate_video -------")
        some_video_clip = ImageClip(self.thumbnail_path)
        some_video_clip.set_duration(3).write_videofile(self.video_path, fps=1, verbose=False)


    def perform_merge(self):
        print("---- perform_merge -------")
        clip1 = VideoFileClip(self.video_path)
        clip2 = VideoFileClip(self.file_path, audio=True)
        clip2 = clip2.resize((480, 640))
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(self.video_path, audio=True, audio_codec='aac', verbose=False)


    def perform_upload(self):
        s3 = boto3.client('s3')
        self.key = "{}.mp4".format(str(uuid.uuid4()))
        file = open(self.video_path, 'rb')
        s3.put_object(Bucket='spitchdev-bucket-uwfmzpv98dvk', Key=self.key, Body=file, ContentType='video/mp4')


    def perform_delete(self):
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)
        os.remove(self.video_path)


    def get_url(self):
        return "https://s3-eu-west-1.amazonaws.com/spitchdev-bucket-uwfmzpv98dvk/"+self.key

    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)

    def set_background(self):
        self.background = Image.open("apps/spitch/theme/fond-iphone.png")





class VideoNoFade(object):

    def __init__(self, file):
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.video_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        self.perform_thumbnail()

        self.set_foreground()
        self.set_background()

        self.perfom_add_text_thumb()
        self.perform_generate_video()
        self.perform_merge()
        self.perform_upload()
        self.perform_delete()


    def perform_thumbnail(self):
        clip = VideoFileClip(self.file_path)
        clip= clip.resize( (480,640) )
        clip.save_frame(self.thumbnail_path, t=0.00)


    def perfom_add_text_thumb(self):
        self.foreground = self.foreground.resize((480, 640), Image.ANTIALIAS)
        self.foreground.paste(self.background, (0, 0), self.background)

        font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', 30)  # 55
        draw = ImageDraw.Draw(self.foreground)
        lines = textwrap.wrap("Que pensez-vous de Spitch ? La nouvelle application qui dechire sa mere", width=18)  # 20
        W, H = self.foreground.size
        y_text = 150  # 400
        for line in lines:
            width, height = font.getsize(line)
            w, h = draw.textsize(line, font=font)
            m = (W - w) / 2
            draw.text((m, y_text), line, font=font, fill=(255, 255, 255))
            y_text += height + 5

        self.foreground.save(self.thumbnail_path, "JPEG")


    def perform_generate_video(self):
        print("---- perform_generate_video -------")
        some_video_clip = ImageClip(self.thumbnail_path)
        some_video_clip.set_duration(3).write_videofile(self.video_path, fps=15)


    def perform_merge(self):
        print("---- perform_merge -------")
        clip1 = VideoFileClip(self.video_path)
        clip2 = VideoFileClip(self.file_path, audio=True)
        clip2 = clip2.resize((480, 640))
        final_clip = concatenate_videoclips([clip1, clip2])
        final_clip.write_videofile(self.video_path, audio=True, audio_codec='aac')


    def perform_upload(self):
        s3 = boto3.client('s3')
        self.key = "{}.mp4".format(str(uuid.uuid4()))
        file = open(self.video_path, 'rb')
        s3.put_object(Bucket='spitchdev-bucket-uwfmzpv98dvk', Key=self.key, Body=file, ContentType='video/mp4')


    def perform_delete(self):
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)
        os.remove(self.video_path)


    def get_url(self):
        return "https://s3-eu-west-1.amazonaws.com/spitchdev-bucket-uwfmzpv98dvk/"+self.key

    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)

    def set_background(self):
        response = requests.get("https://s3-eu-west-1.amazonaws.com/spitchdev-bucket-uwfmzpv98dvk/fond-iphone.png")
        self.background = Image.open(BytesIO(response.content))