from django import forms
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div

from main.models import Hours

class HoursForm(forms.ModelForm):
    class Meta:
        model = Hours
        fields = ["date", "project", "quantity", "notes", "user"]
        widgets = {"user": forms.HiddenInput(),
                   "date": forms.DateInput(attrs={"type":"date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = ("POST")
        self.helper.form_action = reverse("main:hours_create")
        self.helper.form_class = "form-inline"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Div(
                Field("date"),
                Field("project", wrapper_class="ml-2"),
                Field("quantity", wrapper_class="ml-2"),
                Field("notes", wrapper_class="ml-2 mr-2"),
                Field("user"),
                Submit("submit", "Submit"),
                css_class="form-row"))
                


