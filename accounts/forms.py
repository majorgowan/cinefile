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
    username = forms.CharField(label="Username (no spaces)")
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput)
    email = forms.CharField(label="Email address",
                            widget=forms.EmailInput)
    displayname = forms.CharField(label="Display Name")
    private = forms.BooleanField(label="Make Cinefile private",
                                 initial=False,
                                 required=False)

    class Meta:
        model = JUser
        fields = ("username", "password1", "password2",
                  "email", "displayname", "private")

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


class SettingsForm(forms.ModelForm):
    """
    For customizing user preferences
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get("instance")

    error_messages = {
        "invalid_username": "username cannot contain spaces.",
        "username_exists": "user with that name exists.",
    }

    username = forms.CharField(label="Username")
    email = forms.CharField(label="Email address",
                            widget=forms.EmailInput)
    displayname = forms.CharField(label="Display Name")
    private = forms.BooleanField(label="Make Cinefile private",
                                 required=False)

    class Meta:
        model = JUser
        fields = ("username", "email", "displayname", "private")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if " " in username:
            raise forms.ValidationError(
                self.error_messages["invalid_username"],
                code="invalid_username"
            )
        if username != self.instance.username:
            if JUser.objects.filter(username=username).exists():
                raise forms.ValidationError(
                    self.error_messages["username_exists"],
                    code="username_exists"
                )
        return self.cleaned_data.get("username")

    def save(self, commit=True):
        user = self.instance
        user.username = self.cleaned_data.get("username")
        user.displayname = self.cleaned_data.get("displayname")
        user.email = self.cleaned_data.get("email")
        user.private = self.cleaned_data.get("private")
        if commit:
            user.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    """
    For changing password
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get("instance")

    error_messages = {
        "wrong_password": "Old password incorrect",
        "password_mismatch": "Passwords do not match.",
    }

    old_password = forms.CharField(label="Old Password",
                                   widget=forms.PasswordInput(
                                       attrs={"style": "margin: 30px 0"}
                                   ))
    password1 = forms.CharField(label="New Password",
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm New Password",
                                widget=forms.PasswordInput)

    class Meta:
        model = JUser
        fields = ("old_password", "password1", "password2",)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.instance.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages["wrong_password"],
                code="wrong_password",
            )
        return old_password

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
        user = self.instance
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class DeleteAccountForm(forms.Form):
    confirm = forms.BooleanField(label="Confirm delete account",
                                 initial=False, required=True)
