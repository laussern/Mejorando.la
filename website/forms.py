from django.forms import ModelForm
from .models import VideoComentario


# el formulario para agregar un comentario al video
class VideoComentarioForm(ModelForm):
    class Meta:
        model = VideoComentario
        fields = ('autor', 'autor_email', 'autor_url', 'content')
