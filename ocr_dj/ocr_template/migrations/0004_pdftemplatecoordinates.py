# Generated by Django 4.0.5 on 2022-07-11 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0003_pdfgeneratedimages'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfTemplateCoordinates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=120)),
                ('code', models.CharField(max_length=120)),
                ('page', models.CharField(max_length=120)),
                ('x_cord', models.IntegerField()),
                ('y_cord', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ocr_template.pdftemplates')),
            ],
        ),
    ]
