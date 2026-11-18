from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, ResumeRecord

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80, required=True)
    class Meta:
        model = User
        fields = ("first_name", "username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("stream", "college", "target_role")
        widgets = {f: forms.TextInput(attrs={"class":"form-control"}) for f in ("college","target_role")}

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = ResumeRecord
        fields = ("file",)
        widgets = {"file": forms.ClearableFileInput(attrs={"class":"form-control", "accept":".pdf,.docx"})}
    def clean_file(self):
        f = self.cleaned_data["file"]
        if f.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be 5 MB or less.")
        if not f.name.lower().endswith((".pdf", ".docx")):
            raise forms.ValidationError("Upload a PDF or DOCX file.")
        return f
