from django.forms import ModelForm
from apps.runlog.models import Run


class addRunForm(ModelForm):
    class Meta:
        model = Run
        exclude = ('user',)
    # validation is inside the model
