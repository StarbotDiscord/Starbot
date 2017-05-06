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

__author__='Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__='''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__='''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''

class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''
    def pushFirst(self, strg, loc, toks ):
        self.exprStack.append( toks[0] )
    def pushUMinus(self, strg, loc, toks ):
        if toks and toks[0]=='-':
            self.exprStack.append( 'unary -' )
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
        point = Literal( "." )
        e     = CaselessLiteral( "E" )
        fnumber = Combine( Word( "+-"+nums, nums ) +
                        Optional( point + Optional( Word( nums ) ) ) +
                        Optional( e + Word( "+-"+nums, nums ) ) )
        ident = Word(alphas, alphas+nums+"_$")
        plus  = Literal( "+" )
        minus = Literal( "-" )
        mult  = Literal( "x" )
        div   = Literal( "/" )
        lpar  = Literal( "(" ).suppress()
        rpar  = Literal( ")" ).suppress()
        addop  = plus | minus
        multop = mult | div
        expop = Literal( "^" )
        pi    = CaselessLiteral( "PI" )
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                (pi|e|fnumber|ident+lpar+expr+rpar).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar+expr+rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + ZeroOrMore( ( expop + factor ).setParseAction( self.pushFirst ) )
        term = factor + ZeroOrMore( ( multop + factor ).setParseAction( self.pushFirst ) )
        expr << term + ZeroOrMore( ( addop + term ).setParseAction( self.pushFirst ) )
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = { "+" : operator.add,
                "-" : operator.sub,
                "x" : operator.mul,
                "/" : operator.truediv,
                "^" : operator.pow }
        self.fn  = { "sin" : math.sin,
                "cos" : math.cos,
                "tan" : math.tan,
                "abs" : abs,
                "trunc" : lambda a: int(a),
                "round" : round,
                "sgn" : lambda a: abs(a)>epsilon and cmp(a,0) or 0}
    def evaluateStack(self, s ):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack( s )
        if op in "+-x/^":
            op2 = self.evaluateStack( s )
            op1 = self.evaluateStack( s )
            return self.opn[op]( op1, op2 )
        elif op == "PI":
            return math.pi # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op]( self.evaluateStack( s ) )
        elif op[0].isalpha():
            return 0
        else:
            return float( op )
    def eval(self,num_string,parseAll=True):
        self.exprStack=[]
        results=self.bnf.parseString(num_string,parseAll)
        val=self.evaluateStack( self.exprStack[:] )
        return val

def onInit(plugin_in):
    #create the basics of our plugin
    calc_command = command.command(plugin_in, 'calc', shortdesc='Calculate given input')
    return plugin.plugin(plugin_in, 'calc', [calc_command])

async def onCommand(message_in):
    """Do some math."""
    formula = message_in.body
    formula = formula.replace('*', 'x')

    if formula == None:
        msg = 'Usage: `{}calc [formula]`'.format('!')
        return message.message(body=msg)

    try:
        nsp = NumericStringParser()
        answer = nsp.eval(formula)
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
        return message.message(body=msg)

    msg = '`{}` = `{}`'.format(formula, answer)
    # Say message
    return message.message(body=msg)