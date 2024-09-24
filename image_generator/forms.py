from django import forms


class ImagePromptForm(forms.Form):
    prompt = forms.CharField(label='Enter your prompt', max_length=500,
                             widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe your campaign...'}))
