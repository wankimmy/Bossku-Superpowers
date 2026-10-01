import unittest

from comments import render_comment


class RenderCommentHiddenTests(unittest.TestCase):
    def test_plain_comment_no_link(self):
        self.assertEqual(
            render_comment("Au", "Tx"),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_none_link_uses_span(self):
        self.assertEqual(
            render_comment("Au", "Tx", link=None),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_empty_string_link_uses_span(self):
        self.assertEqual(
            render_comment("Au", "Tx", link=""),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_escapes_angle_brackets_in_author_and_text(self):
        self.assertEqual(
            render_comment("<b>x</b>", "a<b>c"),
            '<div class="comment"><span class="author">&lt;b&gt;x&lt;/b&gt;</span>'
            '<p>a&lt;b&gt;c</p></div>',
        )

    def test_ampersand_and_angle_bracket_escaped_without_double_escaping(self):
        self.assertEqual(
            render_comment("A & B < C", "text"),
            '<div class="comment"><span class="author">A &amp; B &lt; C</span><p>text</p></div>',
        )

    def test_http_link_renders_anchor(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="http://example.com"),
            '<div class="comment"><a class="author" href="http://example.com">Au</a><p>Tx</p></div>',
        )

    def test_mailto_link_renders_anchor(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="mailto:a@b.com"),
            '<div class="comment"><a class="author" href="mailto:a@b.com">Au</a><p>Tx</p></div>',
        )

    def test_scheme_matching_is_case_insensitive(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="HTTP://Example.com"),
            '<div class="comment"><a class="author" href="HTTP://Example.com">Au</a><p>Tx</p></div>',
        )

    def test_javascript_link_falls_back_to_span(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="javascript:alert(1)"),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_bare_domain_without_scheme_falls_back_to_span(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="example.com"),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_protocol_relative_link_falls_back_to_span(self):
        self.assertEqual(
            render_comment("Au", "Tx", link="//evil.com"),
            '<div class="comment"><span class="author">Au</span><p>Tx</p></div>',
        )

    def test_link_quote_is_escaped_in_href_attribute(self):
        malicious = 'http://example.com/"><script>alert(1)</script>'
        self.assertEqual(
            render_comment("Au", "Tx", link=malicious),
            '<div class="comment"><a class="author" '
            'href="http://example.com/&quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;">'
            'Au</a><p>Tx</p></div>',
        )

    def test_return_value_is_single_line(self):
        result = render_comment("A & B", "x < y", link="http://example.com/a?b=1")
        self.assertNotIn("\n", result)

    def test_return_value_is_a_string(self):
        self.assertIsInstance(render_comment("Au", "Tx"), str)


if __name__ == "__main__":
    unittest.main()
