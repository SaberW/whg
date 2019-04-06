from django import forms
from django.db import models

from main.models import Comment
from main.choices import COMMENT_TAGS
from bootstrap_modal_forms.forms import BSModalForm

class CommentModalForm(BSModalForm):
    
    place_id = forms.CharField(widget=forms.TextInput, label='WHG record id')    
    class Meta:
        model = Comment
        # fields: user, place_id, tag, note, created
        fields = ['tag', 'note','place_id']
        hidden_fields = ['created']
        #exclude = ['user','place_id']
        exclude = ['user']
        widgets = {
            'place_id': forms.TextInput(),
            'tag': forms.RadioSelect(choices=COMMENT_TAGS),
            'note': forms.Textarea(attrs={
                'rows':2,'cols': 30,'class':'textarea',
                'placeholder':'what up? (briefly'})
        }
        
    #def __init__(self, *args, **kwargs):
        #self._user = kwargs.pop('user')
        #super(ReviewForm, self).__init__(*args, **kwargs)    