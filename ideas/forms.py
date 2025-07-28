from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
            }),
        }

from django import forms
from .models import CustomUser
from ideas.models import Tag

class EditProfileForm(forms.ModelForm):
    interest_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'bio', 'interest_tags', 'profile_picture', 'twitter', 'instagram', 'linkedin']
