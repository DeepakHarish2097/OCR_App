# Generated by Django 4.0.5 on 2022-07-11 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0007_pdftemplatecoordinates_pdf_source_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdftemplatecoordinates',
            old_name='pdf_source_id',
            new_name='pdf_src_id',
        ),
    ]