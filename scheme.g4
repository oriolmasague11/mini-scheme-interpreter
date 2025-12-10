// Gramàtica per expressions senzilles
grammar scheme;
root : expr+             // l'etiqueta ja és root        // expr* ? 
     ;

expr : '(' expr* ')'     # parentesi
     | NUM               # numero
     | BOOL              # bolea
     | ID                # identificador
     | OP                # operador
     | STRING            # string
     | '\'(' expr* ')'   # llista  
     ;

NUM : [0-9]+ ;
STRING : '"' .*? '"';
BOOL : '#t' | '#f' ;
ID : [a-zA-Z]+[a-zA-Z0-9-_?]* ;
OP : '+' | '-' | '/' | '*' | '^' | '=' | '>' | '<' | '<>' | 'mod' | 'and' | 'or' | 'not';
COMMENT : ';' ~[\n\r]* -> skip; 
WS  : [ \t\n\r]+ -> skip;