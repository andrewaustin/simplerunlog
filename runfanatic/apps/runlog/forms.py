from django.forms import ModelForm, TypedChoiceField
from apps.runlog.models import Run, UserProfile


class AddRunForm(ModelForm):
    class Meta:
        model = Run
        exclude = ('user',)
    # validation is inside the model


class UserProfileForm(ModelForm):
    public = TypedChoiceField(coerce=lambda x: x =='True', choices=((False,
        'No'), (True, 'Yes')))
    class Meta:
        model = UserProfile
        exclude = ('user',)
