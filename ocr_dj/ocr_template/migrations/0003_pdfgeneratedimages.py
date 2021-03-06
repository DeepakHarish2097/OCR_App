# Generated by Django 4.0.5 on 2022-07-11 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_template', '0002_pdftemplates_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfGeneratedImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_source_id', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('pdf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ocr_template.pdftemplates')),
            ],
        ),
    ]
