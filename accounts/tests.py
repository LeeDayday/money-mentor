from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import CustomUserCreationForm
from .views import SignupPageView


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser', email='testuser@email.com', password='testpw123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='testsuperuser', email='testsuperuser@email.com', password='testpw123'
        )
        self.assertEqual(admin_user.username, 'testsuperuser')
        self.assertEqual(admin_user.email, 'testsuperuser@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

class SignUpPageTests(TestCase):
    def setUp(self):
        """각 테스트 (method) 실행 전에 실행됨 (초기 설정)"""
        url = reverse('signup')  # URL 가져오기
        self.response = self.client.get(url)

    def test_signup_template(self):
        """회원가입 페이지가 정상적으로 렌더링되는지 확인"""
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'Hi there! I should not be on the page.')

    def test_signup_form(self):
        """회원가입 페이지에서 올바른 폼이 전달되고, csrf 보안이 적용되었는지 검증"""
        form = self.response.context.get('form') # view에서 전달된 form 가져오기
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        """URL '/accounts/signup/'이 SignupPageView와 올바르게 매핑되는지 검증"""
        view = resolve('/accounts/signup/') # 해당 URL과 연결된 view 정보 반환
        self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)
