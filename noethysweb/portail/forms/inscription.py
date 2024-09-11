from core.data import data_civilites
from core.models import Utilisateur
from core.utils.utils_captcha import CaptchaField, CustomCaptchaTextInput
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _


class InscriptionFamilleForm(SetPasswordForm):
    civilite = forms.ChoiceField(
        choices=data_civilites.GetListeCivilitesByCategory("ADULTE")
    )
    nom = forms.CharField(label=_("Nom"), max_length=200)
    prenom = forms.CharField(label=_("Prénom"), max_length=200)
    mail = forms.EmailField(label=_("Email personnel"), max_length=300)
    captcha = CaptchaField(
        label=_("Recopiez le code de sécurité ci-contre"), widget=CustomCaptchaTextInput
    )

    def __init__(self, *args, **kwargs):
        # First None arg is for user
        super().__init__(None, *args, **kwargs)

        # Move new_passwords fileds to the end of self.fields
        # to have to other fields in clean_new_password2
        self.fields["new_password1"] = self.fields.pop("new_password1")
        self.fields["new_password2"] = self.fields.pop("new_password2")

        for name, field in self.fields.items():
            if not field.widget.is_hidden:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label

            if name == "nom":
                field.widget.attrs["autocomplete"] = "family-name"
            elif name == "prenom":
                field.widget.attrs["autocomplete"] = "given-name"
            # elif name == "new_password1" or name == "new_password2":
            #     field.widget.attrs["autocomplete"] = "new-password"

    def clean_new_password2(self):
        # Simulate user
        self.user = Utilisateur(
            last_name=self.cleaned_data["nom"],
            first_name=self.cleaned_data["prenom"],
            email=self.cleaned_data["mail"],
        )
        password = super().clean_new_password2()
        self.user = None
        return password
