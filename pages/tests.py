from django.test import TestCase
from django.urls import reverse, resolve

from .views import HomePageView


class HomepageTests(TestCase):
    def setUp(self):
        """각 테스트 (method) 실행 전에 실행됨 (초기 설정)"""
        url = reverse("home")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        """루트 URL('/')이 정상적으로 접근 가능한지 확인 (HTTP 200)"""
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        """홈페이지가 'home.html' 템플릿을 사용하는지 확인"""
        self.assertTemplateUsed(self.response, "home.html")

    def test_homepage_contains_correct_html(self):
        """홈페이지에 'home page' 텍스트가 포함되어 있는지 확인"""
        self.assertContains(self.response, "home page")

    def test_homepage_does_not_contain_incorrect_html(self):
        """홈페이지에 포함되지 않아야 할 텍스트가 없는지 확인"""
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_homepage_url_resolves_homepageview(self):
        """URL '/'이 HomePageView와 올바르게 매핑되는지 검증"""
        view = resolve("/")
        self.assertEqual(view.func.__name__, HomePageView.as_view().__name__)