# --encoding: utf8 --
import unittest
import timeit
import sys
import math

from tipa import parser

class Test(unittest.TestCase):
    
    def test_parse(self):
        for (test, expected) in [('one two', ''),
                                 ('one or two', ''),
                                 ('one not three', ''),
                                 ('(one)', ''),
                                 ('(one two)', ''),
                                 ('((one two))', ''),
                                 ('(((one two)))', ''),
                                 ('(one (two three))', ''),
                                 ('(one (two or three))', ''),
                                 ('(one (two or three and four))', ''),
                                 ]:
            
            print 'query:' , test
            p = parser.QueryParser()
            output = p.parse(test)
            
            #self.assertEquals(output, expected)
            
            print output.pretty(' ')
    
        
    
           
if __name__ == "__main__":
    print sys.argv
    if '--verbose' in sys.argv:
        test_input = 'foo -bar (hey not foo)'
        p = parser.QueryParser(use_kwargs=False, flatten_tfidf=False)
        print p.get_tree(test_input)
        _, formula = p.parse(test_input)
        print formula
    else:
        unittest.main()
        
