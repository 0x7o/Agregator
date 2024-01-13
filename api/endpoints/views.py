from transliterate import translit
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers, models, indexes
import uuid


class ArticleViewSet(ModelViewSet):
    """
    Получение всех статей в БД по страницам.
    """

    queryset = models.Article.objects.all().order_by("-date")
    serializer_class = serializers.ArticleSerializer


class ArticleDetailView(APIView):
    document_class = indexes.ArticleDocument

    def get(self, request, friendly_url):
        try:
            article = models.Article.objects.get(friendly_url=friendly_url)
            serializer = serializers.ArticleSerializer(article)
            search = self.document_class.search().query(
                "more_like_this",
                like=article.text,
                min_term_freq=1,
                fields=["text", "title"],
            )
            similar_articles = search.execute()
            similar_articles_serializer = serializers.ArticleSerializer(
                similar_articles, many=True
            )
            data = serializer.data
            data["similar_articles"] = similar_articles_serializer.data

            return Response(data)
        except models.Article.DoesNotExist:
            return Response({"error": "Article not found"}, status=404)


class ArticleCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data if isinstance(request.data, list) else [request.data]
        articles = []
        for item in data:
            item["friendly_url"] = self.generate_unique_friendly_url(item)
            serializer = serializers.ArticleSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                articles.append(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        return Response(articles if len(articles) > 1 else articles[0], status=201)

    def generate_unique_friendly_url(self, data):
        friendly_url = translit(data["title"], "ru", reversed=True).replace(" ", "-").lower()
        while models.Article.objects.filter(friendly_url=friendly_url).exists():
            friendly_url += '-' + str(uuid.uuid4())[:8]
        return friendly_url


class SearchArticle(APIView):
    serializer_class = serializers.ArticleSerializer
    document_class = indexes.ArticleDocument

    def get(self, request, query):
        search = self.document_class.search().query(
            "multi_match",
            query=query,
            fields=["title", "text", "url"],
            fuzziness="AUTO",
        )
        return Response(self.serializer_class(search.to_queryset(), many=True).data)
