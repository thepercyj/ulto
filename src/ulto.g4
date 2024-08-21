grammar Ulto;

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
    | functionDefinition
    | breakStatement
    ;

assignment
    : ID (ASSIGN | PLUS_ASSIGN | MINUS_ASSIGN | TIMES_ASSIGN | OVER_ASSIGN) expression
    ;

reverse
    : 'rev' ID
    ;

revtrace
    : 'revtrace' ID NUMBER
    ;

ifStatement
    : 'if' expression ':' block elifBranch* elseBranch?
    ;

elifBranch
    : 'elif' expression ':' block
    ;

elseBranch
    : 'else' ':' block
    ;

forLoop
    : 'for' ID 'in' iterable ':' block
    ;

whileLoop
    : 'while' expression ':' block
    ;

printStatement
    : 'print' '(' expression (',' expression)* ')'
    ;

breakStatement
    : 'break'
    ;

functionDefinition
    : 'def' ID '(' (ID (',' ID)*)? ')' ':' block
    ;

expression
    : primaryExpression (operator primaryExpression)*
    ;

primaryExpression
    : NUMBER
    | STRING
    | 'True'
    | 'False'
    | 'len' '(' expression ')'
    | ID ('[' expression ']')?
    | '(' expression ')'
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
    | 'and'
    | 'or'
    | MODULO
    | INT_DIV
    ;

block
    : INDENT statement+ DEDENT
    ;

iterable
    : 'range' '(' expression (',' expression (',' expression)?)? ')'
    | '[' expression (',' expression)* ']'
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