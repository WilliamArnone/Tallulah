/*
    This file defines a grammar to recognize graphs
    in DOT language.
*/
grammar DOT;

graph   :  'strict'? 'digraph' identifier '{' stmt_list '}' ;

stmt_list:  (stmt ';'? stmt_list)? ;

/* A statement could be:
    - x1 [... some attributes ...]       // a node
	- x1 -> x2                           // a simply edge (no label)
    - x1 -> x2 [label="..."]             // a label edge

   where x1 and x2 are IDs of nodes (a number or a couple of numbers).
*/
stmt : node_stmt | edge_stmt | attr_stmt | assignment | subgraph_stmt ;

attr_stmt : ('graph' | 'node' | 'edge') attr_list ;

attr_list  : '[' a_list? ']' attr_list?;

attr_label  : '[' a_label ']' attr_list?;

a_list : (comment | assignment)  (';'|',')? a_list?;

a_label : ('label' | '"label"') '=' identifier (';'|',')? a_list?;

edge_stmt : (node_id | subgraph_stmt) edgeRHS attr_label;

edgeRHS : '->' (node_id | subgraph_stmt) edgeRHS?;

node_stmt : node_id attr_list?;

node_id : identifier port?;

port : ':' identifier (':' identifier)?;

subgraph_stmt : ('subgraph' identifier?)? '{'stmt_list'}';

assignment : identifier '=' identifier;

comment : ('comment' | '"comment"') '=' comment_content;

comment_content : ('"+'indipendence_comment (';' indipendence_comment)*'+"' | identifier);

indipendence_comment : Direction Direction identifier_no_quote '-'identifier_no_quote'->' identifier_no_quote;

identifier : identifier_no_quote | QuoteString ;

identifier_no_quote : string | number;

string : letter letter_digit* ;

number : '-'? (('.'Digit+) | Digit+('.'Digit*)?);

letter_digit : letter | Digit;
letter : (Uppercase_letter | Lowercase_letter | '-' | '_' | ',') ;


/* TODO: should be possible to create string with + */
QuoteString: '"' (~[+"\\] | '\\' .)* '"';
Direction : '<' | '>';
Uppercase_letter : [A-Z];
Lowercase_letter : [a-z];
Digit : [0-9];

WS: [ \t\n\r]+ -> skip;

COMMENT: '/*' .*? '*/' -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;