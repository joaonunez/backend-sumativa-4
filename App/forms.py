from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'nombre', 'telefono', 'fechareserva', 'horareserva', 'fecha_nacimiento',
            'foto_paciente', 'cantidad_hermanos', 'observaciones', 'website', 'email',
            'donante', 'estadoReservaId', 'tipoSolicitudId'
        ]

    fechareserva = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Reserva')
    horareserva = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Hora de Reserva')
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Fecha de Nacimiento')
    foto_paciente = forms.FileField(label="Foto tamaño carnet (Archivo a subir)")
    cantidad_hermanos = forms.IntegerField(label="Cantidad de Hermanos")
