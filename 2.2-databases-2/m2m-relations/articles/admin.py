from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        total_forms = 0
        unique_tags = set()
        is_main_count = 0
        for form in self.forms:
            if not form.cleaned_data or form.cleaned_data['DELETE']:
                continue
            total_forms += 1
            unique_tags.add(form.cleaned_data['tag'])
            if form.cleaned_data.get('is_main'):
                is_main_count += 1
        if is_main_count > 1:
            raise ValidationError("Основным может быть только один раздел")
        if total_forms > len(unique_tags):
            raise ValidationError("Выбраны повторяющие разделы")
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

