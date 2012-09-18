from django.forms import ModelForm
from apps.runlog.models import Run, UserProfile


class AddRunForm(ModelForm):
    class Meta:
        model = Run
        exclude = ('user',)
    # validation is inside the model


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
