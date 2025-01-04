from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=255, default="Unnamed Video")  # Add a default value
    video = models.FileField(upload_to='videos/')  # Field to store video file
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for upload (auto_now_add=True)
    result = models.CharField(max_length=100, blank=True, null=True)  # Add result field to store detection result

    def __str__(self):
        return self.name

class Stream(models.Model):
    name = models.CharField(max_length=255, default="Video stream")  # Add a default value
    yt_url = models.URLField()  # Field to store YouTube URL
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    result = models.CharField(max_length=100, blank=True, null=True)  # Add result field to store detection result

    def __str__(self):
        return self.name

class Detection(models.Model):
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=255)
    link = models.URLField()
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"Detection {self.id} - {self.result} ({self.timestamp})"

class UploadedVideo(models.Model):
    video = models.FileField(upload_to='uploads/videos/')  # Directory where videos will be saved
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the video is uploaded

    def __str__(self):
        return f"Video uploaded on {self.uploaded_at}"
    
