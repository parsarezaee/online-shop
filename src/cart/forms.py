from django import forms
from django.utils.translation import gettext_lazy as _



PRODUCT_QUANTIFY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantify = forms.TypedChoiceField(
        choices=PRODUCT_QUANTIFY_CHOICES,
        coerce=int,
        label=_('Quantify')
    )
    override = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
