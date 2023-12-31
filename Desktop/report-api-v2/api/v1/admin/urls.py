from django.urls import path

from .views import EntityView, EntitiesView

urlpatterns = [
    path("entities/", EntitiesView.as_view(), name="entities"),
    path("entity/<int:pk>/", EntityView.as_view(), name="entity"),
]
