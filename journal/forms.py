from django import forms
from .models import Viewing, Film
from django.apps import apps


JUser = apps.get_model('accounts', 'JUser')


class ViewingFormCinema(forms.ModelForm):
    """
    A form that creates a new Viewing instance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" in kwargs:
            self.instance = kwargs.get("instance")

    error_messages = {
        "invalid_date": "The date is invalid.",
    }
    title = forms.CharField(label="Film",
                            widget=forms.TextInput(
                                attrs={"readonly": True}
                            ))
    date = forms.DateField(label="Date",
                           widget=forms.DateInput(
                               format="%Y-%m-%d",
                               attrs={"type": "date",
                                      "style": "font-size: 20px;"}
                           ))
    comments = forms.CharField(label="",
                               widget=forms.Textarea(
                                   attrs={"placeholder": "comments",
                                          "style": "padding: 5px; line-height: 1.2;",
                                          "cols": 52,
                                          "rows": 7}
                               ))
    user = forms.Field(label=False,
                       widget=forms.HiddenInput())
    film = forms.Field(label=False,
                       widget=forms.HiddenInput())

    field_order = ["title", "date", "location",
                   "cinema", "spoilers", "comments",
                   "private"]

    class Meta:
        model = Viewing
        fields = ("user", "film", "date", "location", "cinema",
                  "comments", "spoilers", "private")

    def clean_user(self):
        user = JUser.objects.get(id=self.cleaned_data["user"])
        return user

    def clean_film(self):
        film = Film.objects.get(id=self.cleaned_data["film"])
        return film

    def save(self, commit=False, pk=None):
        viewing = self.instance
        viewing.user = self.cleaned_data.get("user")
        viewing.film = self.cleaned_data.get("film")
        viewing.location = self.cleaned_data.get("location")
        viewing.cinema = self.cleaned_data.get("cinema")
        viewing.spoilers = self.cleaned_data.get("spoilers")
        viewing.comments = self.cleaned_data.get("comments")
        viewing.private = self.cleaned_data.get("private")
        if pk is not None:
            viewing.pk = int(pk)
        if commit:
            viewing.save()

        return viewing


class ViewingFormVideo(forms.ModelForm):
    """
    A form that creates a new Viewing instance.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "instance" in kwargs:
            self.instance = kwargs.get("instance")

    error_messages = {
        "invalid_date": "The date is invalid.",
    }
    title = forms.CharField(label="Film",
                            widget=forms.TextInput(
                                attrs={"readonly": True}
                            ))
    date = forms.DateField(label="Date",
                           widget=forms.DateInput(
                               format="%Y-%m-%d",
                               attrs={"type": "date",
                                      "style": "font-size: 20px;"}
                           ))
    video_medium = forms.ChoiceField(label="Video Medium",
                                     choices=[
                                         ("", "-- Select Media Type --"),
                                         ("TV", "TV"),
                                         ("Streaming", "Streaming"),
                                         ("DVD/PPV", "DVD / PPV")
                                     ])
    tv_channel = forms.CharField(label="TV Channel",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={"disabled": True}
                                 ))
    streaming_platform = forms.CharField(label="Streaming Platform",
                                         required=False,
                                         widget=forms.TextInput(
                                             attrs={"disabled": True}
                                         ))
    comments = forms.CharField(label="",
                               widget=forms.Textarea(
                                   attrs={"placeholder": "comments",
                                          "style": "padding: 5px; line-height: 1.2;",
                                          "cols": 52,
                                          "rows": 7}
                               ))
    user = forms.Field(label=False,
                       widget=forms.HiddenInput())
    film = forms.Field(label=False,
                       widget=forms.HiddenInput())

    field_order = ["title", "date", "video_medium",
                   "tv_channel", "streaming_platform",
                   "spoilers", "comments",
                   "private"]

    class Meta:
        model = Viewing
        fields = ("user", "film", "date", "video_medium",
                  "tv_channel", "streaming_platform",
                  "comments", "spoilers", "private")

    def clean_user(self):
        user = JUser.objects.get(id=self.cleaned_data["user"])
        return user

    def clean_film(self):
        film = Film.objects.get(id=self.cleaned_data["film"])
        return film

    def save(self, commit=False, pk=None):
        viewing = self.instance
        viewing.user = self.cleaned_data.get("user")
        viewing.film = self.cleaned_data.get("film")
        viewing.video_medium = self.cleaned_data.get("video_medium")
        viewing.tv_channel = self.cleaned_data.get("tv_channel")
        viewing.streaming_platform = self.cleaned_data.get("streaming_platform")
        viewing.spoilers = self.cleaned_data.get("spoilers")
        viewing.comments = self.cleaned_data.get("comments")
        viewing.private = self.cleaned_data.get("private")
        if pk is not None:
            viewing.pk = int(pk)

        if commit:
            viewing.save()
        return viewing
