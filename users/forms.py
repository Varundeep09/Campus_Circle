
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile, AlumniVerificationRequest

# Form for alumni verification request
class AlumniVerificationRequestForm(forms.ModelForm):
    class Meta:
        model = AlumniVerificationRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'placeholder': 'Optional: Add a note for the admin', 'rows': 3}),
        }


class CustomUserCreationForm(UserCreationForm):
    # Exclude 'admin' from registration choices
    role = forms.ChoiceField(
        choices=[c for c in User.ROLE_CHOICES if c[0] != 'admin'],
        required=True
    )

    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'college', 'graduation_year', 'profile_image', 'resume', 'linkedin_url', 'github_url']