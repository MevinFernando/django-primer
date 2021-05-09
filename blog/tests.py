from django.http import response
from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from .models import Post

class BlogTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username = 'testuser',
            email = 'email@email.com',
            password = 'testuser'
        )

        self.post = Post.objects.create(
            title = 'test',
            body = 'test',
            author = self.user,
        )
    
    def test_string_representation(self):
        post = Post(title='A sample title')
        self.assertEqual(str(post), post.title)
    
    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'test')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'test')
    
    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, 'test')
    
    def test_post_detail_view(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'test')
        self.assertTemplateUsed(response, 'post_detail.html')