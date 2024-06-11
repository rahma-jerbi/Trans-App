from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label='Upload PDF File')
    keywords = forms.CharField(label='Keywords', help_text='Comma-separated keywords')
