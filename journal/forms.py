from django import forms
from .models import Viewing, Film


class ViewingFormCinema(forms.ModelForm):
    """
    A form that creates a new Viewing instance.
    """
    error_messages = {
        "invalid_date": "The date is invalid.",
    }
    title = forms.CharField(label="Film")
    date = forms.DateField(label="Date",
                           widget=forms.DateInput(
                               format="%d/%m/%Y",
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
    field_order = ["title", "date", "location",
                   "cinema", "spoilers", "comments",
                   "private"]

    class Meta:
        model = Viewing
        fields = ("date", "location", "cinema",
                  "comments", "spoilers", "private")

    def save(self, commit=False):
        viewing = Viewing()
        if commit:
            viewing.save()
        return viewing
