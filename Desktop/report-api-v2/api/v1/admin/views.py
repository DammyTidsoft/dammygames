from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.models import Entity
from api.serializer import EntitySerializer
from api.v1.mixin import BaseAdminView


class EntitiesView(BaseAdminView):
    serializer_class = EntitySerializer
    queryset = Entity.objects.active()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EntityView(BaseAdminView):
    serializer_class = EntitySerializer
    queryset = Entity.objects.active()

    def get_object(self):
        return get_object_or_404(self.get_queryset(), slug=self.kwargs.get("slug"))

    def get(self, request, *args, **kwargs):
        entity = self.get_object()
        serializer = EntitySerializer(entity)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        entity = self.get_object()
        serializer = EntitySerializer(entity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
