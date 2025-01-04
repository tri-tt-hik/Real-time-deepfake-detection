f"""rom django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Video,Stream

class Video_form(forms.ModelForm):
    class Meta:
        model=Video
        fields=("caption","video")
class Stream_form(forms.ModelForm):
    class Meta:
        model=Stream
        fields=("name","yt_url")
"""
from django import forms
from .models import Video, Stream , UploadedVideo

class Video_form(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['name', 'video']

class Stream_form(forms.ModelForm):
    class Meta:
        model = Stream
        fields = ['name', 'yt_url']

class VerifyForm(forms.ModelForm):
    class Meta:
        model = UploadedVideo  # Use the UploadedVideo model
        fields = ['video']  # Include only the video field in the form