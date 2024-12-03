from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from .models import Reserva
from .forms import ReservaForm
from xhtml2pdf import pisa
from io import BytesIO

# Función para generar PDF
def generar_pdf_en_memoria(reserva, request):
    """
    Genera un PDF con los detalles de la reserva y lo devuelve como un archivo en memoria.
    """
    template_path = 'templatesApp/pdf_template.html'

    # Crear URLs absolutas para las imágenes
    foto_paciente_url = request.build_absolute_uri(reserva.foto_paciente.url) if reserva.foto_paciente else None
    codigo_qr_url = request.build_absolute_uri(reserva.codigo_qr.url) if reserva.codigo_qr else None

    # Contexto para el template
    context = {
        'reserva': reserva,
        'foto_paciente_url': foto_paciente_url,
        'codigo_qr_url': codigo_qr_url,
    }

    # Renderizar el template
    html = render_to_string(template_path, context)

    # Generar PDF en memoria
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        print(f"Error al generar el PDF: {pisa_status.err}")
        return None

    pdf_buffer.seek(0)
    return pdf_buffer


# Función para enviar correos con PDF adjunto
def enviar_correo(reserva, request):
    """
    Envía un correo al email registrado en la reserva utilizando un PDF adjunto.
    """
    # Generar el PDF
    pdf_file = generar_pdf_en_memoria(reserva, request)

    if not pdf_file:
        print(f"Error al generar el PDF para la reserva ID {reserva.idSolicitud}. El correo no será enviado.")
        return

    # Renderizar la plantilla del email
    contenido_html = render_to_string('templatesApp/email_template.html', {
        'reserva': reserva,
    })

    # Configurar el mensaje de correo
    email = EmailMessage(
        subject=f'Confirmación de Reserva #{reserva.idSolicitud}',
        body=contenido_html,
        from_email='joao.nunez@inacapmail.cl',  # Cambiar por el correo verificado
        to=[reserva.email],
    )
    email.content_subtype = 'html'  # Especificar que el contenido es HTML

    # Adjuntar el PDF
    email.attach(f'reserva_{reserva.idSolicitud}.pdf', pdf_file.read(), 'application/pdf')

    # Enviar el correo
    try:
        email.send()
        print(f"Correo enviado exitosamente a {reserva.email} con el PDF adjunto.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


# Función para agregar reservas
def agregarReserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.save()

            # Llamar a la función para enviar el correo
            enviar_correo(reserva, request)

            print(f"Reserva agregada con éxito: ID {reserva.idSolicitud}")
            return redirect('/')
    else:
        form = ReservaForm()

    reservas = Reserva.objects.all()
    return render(request, 'templatesApp/agregar.html', {'form': form, 'reservas': reservas})


# Función para eliminar reservas
def eliminarReserva(request, id):
    """
    Elimina una reserva por su ID y redirige a la página principal.
    """
    reserva = get_object_or_404(Reserva, idSolicitud=id)
    reserva.delete()
    print(f"Reserva con ID {id} eliminada exitosamente.")
    return redirect('/')


# Función para actualizar reservas
def actualizarReserva(request, id):
    """
    Actualiza una reserva existente.
    """
    reserva = get_object_or_404(Reserva, idSolicitud=id)
    form = ReservaForm(instance=reserva)
    if request.method == 'POST':
        form = ReservaForm(request.POST, request.FILES, instance=reserva)
        if form.is_valid():
            form.save()
            print(f"Reserva con ID {id} actualizada correctamente.")
            return redirect('/')
    reservas = Reserva.objects.all()
    return render(request, 'templatesApp/agregar.html', {'form': form, 'reservas': reservas})


# Función para generar PDF
def generar_pdf(request, id):
    """
    Genera un PDF con los detalles de la reserva y lo muestra en el navegador.
    """
    reserva = get_object_or_404(Reserva, idSolicitud=id)
    template_path = 'templatesApp/pdf_template.html'

    # Crear URLs absolutas para las imágenes
    foto_paciente_url = request.build_absolute_uri(reserva.foto_paciente.url) if reserva.foto_paciente else None
    codigo_qr_url = request.build_absolute_uri(reserva.codigo_qr.url) if reserva.codigo_qr else None

    # Contexto para el template
    context = {
        'reserva': reserva,
        'foto_paciente_url': foto_paciente_url,
        'codigo_qr_url': codigo_qr_url,
    }

    # Configuración para la respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="reserva_{reserva.idSolicitud}.pdf"'

    # Renderizar el template
    html = render_to_string(template_path, context)

    # Generar el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        print(f"Error al generar el PDF: {pisa_status.err}")
        return HttpResponse(f"Error al generar el PDF: {pisa_status.err}")
    print(f"PDF generado exitosamente para la reserva ID {reserva.idSolicitud}")
    return response


# Función para mostrar el QR
def mostrar_qr(request, id):
    """
    Muestra el código QR de la reserva.
    """
    reserva = get_object_or_404(Reserva, idSolicitud=id)
    print(f"Mostrando QR para la reserva ID {reserva.idSolicitud}")
    return render(request, 'templatesApp/ver_qr.html', {'reserva': reserva})
