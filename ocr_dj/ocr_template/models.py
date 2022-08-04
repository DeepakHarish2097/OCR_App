from django.db import models


class PdfTemplates(models.Model):
    title = models.CharField(max_length=100)
    pages = models.IntegerField()
    output_format = models.CharField(max_length=20)
    pdf = models.FileField(upload_to='pdf_templates/')
    marked = models.BooleanField(default=False)
    # detail_field = models.BooleanField(default=False)
    height_diff = models.IntegerField(default=0)
    total_rows = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class PdfGeneratedImages(models.Model):
    pdf = models.ForeignKey(PdfTemplates, on_delete=models.CASCADE)
    pdf_source_id = models.IntegerField()
    image = models.ImageField()


class PdfTemplateCoordinates(models.Model):
    pdf = models.ForeignKey(PdfTemplates, on_delete=models.CASCADE)
    pdf_source_id = models.IntegerField()
    caption = models.CharField(max_length=120)
    code = models.CharField(max_length=120)
    page = models.CharField(max_length=120)
    x_cord = models.IntegerField()
    y_cord = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    field_type = models.CharField(max_length=30)
    in_date_format = models.CharField(max_length=30)
    out_date_format = models.CharField(max_length=30)
    detail_field = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pdf_source_id}_{self.caption}"


class PdfProcess(models.Model):
    template_source_id = models.IntegerField()
    pdf = models.FileField(upload_to="pdf_process")
    data = models.TextField()
    process_count = models.IntegerField(default=0)


class PdfProcessImages(models.Model):
    process_source = models.ForeignKey(PdfProcess, models.CASCADE)
    source_id = models.IntegerField()
    image = models.ImageField()
