# Generated by Django 4.0.5 on 2022-07-14 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0012_pdfprocess_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdftemplates',
            name='marked',
            field=models.BooleanField(default=False),
        ),
    ]
