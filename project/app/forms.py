from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class ConfirmationForm(forms.Form):
    confirmed = forms.BooleanField(label="Xác nhận")
