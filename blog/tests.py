from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 1.1 포스트 목록 페이지(post list)를 연다.
        response = self.client.get('/blog/')

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 1.3 페이지의 타이틀에 Blog라는 문구가 있다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn('Blog', soup.title.text)

        # 1.4 NavBar가 있다.
        navbar = soup.nav
        
        # 1.5 Blog, About me라는 문구가 NavBar에 있다.
        self.assertIn('Plog', navbar.text)
        self.assertIn('Home', navbar.text)

        # 2.1 게시물이 하나도 없을 때, 메인 영역에 "아직 게시물이 없습니다." 라는 문구가 나온다.
        self.assertEqual(Post.objects.count(), 0)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        
        # 3.1 만약 게시물이 n개 있다면, 포스트 목록 페이지를 새로고침 했을 때 메인 영역에 표시
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = 'Hello World!. We are the world',            
        )

        post_002 = Post.objects.create(
            title = '두번째 포스트입니다.',
            content = '저는 냉면을 좋아합니다.',
        )
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)


    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title = '',
            content = '',
        )
        self.assertEqual(Post.objects.count(), 1)
        # 1.2. 그 포스트의 url은 '/blog/1/'이다.
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1. 첫 번째 포스트의 url로 접근하면 정상적으로 response가 온다
        response = self.client.get(post_001.get_absoloute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # 2.2. 포스트 목록 페이지와 똑같은 네비게이션 바가 있다.
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About me', navbar.text)

        # 2.3. 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.content, post_area.text)


