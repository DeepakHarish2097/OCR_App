from django.contrib import admin
from .models import PdfTemplates, PdfGeneratedImages, PdfTemplateCoordinates, PdfProcess, PdfProcessImages


admin.site.register(PdfTemplates)
admin.site.register(PdfGeneratedImages)
admin.site.register(PdfTemplateCoordinates)
admin.site.register(PdfProcess)
admin.site.register(PdfProcessImages)
