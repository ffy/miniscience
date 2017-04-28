from datetime import datetime, timedelta

from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Author, Publication
from .serializers import AuthorSerializer, PublicationSerializer
from .utils import do_request


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer


@api_view(['GET', 'POST'])
def author_publications(request, author_id):
    if request.method == 'GET':
        publications = Publication.objects.filter(authors__id=author_id)
        serializer = PublicationSerializer(publications, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PublicationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(authors=[author_id])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def author_publication(request, author_id, publication_id):
    try:
        author = Author.objects.get(id=author_id)
        publication = Publication.objects.get(id=publication_id)
    except (Author.DoesNotExist, Publication.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    publication.authors.remove(author)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def importer(request):
    if request.method == 'GET':
        queryset = Publication.objects.filter(imported_datetime__gt=timezone.now() - timedelta(minutes=30))
        serializer = PublicationSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        faculty = request.data['faculty'].upper()
        do_request("secret" + faculty + "url")
        return Response(status=status.HTTP_201_CREATED)