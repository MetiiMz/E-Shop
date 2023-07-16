from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        max_value=100,
        label=False,
        initial=1,
        widget=forms.NumberInput({
            'class': 'form-control',
        })
    )
