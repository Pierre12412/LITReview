from django import forms

class BookArticle(forms.Form):
    titre = forms.CharField(max_length=20,required=True)
    description = forms.CharField(max_length=1200, required=True,widget=forms.Textarea())
    image = forms.ImageField()

class ReviewForm(forms.Form):
    titre = forms.CharField(max_length=20,required=True)
    note = forms.IntegerField(max_value=5,min_value=1,required=True)
    description = forms.CharField(max_length=1200, required=True, widget=forms.Textarea())