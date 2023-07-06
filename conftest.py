import pytest

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='testAuthor')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='testTitle',
        text='testText')
    return news


@pytest.fixture
def get_news_pk_arg(news):
    return news.pk,


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='testCommentText'
    )
    return comment


@pytest.fixture
def get_comment_pk_arg(comment):
    return comment.pk,


@pytest.fixture
def form_data():
    return {
        'text': 'testCommentText'
    }
