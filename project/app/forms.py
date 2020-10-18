import csv 
from django import forms
from io import StringIO

class UploadFileForm(forms.Form):
    """Form for uploading csv file containing Youtube urls"""
    input_file = forms.FileField()
    
    def get_url_list(self):
        """Get url list form input csv file"""
        csv_file = str(self.cleaned_data['input_file'].read(), encoding='utf-8')
        reader = csv.reader(StringIO(csv_file), dialect='excel')
        url_list = [x for x in reader]
        return url_list[1:] # first line is header 
    
