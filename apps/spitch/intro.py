from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import os, boto3, uuid, requests
import textwrap
from moviepy.editor import *

from .models import Spitch


class Intro(object):
    png = None
    mp4 = None
    foreground = None
    background = None

    def __init__(self, file):
        # self.url = url
        # self.get_spitch()

        self.png = "/tmp/{}.png".format(str(uuid.uuid4()))
        self.mp4 = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.foreground = None
        self.background = None

        self.thumbnail(file)
        self.set_foreground()
        self.set_background()
        self.merge()
        self.generate_video()
        self.upload()
        self.delete()


    def thumbnail(self, file):
        self.file_path = "/tmp/{}.mp4".format(str(uuid.uuid4()))
        self.thumbnail_path = "/tmp/{}.jpg".format(str(uuid.uuid4()))

        with open(self.file_path, 'wb') as open_file:
            open_file.write(file.file.read())

        clip = VideoFileClip(self.file_path)
        clip.save_frame(self.thumbnail_path, t=0.00)



    def set_foreground(self):
        self.foreground = Image.open(self.thumbnail_path)


    def set_background(self):
        response = requests.get("https://s3-eu-west-1.amazonaws.com/spitchdev-bucket-uwfmzpv98dvk/fond-iphone.png")
        self.background = Image.open(BytesIO(response.content))


    def merge(self):
        self.foreground = self.foreground.resize((480,640), Image.ANTIALIAS)
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

        self.foreground.save(self.png, "JPEG")


    def generate_video(self):
        os.system(
            "ffmpeg -loop 1 -i {} -i audio.wav -vcodec libx264 -profile:v high -level 4.2 -preset medium -crf 23 -x264-params ref=4 -acodec copy -movflags +faststart -c:a aac -strict -2 -t 3 -pix_fmt yuv420p -vf scale=480:640 {}".format(
                self.png, self.mp4
            )
        )

    def upload(self):
        s3 = boto3.client('s3')
        self.key = "out.mp4"
        file = open(self.mp4, 'rb')
        buck = s3.put_object(Bucket='spitchdev-bucket-uwfmzpv98dvk', Key=self.key, Body=file, ContentType='video/mp4')


    def delete(self):
        os.remove(self.png)
        os.remove(self.mp4)
        os.remove(self.thumbnail_path)
        os.remove(self.file_path)


    def get_object(self):
        return "https://s3-eu-west-1.amazonaws.com/spitchdev-bucket-uwfmzpv98dvk/" + self.key






