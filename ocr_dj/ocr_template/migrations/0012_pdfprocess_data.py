# Generated by Django 4.0.5 on 2022-07-13 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0011_pdfprocess_pdfprocessimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfprocess',
            name='data',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
