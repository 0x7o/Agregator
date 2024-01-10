from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models, indexes


class ArticleViewSet(ModelViewSet):
    """
    Получение всех статей в БД по страницам.
    """

    queryset = models.Article.objects.all().order_by("-date")
    serializer_class = serializers.ArticleSerializer


class ArticleCreateView(APIView):
    """
    Добавление статей (одной или нескольких) в БД через ключ доступа.
    """

    def post(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            articles = []
            for item in request.data:
                serializer = serializers.ArticleSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    articles.append(serializer.data)
                else:
                    return Response(serializer.errors, status=400)
            return Response(articles, status=201)
        else:
            serializer = serializers.ArticleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class SearchArticle(APIView):
    serializer_class = serializers.ArticleSerializer
    document_class = indexes.ArticleDocument

    def get(self, request, query):
        search = self.document_class.search().query("multi_match", query=query, fields=['title', 'text', 'url'],
                                                    fuzziness='AUTO')
        return Response(self.serializer_class(search.to_queryset(), many=True).data)
