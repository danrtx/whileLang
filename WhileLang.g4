grammar WhileLang;

program: statement+ EOF;
declaration: type ID ('=' expr)? SEMI;
type: INT_TYPE | STRING_TYPE;

statement
    : assignment | ifStatement | whileStatement
    | declaration | breakStatement | continueStatement
    ;

assignment: ID ASSIGN expr SEMI;

ifStatement
    : IF LPAREN condition RPAREN LBRACE statement* RBRACE
      (ELSE LBRACE statement* RBRACE)?
    ;

whileStatement
    : WHILE LPAREN condition RPAREN LBRACE statement* RBRACE
    ;

breakStatement: BREAK SEMI;
continueStatement: CONTINUE SEMI;
condition: expr;

expr
    : ID                                       # idExpr
    | NUMBER                                   # numberExpr
    | STRING                                   # stringExpr
    | expr (LT | GT | GE | LE | EQ | NE) expr  # comparisonExpr
    | expr (PLUS | MINUS | MUL | DIV) expr     # arithmeticExpr
    | LPAREN expr RPAREN                       # parenExpr
    ;

IF: 'if'; ELSE: 'else'; WHILE: 'while';
BREAK: 'break'; CONTINUE: 'continue';
INT_TYPE: 'int'; STRING_TYPE: 'string';
LPAREN: '('; RPAREN: ')'; LBRACE: '{'; RBRACE: '}';
SEMI: ';'; ASSIGN: '=';
GE: '>='; LE: '<='; EQ: '=='; NE: '!=';
LT: '<'; GT: '>';
PLUS: '+'; MINUS: '-'; MUL: '*'; DIV: '/';
STRING: '"' (~["\r\n])* '"';
ID: [a-zA-Z_][a-zA-Z_0-9]*;
NUMBER: [0-9]+;
COMMENT: '//' ~[\r\n]* -> skip;
WS: [ \t\r\n]+ -> skip;