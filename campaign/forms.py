from django import forms

class UploadContactsForm(forms.Form):
    file = forms.FileField(label="اختر ملف Excel لرفع جهات الاتصال")
