from django import forms  
class UploadForm(forms.Form):  
    image = forms.FileField() # for creating file input  
    # date_added = forms.DateField(label="Date")
    # date = forms.DateField(label="Date")
    amount = forms.DecimalField(label = "Amount")
    image = forms.FileField()
    notes = forms.Textarea()
    expense = forms.TextInput()