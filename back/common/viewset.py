import typing as t

from django.db.models import Model
from rest_framework import status
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet


class RequestPayloadSerializerDict(t.TypedDict):
    """
    Dict to describe request serializers for allowed actions
    """

    create: t.NotRequired[Serializer]
    update: t.NotRequired[Serializer]
    partial_update: t.NotRequired[Serializer]


class ResponsePayloadSerializerDict(t.TypedDict):
    """
    Dict to describe response serializers for allowed actions
    """

    create: t.NotRequired[Serializer]
    update: t.NotRequired[Serializer]
    partial_update: t.NotRequired[Serializer]
    list: t.NotRequired[Serializer]
    retrieve: t.NotRequired[Serializer]


class SeparateRequestAndResponseSerializerListModelMixin(ListModelMixin):
    def list(self, request, *args, **kwargs):
        """
        Overridden method to use response serializer
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_response_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_response_serializer(queryset, many=True)
        return Response(serializer.data)


class SeparateRequestAndResponseSerializerCreateModelMixin(CreateModelMixin):
    """
    Adjust rest_framework's CreateModelMixin to use different serializers
    for deserializing request payload and serializing response payload
    """

    def create(self, request, *args, **kwargs):
        """
        Overridden method to use different serializers for request and response serialization
        """
        request_serializer = self.get_request_serializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        instance = self.perform_create(request_serializer)
        response_serializer = self.get_response_serializer(instance=instance)
        headers = self.get_success_headers(request.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: Serializer) -> Model:
        """
        We need to return instance to serialize by different serializer
        :param serializer: serializer for validated data for creation
        :return: instance created
        """
        serializer.save()
        return serializer.instance


class SeparateRequestAndResponseSerializersGenericViewSet(GenericViewSet):
    """
    Adjust rest_framework's GenericViewSet to use different serializers
    for deserializing request payload and serializing response
    """

    request_serializers_by_action: RequestPayloadSerializerDict = {}
    response_serializers_by_action: ResponsePayloadSerializerDict = {}

    def get_serializer_class(self):
        """
        A little workaround for debug version, used for renderers to render debug form to send data
        :return: serializer for request payload
        """
        return self.get_request_serializer_class()

    def get_request_serializer_class(self):
        serializer = self.request_serializers_by_action.get(self.action)
        if serializer is None:
            return self.serializer_class
        return serializer

    def get_request_serializer(self, *args, **kwargs):
        serializer_class = self.get_request_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def get_response_serializer_class(self):
        serializer = self.response_serializers_by_action.get(self.action)
        if serializer is None:
            return self.serializer_class
        return serializer

    def get_response_serializer(self, *args, **kwargs):
        serializer_class = self.get_response_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
