# Generated by Django 4.0.5 on 2022-07-11 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0006_remove_pdftemplatecoordinates_pdf_source_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdftemplatecoordinates',
            name='pdf_source_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
