from django import forms
from .models import Notebook, Note
from taggit.forms import TagWidget

class CreateNotebookForm(forms.ModelForm):
    class Meta:
        model = Notebook
        fields = ['title']

class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'notebook', 'tags']
    tags = forms.CharField(
        required=True,
        widget=TagWidget(),
        label="Tags (comma separated)"
    )
    notebook = forms.ModelChoiceField(queryset=Notebook.objects.none(), label="Select a Notebook", required=False)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'trix-editor', 'input': 'trix-input'}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['notebook'].queryset = Notebook.objects.filter(author=user).exclude(slug='uncategorized')