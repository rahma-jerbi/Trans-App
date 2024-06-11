from django.db import models

class Transcription(models.Model):
    audio_file = models.FileField(upload_to='audio_files/')
    transcribed_text = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='pdf_files/', blank=True)

    def __str__(self):
        return f"Transcription {self.id}"
