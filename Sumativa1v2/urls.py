from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.agregarReserva, name='agregar_reserva'),
    path('eliminarReserva/<int:id>/', views.eliminarReserva, name='eliminar_reserva'),
    path('actualizarReserva/<int:id>/', views.actualizarReserva, name='actualizar_reserva'),
    path('generarPDF/<int:id>/', views.generar_pdf, name='generar_pdf'),
    path('verQR/<int:id>/', views.mostrar_qr, name='ver_qr'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
