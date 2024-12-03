import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Configurar el mensaje de correo
message = Mail(
    from_email='joao.nunez@inacapmail.cl',  # Cambia esto por el correo registrado en SendGrid
    to_emails='joaovaldiglesias@gmail.com',  # Cambia esto por el correo destino
    subject='Prueba de Envío con SendGrid',
    html_content='<strong>¡Esto es una prueba con SendGrid!</strong>'
)

# Intentar enviar el correo
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))  # Clave API desde el entorno
    response = sg.send(message)
    print("Status Code:", response.status_code)  # Código de estado
    print("Body:", response.body)  # Respuesta del cuerpo
    print("Headers:", response.headers)  # Encabezados
except Exception as e:
    print("Error al enviar el correo:", str(e))
