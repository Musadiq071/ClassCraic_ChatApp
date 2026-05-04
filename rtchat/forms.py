from django.forms import ModelForm
from django import forms
from .models import GroupMessage, ChatGroup


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body', 'file']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add message ...',
                'class': 'p-4 text-black w-full',
                'maxlength': '300',
                'autofocus': True,
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'text-white'
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        # if no file, it wont validate 
        if not file:
            return file

        #Only mentioned image format and PDFs acceptable.
        allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf']
        ext = file.name.split('.')[-1].lower()

        if ext not in allowed_extensions:
            raise forms.ValidationError(
                "Only JPG, JPEG, PNG, GIF, and PDF files are allowed."
            )

        #Max file size 5MB
        max_size = 5 * 1024 * 1024  # 5 MB
        if file.size > max_size:
            raise forms.ValidationError("File size must be under 5MB.")

        return file

    def clean(self):
        cleaned_data = super().clean()

        # If already errors return only clean data
        if self.errors:
            return cleaned_data

        body = (cleaned_data.get('body') or '').strip()
        file = cleaned_data.get('file')

        #Avoids sending empty messages
        if not body and not file:
            raise forms.ValidationError("Please add a message or choose a file.")

        return cleaned_data

class CreateClassGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['group_name']


class JoinClassForm(forms.Form):
    code = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter class code...',
            'class': 'p-3 text-black'
        })
    )