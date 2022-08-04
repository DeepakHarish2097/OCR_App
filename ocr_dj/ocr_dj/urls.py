from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ocr_template.views import (
    template_creation, get_pdf_templates, get_template_details,
    create_template, update_template_file, create_temp_coord,
    delete_cord, process_page, open_images, download_file,
    set_data, login_page, log_out, register_page, get_cord_values,
    preview_data, home_page, height_difference, process_images)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('template', template_creation, name='template'),
    path('get_pdf_temps/', get_pdf_templates, name='get_pdf_temps'),
    path('get_temp_details/', get_template_details, name='get_temp_details'),
    path('create_template/', create_template, name='create_template'),
    path('update_template/', update_template_file, name="update_template"),
    path('create_temp_coord/', create_temp_coord, name='create_temp_coord'),
    path('delete_cord/', delete_cord, name='delete_cord'),
    path('process/', process_page, name='process_page'),
    path('open_images/', open_images, name='open_images'),
    path('process_images/', process_images, name='process_images'),
    path('download/<int:data>/', download_file),
    path('set_data/', set_data, name='set_data'),
    path('login/', login_page, name='login'),
    path('logout/', log_out, name='logout'),
    path('register/', register_page, name='register'),
    path('get_cord_values/', get_cord_values, name='get_cord_values'),
    path('preview_data/', preview_data, name='preview_data'),
    path('home/', home_page, name='home'),
    path('', home_page, name='home'),
    path('height_difference/', height_difference, name='height_difference'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
