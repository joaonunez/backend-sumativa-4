from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils.timezone import now

class EstadReserva(models.Model):
    estadoReservaId = models.CharField(primary_key=True, max_length=3)
    estadoReservaNombre = models.CharField(max_length=20)

    def __str__(self):
        return self.estadoReservaNombre


class TipoReserva(models.Model):
    tipoSolicitudId = models.CharField(primary_key=True, max_length=3)
    tipoSolicitud = models.CharField(max_length=20)

    def __str__(self):
        return self.tipoSolicitud


class Reserva(models.Model):
    idSolicitud = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)
    fechareserva = models.DateField()
    horareserva = models.TimeField()
    fecha_nacimiento = models.DateField()
    foto_paciente = models.ImageField(upload_to="fotos_carnet/", null=True, blank=True)
    cantidad_hermanos = models.IntegerField(null=True, blank=True)
    observaciones = models.TextField(max_length=5000)
    website = models.URLField()
    email = models.EmailField()
    donante = models.BooleanField()
    estadoReservaId = models.ForeignKey(EstadReserva, null=True, blank=False, on_delete=models.RESTRICT)
    tipoSolicitudId = models.ForeignKey(TipoReserva, null=True, blank=False, on_delete=models.RESTRICT)
    codigo_qr = models.ImageField(upload_to="qr_codes/", null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        qr_content = f"Reserva ID: {self.idSolicitud}, Nombre: {self.nombre}, Email: {self.email}"
        qr = qrcode.make(qr_content)
        qr_image = BytesIO()
        qr.save(qr_image, format="PNG")
        qr_image.seek(0)
        self.codigo_qr.save(f"qr_{self.idSolicitud}.png", File(qr_image), save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva {self.idSolicitud} - {self.nombre}"
