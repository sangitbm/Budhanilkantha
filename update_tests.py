with open('core/tests_home.py', 'a', encoding='utf-8') as f:
    f.write('''
    def test_title_and_testimonials_section(self):
        from core.models import Testimonial
        import re
        Testimonial.objects.create(name='John Doe', quote='Great school!', is_published=True)
        response = self.client.get(reverse('home'))
        
        # Check title
        content = response.content.decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        self.assertIsNotNone(title_match)
        title_text = title_match.group(1).strip()
        self.assertNotIn('<', title_text)
        self.assertLess(len(title_text), 100)
        
        # Check tst-section appears exactly once
        self.assertEqual(content.count('class="tst-section"'), 1)
''')
