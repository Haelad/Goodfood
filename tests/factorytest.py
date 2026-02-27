import factory
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.goodfood.models import Categories, Goods


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categories

    cat = factory.Faker("word")  # случайное слово как имя категории


class GoodsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goods

    name = factory.Faker("word")  # случайное название товара
    desc = factory.Faker("text")
    photo = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    category = factory.SubFactory(CategoryFactory)
    slugify_name = factory.Sequence(lambda n: f"product-{n}")
