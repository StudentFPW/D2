# ----------------------------------------------------------------------------------------------------------------------

# Задание выполнено студентом (Leonids Jofe) из школы SkillFactory, курс Full-stack python developer, класс FPW-104

# ----------------------------------------------------------------------------------------------------------------------

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


########################################################################################################################

class Author(models.Model):
    """
    Модель, содержащая объекты всех авторов.
    """

    one_user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.SmallIntegerField(default=0)

    def update_rating(self):  # Вариант из видео ↓
        postRat = self.post_set.aggregate(postRating=Sum("rating"))
        pRat = 0
        pRat += postRat.get("postRating")

        commentRat = self.one_user.comment_set.aggregate(commentRating=Sum("rating"))
        cRat = 0
        cRat += commentRat.get("commentRating")

        self.rating = pRat * 3 + cRat
        self.save()
    # Вариант из видео ↑


########################################################################################################################

class Category(models.Model):
    """
    Имеет единственное поле, название категории.
    """

    name_category = models.CharField(max_length=64, unique=True)


########################################################################################################################

class Post(models.Model):
    """
    Модель, которая создает статьи и новости, которые публикуют пользователи.
    """

    article = 'AT'
    news = 'NW'
    TYPE = [(article, 'Статья'), (news, 'Новость')]

    many_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article_or_news = models.CharField(max_length=2, choices=TYPE, default=article)

    datetime = models.DateTimeField(auto_now_add=True)

    many_category = models.ManyToManyField(Category, through="PostCategory")

    header = models.CharField(max_length=150)

    text = models.TextField()

    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        """
        (Предварительный просмотр) длиной 124 символа.
        """
        return self.text[:123] + "..."


########################################################################################################################

class PostCategory(models.Model):
    """
    Промежуточная модель для связи «многие ко многим»

    1. Поля внешнего ключа в базе данных, которое ссылается на модель Post.

    2. Поле внешнего ключа в базе данных, которое ссылается на модель Category.
    """

    many_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    many_category = models.ForeignKey(Category, on_delete=models.CASCADE)


########################################################################################################################

class Comment(models.Model):
    """
    Модель для комментариев.
    """

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    datetime = models.DateTimeField(auto_now_add=True)

    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
