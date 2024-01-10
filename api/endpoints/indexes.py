from django_elasticsearch_dsl import Document, Index, fields
from . import models

article_index = Index("aricle")
article_index.settings(
    number_of_shards=1,
    number_of_replicas=0,
)


@article_index.doc_type
class ArticleDocument(Document):
    name = "ArticleIndex"

    class Django:
        model = models.Article
        fields = ["url", "title", "text"]
        auto_refresh = True
