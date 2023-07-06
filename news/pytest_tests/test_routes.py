from http import HTTPStatus
import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_get_homepage_for_anonymous_user(client):
    url = reverse('news:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_get_news_detail_page_for_anonymous_user(client, news):
    url = reverse('news:detail', args=(news.pk,))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    ['parametrized_client', 'expected_status'],
    [
        ('admin_client', HTTPStatus.NOT_FOUND),
        ('author_client', HTTPStatus.OK)
    ]
)
@pytest.mark.parametrize(
    ['name', 'args'],
    [
        ('news:edit', pytest.lazy_fixture('get_news_pk_arg')),
        ('news:delete', pytest.lazy_fixture('get_news_pk_arg'))
    ]
)
def test_get_page_edit_and_delete_author(
        parametrized_client, name, args, expected_status):
    url = reverse()






# @pytest.mark.parametrize(
#     ['name', 'args'],
#     [
#         ('news:home', None),
#         ('users:login', None),
#         ('users:logout', None),
#         ('users:signup', None),
#         ('news:detail', pytest.lazy_fixture('get_news_pk_arg')),
#         ('news:edit', pytest.lazy_fixture('get_news_pk_arg')),
#         ('news:delete', pytest.lazy_fixture('get_news_pk_arg'))
#     ]
# )