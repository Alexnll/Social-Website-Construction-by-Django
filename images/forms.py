from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image

from urllib import request

class ImageCreateForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

        # clean form fields
        def clean_url(self):
            url = self.cleaned_data['url']
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('.', 1)[1].lower()

            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')

            return url

        # override the save() to save the after-valid data
        def save(self, force_insert=False, force_update=False, commit=True):
            image = super(ImageCreateForm, self).save(commit=False)
            image_url = self.cleaned_data['url']
            image_name = '{}.{}'.format(slugify(image.title), image_url.rsplit('.',1)[1].lower())

            # download image
            response = request.urlopen(image_url)
            image.image.save(image_name, ContentFile(response.read()), save=False)

            if commit:
                image.save()
            return image