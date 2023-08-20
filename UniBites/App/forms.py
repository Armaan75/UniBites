from django import forms

class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16, label='Card Number',  widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    expiration_date = forms.DateField(label='Expiration Date',   widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, label='CVV',   widget=forms.TextInput(attrs={'placeholder': '123'}))


    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['card_number'].help_text = ''
        self.fields['expiration_date'].help_text = ''
        self.fields['cvv'].help_text = ''
