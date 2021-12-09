/*
    This file defines a grammar to recognize graphs
    in DOT language.
*/
grammar DOT;

graph   :  'strict'? 'digraph' identifier '{' start ';'? stmt_list '}' ('/*' indipendence_list? '*/')?;


stmt_list:  (stmt ';'? stmt_list)? ;

indipendence_list: indipendence (';' | ',')? indipendence_list?;

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

a_list : assignment (';'|',')? a_list?;

a_label : ('label' | '"label"') '=' identifier (';'|',')? a_list?;

start: ('start' | '"start"') (port? | edgeRHS attr_label);

start_node: Start_identifier port?;

start_edge: Start_identifier edgeRHS attr_label;

edge_stmt : (node_id | subgraph_stmt) edgeRHS attr_label;

edgeRHS : '->' (node_id | subgraph_stmt) edgeRHS?;

node_stmt : node_id attr_list?;

node_id : identifier port?;

port : ':' identifier (':' identifier)?;

subgraph_stmt : ('subgraph' identifier?)? '{'stmt_list'}';

assignment : identifier '=' identifier;

indipendence: indipendence_edge'/'indipendence_edge;

indipendence_edge: Direction identifier '-' identifier '->' identifier ;


identifier : String | Quote | Number;

Quote: '"' (~["\\] | '\\' .)* '"';
String: [a-zA-Z] [a-zA-Z0-9]*;
Number : '-'? (('.'[0-9]+) | [0-9]+('.'[0-9]*)?);
Direction : '<' | '>';
Start_identifier : 'start' | '"start"';
Uppercase_letter : [A-Z];
Lowercase_letter : [a-z];
Digit : [0-9];

WS: [ \t\n\r]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;