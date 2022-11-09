from django.test import TestCase, Client #사이트에 접속하는자
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
from .models import Post, Category, Tag, Comment

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(
            username='trump',
            password='trump'
        )
        self.user_sdjo = User.objects.create_user(
            username='sdjo',
            password='sdjo'
        )

        self.user_sdjo.is_staff = True
        self.user_sdjo.save()

        self.category_programing = Category.objects.create(
            name='programming', slug='programming'
        )

        self.category_music = Category.objects.create(
            name='music', slug='music'
        )

        self.tag_python_kor = Tag.objects.create(
            name='파이썬 공부', slug='파이썬 공부'
        )

        self.tag_python = Tag.objects.create(
            name='python', slug='python'
        )

        self.tag_hello = Tag.objects.create(
            name='hello', slug='hello'
        )

        self.post_001 = Post.objects.create(
            title='첫번째 포스트 입니다.',
            content='hello world. we are the world.',
            category=self.category_programing,
            author=self.user_trump,
        )
        self.post_001.tags.add(self.tag_hello)

        self.post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='테스트 코드입니다.',
            category=self.category_music,
            author=self.user_sdjo,
        )

        self.post_003 = Post.objects.create(
            title='세 번째 포스트 입니다.',
            content='세번째 테스트코드입니다.',
            author=self.user_sdjo,
        )
        self.post_003.tags.add(self.tag_python_kor)
        self.post_003.tags.add(self.tag_python)

        self.comment_001 = Comment.objects.create(
            post=self.post_001,
            author=self.user_sdjo,
            content='첫 번째 댓글입니다.'
        )

    #def의 이름이 test로 시작하면 test기능으로 간주함.
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        #print('categories_card : ', categories_card)
        self.assertIn('Categories', categories_card.text)
        #print('category_programing.post_set : ', self.category_programing.post_set.count()) #post_set은 models의 category아래 post_set 객체를말함
        self.assertIn(f'{self.category_programing} ({self.category_programing.post_set.count()})',
                      categories_card.text
                      )
        self.assertIn(f'{self.category_music} ({self.category_music.post_set.count()})',
                      categories_card.text
                      )
        self.assertIn(
            f'미분류 ({Post.objects.filter(category=None).count()})',
            categories_card.text
        )

    def test_post_list_with_posts(self):
        self.assertEqual(Post.objects.count(), 3)  # 3.1 if 게시물이 n개 있으면,

        response = self.client.get('/blog/')# 1.1 포스트 목록 페이지(post_list)를 연다. 127.0.0.1:8000/blog/
        self.assertEqual(response.status_code, 200)# 1.2 정상적으로 페이지가 로드된다.

        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)# 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        # 1.4 NavBar가 있다.
        # 1.5 Blog, About me라는 문구가 Navbar에 있다.
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 3.3 메인 영역에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)  # 3.4 "아직 게시물이 없습니다."라는 문구가 없어야 한다.

        post_001_card = main_area.find('div', id='post-1')
        self.assertIn(self.post_001.title, post_001_card.text)
        self.assertIn(self.post_001.category.name, post_001_card.text)
        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_python.name, post_001_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_001_card.text)

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_python.name, post_002_card.text)
        self.assertNotIn(self.tag_python_kor.name, post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn('미분류', post_003_card.text)
        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_python.name, post_003_card.text)
        self.assertIn(self.tag_python_kor.name, post_003_card.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

    def test_post_list_without_post(self):
        Post.objects.all().delete() #포스트 삭제 후 진행.
        self.assertEqual(Post.objects.count(), 0)# 2.1 게시물이 하나도 없을때

        response = self.client.get('/blog/') # 1.1 포스트 목록 페이지(post_list)를 연다. 127.0.0.1:8000/blog/

        self.assertEqual(response.status_code, 200)# 1.2 정상적으로 페이지가 로드된다.

        soup = BeautifulSoup(response.content, 'html.parser')# 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        self.navbar_test(soup)
        self.assertIn('Blog', soup.title.text)

        #print("게시물이 개수는?:", Post.objects.count())
        # 2.2 메인영역에 "아직 게시물이 없습니다."
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

    def test_post_detail(self):
        self.assertEqual(Post.objects.count(), 3)

        # 1.2. 그 포스트의 url은 ‘/blog/1/’ 이다.
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 포스트의 url로 접근하면 정상적으로 response가 온다(status code: 200).
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        # 2.2. 포스트 목록 페이지와 똑같은 내비게이션 바가 있다.
        self.navbar_test(soup)
        self.category_card_test(soup)

        # 2.3. 첫번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')#2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.post_001.category.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)# 2.5 첫번째 포스트의 작성자가 포스트 영역에 있따.
        # 2.6 첫번쨰 포스트의 내용이 영역에 있따.
        self.assertIn(self.post_001.content, post_area.text)

        self.assertIn(self.tag_hello.name, post_area.text)
        self.assertNotIn(self.tag_python.name, post_area.text)
        self.assertNotIn(self.tag_python_kor.name, post_area.text)

    def test_category_page(self):
        response = self.client.get(self.category_programing.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programing.name, main_area.h1.text)
        self.assertIn(self.category_programing.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_tag_page(self):
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)

        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    def test_create_post_without_login(self):
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

    def test_create_post_with_login(self):
        self.client.login(username='trump', password='trump')
        response = self.client.get('/blog/create_post/')
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='sdjo', password='sdjo')
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create a New Post', main_area.text)

        tag_str_input = main_area.find('input', id="id_tags_str")
        self.assertTrue(tag_str_input)

        self.client.post(
            '/blog/create_post/',
            {
                'title': 'Post Form 만들기',
                'content': '페이지 생성',
                'tags_str': 'new tag; 한글 태그, python'
            }
        )

        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post Form 만들기')
        self.assertEqual(last_post.author.username, 'sdjo')

        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
        self.assertTrue(Tag.objects.get(name='python'))

    def test_update_post(self):
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'
        # 로그 아웃 상태에서 접근하는 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)
        # 로그인은 했으나 작성자 권한이 없는 경우
        self.assertNotEqual(self.post_003.author, self.user_trump)
        self.client.login(username='trump', password='trump')
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)

        # 작성자(sdjo)로 접근 하는 경우
        self.assertEqual(self.post_003.author, self.user_sdjo)
        self.client.login(username='sdjo', password='sdjo')
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Edit Post', main_area.text)

        tag_str_input = main_area.find('input', id='id_tags_str')
        self.assertTrue(tag_str_input)
        self.assertIn('파이썬 공부; python', tag_str_input.attrs['value'])

        response = self.client.post(
            update_post_url,
            {
                'title':'세 번째 포스트를 수정했습니다.',
                'content':'안녕하세요????네??',
                'category': self.category_music.pk,
                'tags_str': '파이썬 공부; 한글 태그, some tag'
            },
            follow=True #수정된 페이지 리다이렉트를 위한 값.
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn('세 번째 포스트를 수정했습니다', main_area.text)
        self.assertIn('안녕하세요', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)

        self.assertIn('파이썬 공부', main_area.text)
        self.assertIn('한글 태그', main_area.text)
        self.assertIn('some tag', main_area.text)
        self.assertNotIn('python', main_area.text)

    def test_comment_form(self):
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post_001.comment_set.count(), 1)

        # 로그인 하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertIn('Log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))

        # 로그인 한 상태
        self.client.login(username='sdjo', password='sdjo')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertNotIn('Log in and leave a comment', comment_area.text)

        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment_form.find('textarea', id='id_content'))
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content': 'sdjo의 댓글입니다.'
            },
            follow=True #redirect 동작역할
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2) #댓글 추가 여부 확인

        new_comment = Comment.objects.last()
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)

        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('sdjo', new_comment_div.text)
        self.assertIn('sdjo의 댓글입니다', new_comment_div.text)

    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            post=self.post_001,
            author=self.user_trump,
            content='트럼프의 댓글입니다.'
        )
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertFalse(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        # sdjo로 로그인 한 상태
        self.client.login(username='sdjo', password='sdjo')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        comment_area = soup.find('div', id='comment-area')
        self.assertTrue(comment_area.find('a', id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a', id='comment-2-update-btn'))

        comment_001_update_btn = comment_area.find('a', id='comment-1-update-btn')
        self.assertIn('edit', comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'], '/blog/update_comment/1/')

        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual('Edit Comment - Blog', soup.title.text)
        update_comment_form = soup.find('form', id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content, content_textarea.text)
        #sleep(2)
        response = self.client.post(
            '/blog/update_comment/1/',
            {
                'content': '오바마의 댓글을 수정합니다.'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        comment_001_div = soup.find('div', id='comment-1')
        self.assertIn('오바마의 댓글을 수정합니다.', comment_001_div.text)
        self.assertIn('Updated: ', comment_001_div.text)

    def test_search(self):
        post_about_python = Post.objects.create(
            title='파이썬에 대한 포스트입니다.',
            content='Hello World, We are the world',
            author=self.user_trump
        )

        response = self.client.get('/blog/search/파이썬/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        main_area = soup.find('div', id='main-area')

        self.assertIn('Search: 파이썬 (2)', main_area.text)
        self.assertNotIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertIn(self.post_003.title, main_area.text)
        self.assertIn(post_about_python.title, main_area.text)