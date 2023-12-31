from django.contrib import admin

from api.models import Entity, Attribute


# Register your models here.


class AttributeInline(admin.TabularInline):
    model = Attribute
    extra = 1
    readonly_fields = ("created_at", "updated_at")


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "active")
    search_fields = ("name", "slug")
    readonly_fields = ("created_at", "updated_at")
    filter_horizontal = ("owners",)
    inlines = (AttributeInline,)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "data_type", "active")
    search_fields = ("name", "slug")
    readonly_fields = ("created_at", "updated_at")
