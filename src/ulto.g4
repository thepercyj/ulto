grammar ulto;

program
    : statement* EOF
    ;

statement
    : assignment
    | reverse
    | revtrace
    | ifStatement
    | forLoop
    | whileLoop
    | printStatement
    | breakStatement
    ;

assignment
    : ID (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | TIMES_ASSIGN | OVER_ASSIGN) expression
    ;

reverse
    : REV ID
    ;

revtrace
    : REVTRACE ID NUMBER
    ;

ifStatement
    : IF expression COLON block elifBranch* elseBranch?
    ;

elifBranch
    : ELIF expression COLON block
    ;

elseBranch
    : ELSE COLON block
    ;

forLoop
    : FOR ID IN iterable COLON block
    ;

whileLoop
    : WHILE expression COLON block
    ;

printStatement
    : PRINT LPAREN expression (COMMA expression)* RPAREN
    ;

breakStatement
    : BREAK
    ;

expression
    : primaryExpression (operator primaryExpression)*
    ;

primaryExpression
    : NUMBER
    | STRING
    | TRUE
    | FALSE
    | LEN LPAREN expression RPAREN
    | ID (LBRACKET expression RBRACKET)?
    | LPAREN expression RPAREN
    ;

operator
    : PLUS
    | MINUS
    | TIMES
    | OVER
    | EQ
    | NEQ
    | LT
    | GT
    | LTE
    | GTE
    | AND
    | OR
    | MODULO
    | INT_DIV
    ;

block
    : INDENT statement+ DEDENT
    ;

iterable
    : RANGE LPAREN expression (COMMA expression (COMMA expression)?)? RPAREN
    | LBRACKET expression (COMMA expression)* RBRACKET
    | ID
    ;

ID          : [A-Za-z_][A-Za-z0-9_]* ;
NUMBER      : [0-9]+ ;
STRING      : '"' (~["\\] | '\\' .)* '"' ;
PLUS        : '+' ;
MINUS       : '-' ;
TIMES       : '*' ;
OVER        : '/' ;
EQ          : '==' ;
NEQ         : '!=' ;
LT          : '<' ;
GT          : '>' ;
LTE         : '<=' ;
GTE         : '>=' ;
MODULO      : '%' ;
INT_DIV     : '//' ;
ASSIGN      : '=' ;
PLUS_ASSIGN : '+=' ;
MINUS_ASSIGN: '-=' ;
TIMES_ASSIGN: '*=' ;
OVER_ASSIGN : '/=' ;
REV         : 'rev' ;
REVTRACE    : 'revtrace' ;
IF          : 'if' ;
ELIF        : 'elif' ;
ELSE        : 'else' ;
FOR         : 'for' ;
WHILE       : 'while' ;
IN          : 'in' ;
PRINT       : 'print' ;
BREAK       : 'break' ;
TRUE        : 'True' ;
FALSE       : 'False' ;
AND         : 'and' ;
OR          : 'or' ;
LEN         : 'len' ;
RANGE       : 'range' ;
LPAREN      : '(' ;
RPAREN      : ')' ;
LBRACKET    : '[' ;
RBRACKET    : ']' ;
LBRACE      : '{' ;
RBRACE      : '}' ;
COMMA       : ',' ;
COLON       : ':' ;
NEWLINE     : '\r'? '\n' ;
INDENT      : '    ' ; // 4-space indent
DEDENT      : ''; // Handled by lexer based on indent level
SKIP        : [ \t]+ -> skip ;
COMMENT     : '#' ~[\r\n]* -> skip ;
