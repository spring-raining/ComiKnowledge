# -*- coding: utf-8 -*-

from django import forms
import re

from ck.models import CircleKnowledgeData, CircleKnowledge
import src
from src.utils import generate_rand_str

re_twitter = re.compile('^https?://(www\.)?twitter.com/\w+$')
re_pixiv = re.compile('^http://(www\.)?pixiv\.net/member\.php\?id=\d+$')
re_url = re.compile('^https?://')
class CircleRegisterForm(forms.ModelForm):
    block_choices = [("", "---------")]
    for k, v in src.BLOCK_ID.items():
        block_choices.append((k, v))
    block_id = forms.ChoiceField(choices=block_choices)
    space_number = forms.IntegerField()
    pen_name = forms.CharField(required=False)
    url = forms.URLField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), max_length=4000, required=False)
    twitter_url = forms.CharField(max_length=256, required=False)
    pixiv_url = forms.CharField(max_length=256, required=False)

    class Meta:
        model = CircleKnowledgeData
        fields = ("day", "block_id", "space_number", "space_number_sub", "circle_name", "pen_name", "url",
                  "description", "twitter_url", "pixiv_url")

    def clean_space_number(self):
        try:
            if int(self.cleaned_data["space_number"]) < 1 \
            or int(self.cleaned_data["space_number"])\
                            > src.SPACE_NUMBER[int(self.cleaned_data["day"])][int(self.cleaned_data["block_id"])]:
                raise forms.ValidationError("Invalid space number")
            return int(self.cleaned_data["space_number"])
        except KeyError:
            raise forms.ValidationError("Space number must fill")
        except IndexError:
            raise forms.ValidationError("Invalid space number")

    def clean_url(self):
        if self.cleaned_data["url"] and not re_url.match(self.cleaned_data["url"]):
            raise forms.ValidationError("Invalid URL")
        return self.cleaned_data["url"]

    def clean_twitter_url(self):
        if self.cleaned_data["twitter_url"] and not re_twitter.match(self.cleaned_data["twitter_url"]):
            raise forms.ValidationError("Invalid Twitter URL")
        return self.cleaned_data["twitter_url"]

    def clean_pixiv_url(self):
        if self.cleaned_data["pixiv_url"] and not re_pixiv.match(self.cleaned_data["pixiv_url"]):
            raise forms.ValidationError("Invalid Pixiv URL")
        return self.cleaned_data["pixiv_url"]
