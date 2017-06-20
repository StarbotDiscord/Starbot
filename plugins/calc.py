#    Copyright 2017 Starbot Discord Project
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from __future__ import division

import math
import operator

from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)

from api import command, message, plugin

__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''

class NumericStringParser(object):
    '''Most of this code comes from the fourFn.py pyparsing example.'''
    def push_first(self, strg, loc, toks):
        self.expression_stack.append(toks[0])
    def push_unary_minus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.expression_stack.append('unary -')
    def __init__(self):
        """
        expop   :: '^'
        multop  :: 'x' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        exp = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(exp + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas+nums+"_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("x")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        powop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (pi|exp|fnumber|ident+lpar+expr+rpar).setParseAction(self.push_first))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
               ).setParseAction(self.push_unary_minus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore((powop + factor).setParseAction(self.push_first))
        term = factor + ZeroOrMore((multop + factor).setParseAction(self.push_first))
        expr << term + ZeroOrMore((addop + term).setParseAction(self.push_first))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+" : operator.add,
                    "-" : operator.sub,
                    "x" : operator.mul,
                    "/" : operator.truediv,
                    "^" : operator.pow}
        self.function = {"sin" : math.sin,
                         "cos" : math.cos,
                         "tan" : math.tan,
                         "abs" : abs,
                         "trunc" : lambda a: int(a),
                         "round" : round,
                         "sgn" : lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def stack_evaluate(self, s):
        '''Backend stack evaluation'''
        op_eval = s.pop()
        if op_eval == 'unary -':
            return -self.stack_evaluate(s)
        if op_eval in "+-x/^":
            op_eval2 = self.stack_evaluate(s)
            op_eval1 = self.stack_evaluate(s)
            return self.opn[op_eval](op_eval1, op_eval2)
        elif op_eval == "PI":
            return math.pi # 3.1415926535
        elif op_eval == "E":
            return math.e  # 2.718281828
        elif op_eval in self.function:
            return self.function[op_eval](self.stack_evaluate(s))
        elif op_eval[0].isalpha():
            return 0
        else:
            return float(op_eval)

    def stack_eval(self, num_string, parse_all=True):
        self.expression_stack = []
        results = self.bnf.parseString(num_string, parse_all)
        val = self.stack_evaluate(self.expression_stack[:])
        return val

def onInit(plugin_in):
    #create the basics of our plugin
    calc_command = command.Command(plugin_in, 'calc', shortdesc='Calculate given input')
    return plugin.Plugin(plugin_in, 'calc', [calc_command])

async def onCommand(message_in):
    """Do some math."""
    formula = message_in.body
    formula = formula.replace('*', 'x')

    if formula == None:
        msg = 'Usage: `{}calc [formula]`'.format('!')
        return message.Message(body=msg)

    try:
        nsp = NumericStringParser()
        answer = nsp.stack_eval(formula)
    except Exception as e:
        print("CALC PLUGIN EXCEPTION\r\n{}".format(e))
        msg = 'I couldn\'t parse "{}" :(\n\n'.format(formula)
        msg += 'I understand the following syntax:\n```\n'
        msg += "expop   :: '^'\n"
        msg += "multop  :: 'x' | '/'\n"
        msg += "addop   :: '+' | '-'\n"
        msg += "integer :: ['+' | '-'] '0'..'9'+\n"
        msg += "atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'\n"
        msg += "factor  :: atom [ expop factor ]*\n"
        msg += "term    :: factor [ multop factor ]*\n"
        msg += "expr    :: term [ addop term ]*```"
        # msg = Nullify.clean(msg)
        return message.Message(body=msg)

    msg = '`{}` = `{}`'.format(formula, answer)
    # Say message
    return message.Message(body=msg)
