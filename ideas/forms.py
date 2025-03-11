from ckeditor.widgets import CKEditorWidget
from django import forms

from .models import Post, Tag


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(config_name="default"))  # CKEditor for rich text
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']