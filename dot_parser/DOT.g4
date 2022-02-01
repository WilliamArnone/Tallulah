/*
    This file defines a grammar to recognize graphs
    in DOT language.
*/
grammar DOT;

graph   :  'strict'? 'digraph' identifier '{' stmt_list '}' ('/*' indipendence_list? '*/')?;


stmt_list:  (stmt ';'? stmt_list)? ;

indipendence_list: indipendence (';' | ',')? indipendence_list?;

stmt : node_stmt | edge_stmt | attr_stmt | assignment | subgraph_stmt ;

attr_stmt : ('graph' | 'node' | 'edge') attr_list ;

attr_list  : '[' a_list? ']' attr_list?;

attr_label  : '[' a_label ']' attr_list?;

a_list : assignment (';'|',')? a_list?;

a_label : ('label' | '"label"') '=' identifier (';'|',')? a_list?;

edge_stmt : (node_id | subgraph_stmt) edgeRHS attr_label;

edgeRHS : '->' (node_id | subgraph_stmt) edgeRHS?;

node_stmt : node_id attr_list?;

node_id : identifier port?;

port : ':' identifier (':' identifier)?;

subgraph_stmt : ('subgraph' identifier?)? '{'stmt_list'}';

assignment : identifier '=' identifier;

indipendence: indipendence_edge'/'indipendence_edge;

indipendence_edge: Direction identifier '-' identifier '->' identifier ;

identifier : Variable | Quote | Number ;

Quote: '"' (~["\\] | '\\' .)* '"';
Variable: [a-zA-Z] [a-zA-Z0-9]*;
Number : '-'? (('.'[0-9]+) | [0-9]+('.'[0-9]*)?);
Direction : '<' | '>';

WS: [ \t\n\r]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;