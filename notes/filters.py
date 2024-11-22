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
    sort_by_created = django_filters.ChoiceFilter(
        label='Sort by Created Time',
        choices=[('created', 'Old to First'), ('-created', 'First to Old')],
        method='filter_sort_by_created'
    )
    sort_by_modified = django_filters.ChoiceFilter(
        label='Sort by Modified Time',
        choices=[('modified', 'Old to First'), ('-modified', 'First to Old')],
        method='filter_sort_by_modified'
    )
    sort_by_title = django_filters.ChoiceFilter(
        label='Sort by Title',
        choices=[('title', 'A to Z'), ('-title', 'Z to A')],
        method='filter_sort_by_title'
    )
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

    class Meta:
        model = Note
        fields = ['notebook', 'tags', 'sort_by_created', 'sort_by_modified', 'sort_by_title', 'created_after', 'created_before', 'modified_after', 'modified_before']

    def __init__(self, data=None, queryset=None, *args, **kwargs):
        user = kwargs.pop('user', None) 
        pk = kwargs.pop('pk', None)
        super().__init__(data, queryset=queryset, *args, **kwargs)
        if pk is not None:
            del self.filters['notebook']
        if user and 'notebook' in self.filters:
            self.filters['notebook'].queryset = Notebook.objects.filter(author=user)

    def filter_sort_by_created(self, queryset, name, value):
        """Custom method to sort by created time."""
        return queryset.order_by(value)

    def filter_sort_by_modified(self, queryset, name, value):
        """Custom method to sort by modified time."""
        return queryset.order_by(value)

    def filter_sort_by_title(self, queryset, name, value):
        """Custom method to sort by title."""
        return queryset.order_by(value)

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
    
    sort_by_created = django_filters.ChoiceFilter(
        label='Sort by Created Time',
        choices=[('created', 'Old to First'), ('-created', 'First to Old')],
        method='filter_sort_by_created'
    )
    sort_by_modified = django_filters.ChoiceFilter(
        label='Sort by Modified Time',
        choices=[('modified', 'Old to First'), ('-modified', 'First to Old')],
        method='filter_sort_by_modified'
    )
    sort_by_title = django_filters.ChoiceFilter(
        label='Sort by Title',
        choices=[('title', 'A to Z'), ('-title', 'Z to A')],
        method='filter_sort_by_title'
    )
    
    # New filters for created date
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

    # New filters for modified date
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

    class Meta:
        model = Notebook
        fields = ['title', 'sort_by_created', 'sort_by_modified', 'sort_by_title', 'created_after', 'created_before', 'modified_after', 'modified_before']

    def filter_sort_by_created(self, queryset, name, value):
        """Custom method to sort by created time."""
        return queryset.order_by(value)

    def filter_sort_by_modified(self, queryset, name, value):
        """Custom method to sort by modified time."""
        return queryset.order_by(value)

    def filter_sort_by_title(self, queryset, name, value):
        """Custom method to sort by title."""
        return queryset.order_by(value)
