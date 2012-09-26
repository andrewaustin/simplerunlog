from django.forms import ModelForm, ChoiceField, RadioSelect
from apps.runlog.models import Run, UserProfile


class AddRunForm(ModelForm):
    class Meta:
        model = Run
        exclude = ('user',)
    # validation is inside the model


class UserProfileForm(ModelForm):
    public = ChoiceField(choices=((False,
        'No'), (True, 'Yes')), label="Make my profile public?",
        widget=RadioSelect)
    class Meta:
        model = UserProfile
        exclude = ('user',)
