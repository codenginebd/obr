from django import forms

from book_rental.models.author import Author
from book_rental.models.book_publisher import BookPublisher
from book_rental.models.language import BookLanguage
from book_rental.models.sales.book import Book
from bradmin.forms.base_model_form import BRBaseModelForm
from bradmin.forms.category_forms import CategoryModelChoiceField
from bradmin.forms.fields.image_file_field import BRFormImageField
from ecommerce.models.sales.category import ProductCategory


class AdminBookForm(BRBaseModelForm):
    def __init__(self, *args, **kwargs):
        super(AdminBookForm, self).__init__(*args, **kwargs)

    categories = CategoryModelChoiceField(label="Select Category", required=True, queryset=ProductCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    publisher = CategoryModelChoiceField(label="Select Publisher", required=True, queryset=BookPublisher.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    authors = CategoryModelChoiceField(label="Select Author", required=False, queryset=Author.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    language = CategoryModelChoiceField(label="Select Book Language", required=False, queryset=BookLanguage.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    images = BRFormImageField()

    class Meta:
        model = Book
        fields = ['title', 'title_2', 'subtitle', 'subtitle_2', 'isbn', 'isbn13', 'edition', 'description', 'description_2', "show_2",
                  "is_active", "categories", "publisher", "authors", "page_count", "publish_date", "sale_available",
                  "rent_available", "tags", "images"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'title_2': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle_2': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control'}),
            'publish_date': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'description_2': forms.Textarea(attrs={'class': 'form-control'}),
            'show_2': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            "tags": forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Title",
            'title_2': "Title 2",
            'subtitle': "Subtitle(Optional)",
            'subtitle_2': "Subtitle 2(Optional)",
            'description': 'Description',
            'description_2': 'Description 2',
            'show_2': "Show Bangla",
            'is_active': "Active",
            "tags": "Keywords",
            "images": "Image",
            "publish_date": "Publish Date"
        }
        fields_required = ['title', 'description']
