from django.test import TestCase, Client #사이트에 접속하는자
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1 포스트 목록 페이지(post_list)를 연다. 127.0.0.1:8000/blog/
        response = self.client.get('/blog/')
        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)
        # 1.4 NavBar가 있다.
        navbar = soup.nav

        # 1.5 Blog, About me라는 문구가 Navbar에 있다.
        print("navbar에 Blog, About me가 있는지 확인")
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)
        print("결과:",self.assertIn('Blog', navbar.text),self.assertIn('About me', navbar.text))
        # 2.1 게시물이 하나도 없을때
        self.assertEqual(Post.objects.count(), 0)
        print("게시물이 개수는?:", Post.objects.count())
        # 2.2 메인영역에 "아직 게시물이 없습니다."
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        post_001 = Post.objects.create(
            title='첫번째 포스트 입니다.',
            content='hello world. we are the world.',
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='테스트 코드입니다.',
        )

        # print("포스트가 있는가?:",self.assertEqual(Post.objects.count(), 0))
        # 3.1 if 게시물이 2개 있으면,
        self.assertEqual(Post.objects.count(), 2)
        # 3.2 포스트목록 페이지를 새로 고침했을때,
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        print(post_001.title, post_002)
        # 3.4 "아직 게시물이 없습니다."라는 문구가 없어야 한다.
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)
