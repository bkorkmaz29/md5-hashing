from md5 import MD5
import hashlib
import unittest

class tests(unittest.TestCase):
     def test(self):
        test_strings = [
            "md5hashing",
            "politechnikawarszawska",
            "jabrarpmmomovenom  ",
            "448822sdfc47777ss52",
            "accordingtoMicrosoft,theauthorsoftheFlamemalwareusedanMD5collision",
            "24-December-2010",
            "Not the answer you're looking for?",
            "A lambda function is a small anonymous function.",
            "1.?*/**/2dsdso",
            "  s  3 -*/casge =)(/&%+"
        ]

        md5 = MD5()
        for input_string in test_strings:
            with self.subTest(input_string=input_string):
                self.assertEqual(md5.generate_hash(input_string), hashlib.md5(input_string.encode("utf_8")).hexdigest())
