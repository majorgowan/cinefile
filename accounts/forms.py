from django import forms
from .models import JUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
    }
    username = forms.CharField(label="Username",
                               help_text="no spaces")
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="reenter same password")
    email = forms.CharField(label="Email address",
                            widget=forms.EmailInput)

    class Meta:
        model = JUser
        fields = ("username", "password1", "password2", "email")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user