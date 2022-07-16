from django.shortcuts import render, redirect
from .models import PdfTemplates, PdfGeneratedImages, PdfTemplateCoordinates, PdfProcess, PdfProcessImages
from django.http import HttpResponse, JsonResponse
from pdf2image import convert_from_path
from django.conf import settings
from django.core.files import File
import os
import json
import cv2
import pytesseract
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


@login_required(login_url="login")
def template_creation(request):
    return render(request, 'ocr_template.html')


def get_pdf_templates(request):
    templates = PdfTemplates.objects.all()
    return JsonResponse({"templates": list(templates.values())})


def create_template(request):
    if request.method == "POST":
        message = ""
        temp_name = request.POST['temp_name']
        try:
            temp_pages = request.POST['temp_pages']
        except ValueError:
            message = "No. of Pages must only be in number"
        temp_out_format = request.POST['temp_out_format']

        if not message:
            pdf_template = PdfTemplates(title=temp_name, pages=temp_pages, output_format=temp_out_format)
            pdf_template.save()
            message = "Template Created Successfully"
        return JsonResponse({"message": message, "pdf_template": pdf_template.title, "temp_id": pdf_template.id})


def get_generated_images(id):
    gen_images = PdfGeneratedImages.objects.filter(pdf_source_id=id)
    return gen_images


def get_template_cord(id):
    temp_cord = PdfTemplateCoordinates.objects.filter(pdf_source_id=id)
    return temp_cord


