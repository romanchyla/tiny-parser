import re
from lark import Lark, Tree, Transformer, Visitor
from lark.tree import pydot__tree_to_png
import math
from platform import node

# token +token (token -(token and token))

grammar=r"""

    
    start: clause (clause)*
    
    clause: ("(" clause ")") 
        | query operator? clause*
    
    query: qterm+
    
    modifier: "="
    
    field: ("a".."z")+ ":"
    
    qterm: (anyterm ":" anyterm) -> fielded
        | anyterm -> qterm
    
    anyterm: /[^)^\] \(]+/
    
    operator: "and" | "AND" | "or" | "OR" | "not" | "NOT" | "+" | "-"
    

    %import common.LETTER
    %import common.ESCAPED_STRING
    %import common.FLOAT
    %import common.DIGIT
    %import common.WS
    
    %ignore WS
    
"""


class QueryParser(object):
    def __init__(self, flatten_tfidf=False, use_kwargs=False):
        self.parser = Lark(grammar, parser='lalr')
        self.use_kwargs = use_kwargs
        
    def parse(self, input):
        """Receives query, will parse it into an AST
        and extract final score together with the algebraic expression
        that summarizes the whole scoring chain
        """
        
        # XXX: in true OOM fashion we should save tree with the instance
        # however I am using this class only as a wrapper for useful
        # methods; maybe will change that later...
        tree = self._get_tree(input)
        
        # this can assemble output from the tree (visiting each node)
        #visitor = TreeVisitor() 
        #visitor.visit(tree)
        
        return tree
    
    def _get_tree(self, input):        
        return self.parser.parse(self._cleanup(input))
        
    def get_tree(self, input, destination=None):
        """Generates readable representation of the input
        optionally can save graph into a PNG file"""
        
        tree = self._get_tree(input)
        out = tree.pretty(indent_str=' ')
        
        if destination:
            pydot__tree_to_png(tree, destination)
        
        return out

        
    def _cleanup(self, text):
        t = re.sub(r'\n\s*\)', ")", text, flags=re.MULTILINE)
        return t




class TreeVisitor(Visitor):        
    
    def clause(self, node):
        print 'clause', node
        
    def query(self, node):
        print 'query', node
    
    def qterm(self, node):
        print 'qterm', node
    
    def operator(self, node):
        print 'operator', node
            
    