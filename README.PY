# ----------------------------------------------------------------------------------------------------------------------

# Создать двух пользователей (с помощью метода User.objects.create_user('username')):

from news.models import *

user_1 = User.objects.create_user('username_1')
user_2 = User.objects.create_user('username_2')

# ----------------------------------------------------------------------------------------------------------------------

# Создать два объекта модели Author, связанные с пользователями:

author_1 = Author.objects.create(one_user=user_1)
author_2 = Author.objects.create(one_user=user_2)

# ----------------------------------------------------------------------------------------------------------------------

# Добавить 4 категории в модель Category:

category_1 = Category.objects.create(name_category="Спорт")
category_2 = Category.objects.create(name_category="Политика")
category_3 = Category.objects.create(name_category="Образование")
category_4 = Category.objects.create(name_category="Наука и технологии")

# ----------------------------------------------------------------------------------------------------------------------

# Добавить 2 статьи и 1 новость:

article_1 = Post.objects.create(many_author=author_1, header="Спорт",
                                text="""Более узкое определение спорта даёт «Большая олимпийская энциклопедия» 2006 года.""")

article_2 = Post.objects.create(many_author=author_2, article_or_news=Post.article, header="Наука и технологии",
                                text="""Более узкое определение спорта даёт «Большая олимпийская энциклопедия» 2006 года.""")

news_1 = Post.objects.create(many_author=author_1, article_or_news=Post.news, header="Политика",
                             text="""Более узкое определение спорта даёт «Большая олимпийская энциклопедия» 2006 года.""")

# ----------------------------------------------------------------------------------------------------------------------

# Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий):

article_1.many_category.add(category_4)
article_1.many_category.add(category_2)

article_2.many_category.add(category_2)
article_2.many_category.add(category_1)

news_1.many_category.add(category_1)
news_1.many_category.add(category_3)

# ----------------------------------------------------------------------------------------------------------------------

# Создать как минимум 4 комментария к разным объектам модели Post
# (в каждом объекте должен быть как минимум один комментарий):

comment_1 = Comment.objects.create(comment_post=article_1, comment_user=user_1, text="Здоровее на первом месте !")
comment_2 = Comment.objects.create(comment_post=article_2, comment_user=user_2, text="Привет !")

comment_3 = Comment.objects.create(comment_post=news_1, comment_user=user_1, text="Добрый день !")
comment_3 = Comment.objects.create(comment_post=news_1, comment_user=user_1, text="OXOXO !")

# ----------------------------------------------------------------------------------------------------------------------

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов:

article_1.like()
article_1.like()
article_1.like()
article_2.like()
article_2.like()
article_2.like()
article_2.like()
comment_1.like()
comment_1.like()
comment_1.like()
comment_1.like()
comment_1.like()
comment_3.like()
comment_3.like()
comment_3.like()
comment_3.like()
comment_3.like()
comment_3.like()
news_1.like()
news_1.like()
news_1.like()
news_1.like()
news_1.like()
news_1.like()

article_1.dislike()
comment_1.dislike()
news_1.dislike()

# ----------------------------------------------------------------------------------------------------------------------

# Обновить рейтинги пользователей:

# суммарный рейтинг каждой статьи автора;
Post.objects.values('article_or_news', 'many_author__one_user__username').annotate(rating=Sum('rating'))

# суммарный рейтинг всех комментариев автора;
Comment.objects.values('comment_user__username').annotate(rating=Sum('rating'))

# суммарный рейтинг всех комментариев к статьям автора.
Comment.objects.values("comment_post__article_or_news", 'comment_user__username').annotate(rating=Sum('rating'))

# Извините, пожалуйста, тут я не додумался как написать метод update_rating(), вижу такой способ ↑.

# В следуишии модуль пойду с кодом из видео, уже начал изучать Aggregation :)

# Для update_rating(): ↓ Вариант из видео ↓

author_1.update_rating()
author_1.rating

author_2.update_rating()
author_2.rating

# ↑ Вариант из видео ↑

# ----------------------------------------------------------------------------------------------------------------------

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта):

Post.objects.all().order_by('rating').values('many_author__one_user__username', 'rating').last()

# ----------------------------------------------------------------------------------------------------------------------

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи,
# основываясь на лайках/дислайках к этой статье:

Post.objects.all().order_by('rating').values("datetime", "many_author__one_user__username", "rating", "header",
                                             "text").last()
article_1.preview()

# ----------------------------------------------------------------------------------------------------------------------

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье:

Comment.objects.all().order_by('rating').values("datetime", "comment_user__username", "rating", "text").last()

# ----------------------------------------------------------------------------------------------------------------------

# С последними 4мя пунктами получилось не совсем как надо, перепробовал все, если есть возможность подскажите
# пожалуйста правилнии ответ. (●'◡'●)

# Благодарю за внимание :)

# P. S ВСЕ ОСТАЛНОЕ ПОНЯЛ ПРЕКРАСНО :D
