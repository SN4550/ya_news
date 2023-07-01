from http import HTTPStatus
from unittest import skip

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from news.models import News, Comment


User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            title='Заголовок',
            text='Текст')
        # Создаём двух пользователей с разными именами:
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        # От имени одного пользователя создаём комментарий к новости:
        cls.comment = Comment.objects.create(
            text='Текст комментария',
            news=cls.news,
            author=cls.author)

    def test_pages_availability(self):
        # Создаём набор тестовых данных - кортеж кортежей.
        # Каждый вложенный кортеж содержит два элемента:
        # имя пути и позиционные аргументы для функции reverse().
        urls = (
            # Путь для главной страницы не принимает
            # никаких позиционных аргументов,
            # поэтому вторым параметром ставим None.
            ('news:home', None),
            # Путь для страницы новости
            # принимает в качестве позиционного аргумента
            # id записи; передаём его в кортеже.
            ('news:detail', (self.news.pk,)),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None))
        for item in urls:
            name, args = item
            with self.subTest(name=name):
                # Передаём имя и позиционный аргумент в reverse()
                # и получаем адрес страницы для GET-запроса:
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_comment_edit_and_delete(self):
        # При обращении к страницам редактирования и удаления комментария
        users_statuses = (
            # автор комментария должен получить ответ OK,
            (self.author, HTTPStatus.OK),
            # читатель должен получить ответ NOT_FOUND.
            (self.reader, HTTPStatus.NOT_FOUND))
        for user, status in users_statuses:
            # Логиним пользователя в клиенте(имитация входа юзера на сайт):
            self.client.force_login(user)
            # Для каждой пары "пользователь - ожидаемый ответ"
            # перебираем имена тестируемых страниц:
            for name in ('news:edit', 'news:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        # Сохраняем адрес страницы логина:
        login_url = reverse('users:login')
        # В цикле перебираем имена страниц, с которых ожидаем редирект:
        for name in ('news:edit', 'news:delete'):
            with self.subTest(name=name):
                url = reverse(name, args=(self.comment.id,))
                # Получаем ожидаемый адрес страницы логина,
                # на который будет перенаправлен пользователь.
                # Учитываем, что в адресе будет параметр next, в котором передаётся
                # адрес страницы, с которой пользователь был переадресован.
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    @skip
    def test_homepage(self):
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        url = reverse('news:home')
        response = self.client.get(url)
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @skip
    def test_detail_page(self):
        url = reverse('news:detail', args=[self.news.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)