def get_template_details(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        template = PdfTemplates.objects.filter(id=temp_id).first()
        images_url = []
        gen_images = get_generated_images(temp_id)
        for page in gen_images:
            images_url.append(page.image.url)
        get_cord = get_template_cord(temp_id)
        return JsonResponse(
            {"temp_title": template.title, "pdf_pages": images_url, "temp_cord": list(get_cord.values())})


def update_template_file(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        pdf_file = request.FILES['pdf_file']

        template = PdfTemplates.objects.get(id=temp_id)
        template.pdf = pdf_file
        template.save()

        existing_images = get_generated_images(temp_id)
        for page in existing_images:
            os.remove(page.image.path)
            page.delete()

        gen_folder = os.path.join(settings.MEDIA_ROOT, 'generated_images')
        if not os.path.exists(gen_folder):
            os.mkdir(gen_folder)
        img_save_path = os.path.join(gen_folder, str(temp_id))
        if not os.path.exists(img_save_path):
            os.mkdir(img_save_path)

        pdf_pages = convert_from_path(template.pdf.path)
        num = 1
        for page in pdf_pages:
            name = os.path.join(img_save_path, f'{str(num)}.jpeg')
            with open(name, 'w') as img:
                image = File(img)
                page.save(image, "JPEG")
            generated_pdf_img = PdfGeneratedImages.objects.create(pdf=template, pdf_source_id=template.id,
                                                                  image=f'generated_images/{temp_id}/{num}.jpeg')
            generated_pdf_img.save()
            num += 1

        images_url = []
        gen_images = get_generated_images(temp_id)
        for page in gen_images:
            images_url.append(page.image.url)

        return JsonResponse({
            "pdf_pages": images_url
        })


def create_temp_coord(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        pdf_obj = PdfTemplates.objects.get(id=temp_id)
        data = json.loads(request.POST['data'])
        for dt in data:
            page = dt['page']
            caption = dt['caption']
            code = dt['code']
            cord = dt['cord']
            x_cord = cord['x']
            y_cord = cord['y']
            width = cord['width']
            height = cord['height']
            field_type = dt['field_type']
            in_date_format = dt['in_date_format']
            out_date_format = dt['out_date_format']
            PdfTemplateCoordinates.objects.create(
                page=page,
                caption=caption,
                code=code,
                x_cord=x_cord,
                y_cord=y_cord,
                width=width,
                height=height,
                pdf=pdf_obj,
                pdf_source_id=temp_id,
                field_type=field_type,
                in_date_format=in_date_format,
                out_date_format=out_date_format,
            )

        temp_cord = get_template_cord(temp_id)
        return JsonResponse({"temp_cord": list(temp_cord.values())})


def delete_cord(request):
    if request.method == "POST":
        delete_id = int(request.POST['delete_id'])
        del_obj = PdfTemplateCoordinates.objects.get(id=delete_id)
        source_id = del_obj.pdf_source_id
        del_obj.delete()
        temp_cord = get_template_cord(source_id)
        return JsonResponse({"temp_cord": list(temp_cord.values())})


@login_required(login_url="login")
def process_page(request):
    return render(request, 'ocr_process.html')


def process_images(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        pdf_file = request.FILES['pdf_file']

        pdf_process = PdfProcess(template_source_id=temp_id, pdf=pdf_file)
        pdf_process.save()

        gen_folder = os.path.join(settings.MEDIA_ROOT, 'process_images')
        if not os.path.exists(gen_folder):
            os.mkdir(gen_folder)
        img_save_path = os.path.join(gen_folder, str(pdf_process.id))
        if not os.path.exists(img_save_path):
            os.mkdir(img_save_path)

        pdf_pages = convert_from_path(pdf_process.pdf.path)
        num = 1
        for page in pdf_pages:
            name = os.path.join(img_save_path, f'{str(num)}.jpeg')
            with open(name, 'w') as img:
                image = File(img)
                page.save(image, "JPEG")
            generated_pdf_img = PdfProcessImages.objects.create(process_source=pdf_process, source_id=pdf_process.id,
                                                                image=f'process_images/{pdf_process.id}/{num}.jpeg')
            generated_pdf_img.save()
            num += 1

        img_url = []
        img_path = []
        gen_images = PdfProcessImages.objects.filter(source_id=pdf_process.id)
        for page in gen_images:
            img_url.append(page.image.url)
            img_path.append(page.image.path)

        temp_cord = get_template_cord(temp_id)
        data = []
        for page in img_path:
            img_name = os.path.split(page)[-1]
            image = cv2.imread(page)
            image2 = image.copy()
            for cord in temp_cord:
                if cord.page == img_name:
                    x = cord.x_cord
                    y = cord.y_cord
                    w = cord.width
                    h = cord.height
                    cropped_img = image[y:y + h, x:x + w]
                    text = pytesseract.image_to_string(cropped_img)
                    if cord.field_type == "4":
                        text = text.strip()
                        try:
                            in_date = datetime.datetime.strptime(text, cord.in_date_format)
                            text = in_date.strftime(cord.out_date_format)
                        except Exception as e:
                            print(e)

                    data.append({
                        "code": cord.code,
                        "caption": cord.caption,
                        "page": img_name.replace(".jpeg", ""),
                        "text": text.strip()
                    })
                    marked_image = cv2.rectangle(image2, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    cv2.imwrite(page, marked_image)

        return JsonResponse({"img_url": img_url, "data": data, "pdf_id": pdf_process.id})


def download_file(response, data):
    pdf_process = PdfProcess.objects.get(id=data)
    details = json.loads(pdf_process.data)
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename=SF_{data}.835'
    sample_path = os.path.join(settings.MEDIA_ROOT, "Sample.835")
    with open(sample_path, "r") as file:
        text = file.read()
        for dt in details:
            code = f"{{{dt['code']}}}"
            if code in text:
                text = text.replace(code, dt["text"])
        response.write(text)
    return response


def set_data(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        data = request.POST['data']
        pdf_process = PdfProcess.objects.get(id=temp_id)
        pdf_process.data = data
        pdf_process.save()
        return JsonResponse({"code": 200})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('template')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('template')
            else:
                messages.info(request, 'Username OR password is incorrect')

    return render(request, 'login.html')


def log_out(request):
    logout(request)
    return redirect('login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('template')
    else:
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('login')
            else:
                messages.info(request, "Passwords doesn't match")
    return render(request, 'register.html')


def get_cord_values(request):
    if request.method == "POST":
        view_cord = int(request.POST['view_id'])
        view_obj = PdfTemplateCoordinates.objects.get(id=view_cord)
        data = {
            "x": view_obj.x_cord,
            "y": view_obj.y_cord,
            "width": view_obj.width,
            "height": view_obj.height,
        }
        page = view_obj.page.replace(".jpeg", "")
        return JsonResponse({"data": data, "page": page})


def preview_data(request):
    if request.method == "POST":
        temp_id = int(request.POST['temp_id'])
        gen_images = get_generated_images(temp_id)
        temp_cord = get_template_cord(temp_id)
        gen_folder = os.path.join(settings.MEDIA_ROOT, 'preview_images')
        if not os.path.exists(gen_folder):
            os.mkdir(gen_folder)
        img_save_path = os.path.join(gen_folder, str(temp_id))
        if not os.path.exists(img_save_path):
            os.mkdir(img_save_path)
        num = 1
        data = []
        for page in gen_images:
            img_path = page.image.path
            image = cv2.imread(img_path)
            img_name = os.path.split(img_path)[-1]
            for cord in temp_cord:
                if cord.page == img_name:
                    x = cord.x_cord
                    y = cord.y_cord
                    w = cord.width
                    h = cord.height
                    cropped_img = image[y:y + h, x:x + w]
                    text = pytesseract.image_to_string(cropped_img)
                    img_save_file = os.path.join(img_save_path, f"{num}.jpeg")
                    cv2.imwrite(img_save_file, cropped_img)
                    img_save_file = f"/media/preview_images/{str(temp_id)}/{num}.jpeg"
                    data.append({
                        "path": img_save_file,
                        "code": cord.caption,
                        "text": text
                    })
                    num += 1

        return JsonResponse({"data": data})


# TODO Datetime validation
# TODO onbeforeunload in js
