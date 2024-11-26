from taggit.models import Tag
import django_filters
from django import forms
from .models import Note, Notebook

class NoteFilter(django_filters.FilterSet):
    notebook = django_filters.ModelChoiceFilter(
        queryset=Notebook.objects.none(),
        empty_label="All Notebooks"
    )
    tags = django_filters.CharFilter(method='filter_tags')
    created_after = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Created After',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    created_before = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='Created Before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    modified_after = django_filters.DateFilter(
        field_name='modified',
        lookup_expr='gte',
        label='Modified After',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    modified_before = django_filters.DateFilter(
        field_name='modified',
        lookup_expr='lte',
        label='Modified Before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    order_by = django_filters.OrderingFilter(
        label='Sort by',
        choices=[
            ('created', 'Created Time (Old to New)'),
            ('-created', 'Created Time (New to Old)'),
            ('modified', 'Modified Time (Old to New)'),
            ('-modified', 'Modified Time (New to Old)'),
            ('title', 'Title (A to Z)'),
            ('-title', 'Title (Z to A)'),
        ]
    )

    class Meta:
        model = Note
        fields = ['notebook', 'tags', 'created_after', 'created_before', 'modified_after', 'modified_before', 'order_by']

    def __init__(self, data=None, queryset=None, *args, **kwargs):
        user = kwargs.pop('user', None) 
        pk = kwargs.pop('pk', None)
        super().__init__(data, queryset=queryset, *args, **kwargs)
        if pk is not None:
            del self.filters['notebook']
        if user and 'notebook' in self.filters:
            self.filters['notebook'].queryset = Notebook.objects.filter(author=user)

    def filter_tags(self, queryset, name, value):
        """Custom method to filter tags by title or slug."""
        try:
            tag = Tag.objects.get(name=value) 
            return queryset.filter(tags=tag)
        except Tag.DoesNotExist:
            pass 
        try:
            tag = Tag.objects.get(slug=value)  
            return queryset.filter(tags=tag)
        except Tag.DoesNotExist:
            return queryset.none()

class NotebookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Search by Title')
    created_after = django_filters.DateFilter(
        field_name='created',
        lookup_expr='gte',
        label='Created After',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    created_before = django_filters.DateFilter(
        field_name='created',
        lookup_expr='lte',
        label='Created Before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    modified_after = django_filters.DateFilter(
        field_name='modified',
        lookup_expr='gte',
        label='Modified After',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    modified_before = django_filters.DateFilter(
        field_name='modified',
        lookup_expr='lte',
        label='Modified Before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    order_by = django_filters.OrderingFilter(
        label='Sort by',
        choices=[
            ('created', 'Created Time (Old to New)'),
            ('-created', 'Created Time (New to Old)'),
            ('modified', 'Modified Time (Old to New)'),
            ('-modified', 'Modified Time (New to Old)'),
            ('title', 'Title (A to Z)'),
            ('-title', 'Title (Z to A)'),
        ]
    )

    class Meta:
        model = Notebook
        fields = ['title', 'created_after', 'created_before', 'modified_after', 'modified_before', 'order_by']