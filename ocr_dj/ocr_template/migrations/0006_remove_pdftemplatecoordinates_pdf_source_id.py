# Generated by Django 4.0.5 on 2022-07-11 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0005_pdftemplatecoordinates_pdf_source_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdftemplatecoordinates',
            name='pdf_source_id',
        ),
    ]
