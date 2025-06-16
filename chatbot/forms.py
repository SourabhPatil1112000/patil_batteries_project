from django import forms

class ChatForm(forms.Form):
    user_input = forms.CharField(
        label='Your Message',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ask about batteries...'
        }),
        max_length=500
    )