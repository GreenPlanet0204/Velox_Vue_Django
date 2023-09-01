from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class GCSWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(),
            forms.TextInput(),
            forms.TextInput(),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
        # value is GCS Object
            return (value.bucket, value.filename, value.path,)
        else:
            return (None, None, None)

    def value_from_datadict(self, data, files, name):
        return 'value_from_datadict'


class GCSMultiForm(forms.MultiValueField):
    widget = GCSWidget

    def __init__(self, **kwargs):
        fields = (
            forms.CharField(required=False),
            forms.CharField(required=False),
            forms.CharField(required=False),
        )
        super().__init__(
            fields=fields,
            require_all_fields=False, **kwargs
        )

    def compress(self, data_list):
        return 'asdas'


class GCSBlobForm(forms.Form):
    bucket = forms.CharField(required=False)
    filename = forms.CharField(required=False)
    path = forms.CharField(required=False)
    uri = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        kwargs.pop('required')
        kwargs.pop('help_text')
        kwargs.pop('label')
        super().__init__(*args, **kwargs)
