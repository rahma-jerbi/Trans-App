from django.contrib import admin
from .models import Transcription

@admin.register(Transcription)
class TranscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'transcribed_text', 'pdf_file')
    search_fields = ('transcribed_text',)
