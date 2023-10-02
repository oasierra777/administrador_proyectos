from django import forms
from status.models import Status

class StatusChoiceForm(forms.Form):
    status = forms.ModelChoiceField(queryset = Status.objects.all(), initial=0) #combo de seleccion

    def __init__(self, *args, **kwargs):
        super(StatusChoiceForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class':'browser-default'})
