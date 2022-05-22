from django_filters import rest_framework as filters


class BaseCrmFilter(filters.FilterSet):
    is_active = filters.ChoiceFilter(label='Is active', empty_label='Not selected', method='is_active_filter',
                                     choices=[('true', 'Active'), ('false', 'Not active')])

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(archived_stamp__isnull=False)
        return queryset
