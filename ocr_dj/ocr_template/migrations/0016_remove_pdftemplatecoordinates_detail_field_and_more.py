# Generated by Django 4.0.5 on 2022-07-21 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0015_pdftemplatecoordinates_detail_field_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pdftemplatecoordinates',
            name='detail_field',
        ),
        migrations.RemoveField(
            model_name='pdftemplatecoordinates',
            name='height_diff',
        ),
        migrations.RemoveField(
            model_name='pdftemplatecoordinates',
            name='total_rows',
        ),
        migrations.AddField(
            model_name='pdftemplates',
            name='detail_field',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdftemplates',
            name='height_diff',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdftemplates',
            name='total_rows',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
