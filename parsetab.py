
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\xc7nng\xe2\x1a\xbc\xb4\x8d\xeb\x06k\xbbi\x12\xe5'
    
_lr_action_items = {'ARRAY_ID':([0,4,8,10,14,31,46,47,49,51,52,53,55,56,57,64,65,66,67,69,70,71,72,73,74,75,122,124,125,128,130,132,136,138,148,149,150,151,153,154,166,173,174,179,184,189,192,193,223,224,225,226,227,228,],[1,18,23,35,42,42,78,18,18,84,23,88,84,23,93,78,102,35,105,102,35,109,42,42,42,42,78,78,84,84,23,23,23,23,102,102,35,35,35,35,23,23,23,23,35,35,42,42,84,84,23,23,23,23,]),'LSQBRACE':([162,183,],[200,215,]),'NUMBER':([54,58,97,111,115,126,129,131,133,137,139,],[90,95,142,155,156,165,168,170,172,176,178,]),'SHOW_TRANSITIONS':([0,],[11,]),'LINK':([42,43,61,],[72,75,75,]),'DDOT':([1,9,23,29,35,39,],[15,32,53,57,67,71,]),'STRING':([77,99,158,160,],[119,119,119,119,]),'COMMENT':([0,],[3,]),'PETRINET':([0,],[4,]),'#':([0,],[5,]),'RPAREN':([77,78,79,80,90,95,99,100,118,119,120,121,144,145,155,156,158,160,161,163,165,168,170,172,176,178,195,196,198,199,],[-89,-103,123,-102,134,140,-89,146,157,-90,159,-86,181,182,192,193,-89,-89,-101,-100,201,203,204,205,208,209,-91,-92,-87,-88,]),'SEMI':([0,2,7,11,12,18,19,20,23,24,25,26,27,28,29,30,34,35,36,37,38,39,76,81,82,87,88,89,92,93,94,96,98,104,105,106,108,109,110,127,134,135,140,147,152,157,159,169,171,175,177,181,182,187,188,190,191,202,204,205,206,207,208,209,210,216,217,231,236,237,238,239,240,],[6,17,22,40,41,-5,48,-3,-15,-7,-11,-9,-10,-8,-14,59,-51,-54,68,-50,-49,-52,117,-4,-2,-13,-23,-22,-12,-21,-20,141,143,-55,-62,-58,-53,-60,-56,-38,-26,-36,-27,-67,-66,194,197,-19,-18,-17,-16,213,214,-63,-59,-61,-57,-39,-34,-32,-25,-37,-33,-35,-24,-64,-65,242,-31,-29,-30,-28,245,]),',':([18,20,23,29,35,39,84,86,88,89,93,94,102,103,105,106,109,110,119,121,127,134,135,140,142,147,152,200,201,203,204,205,208,209,215,220,230,233,243,244,],[47,49,52,56,66,70,125,128,130,132,136,138,148,149,150,151,153,154,158,160,166,173,174,179,180,184,189,-99,223,224,225,226,227,228,-99,230,-99,-99,-98,-97,]),'=':([1,9,21,61,212,222,],[16,33,50,97,97,233,]),'$end':([3,6,13,17,22,40,41,48,59,68,83,117,141,143,194,197,213,214,242,245,],[-105,-106,0,-108,-110,-109,-107,-1,-6,-48,-104,-73,-72,-111,-85,-84,-83,-82,-94,-93,]),'RBRACE':([42,43,44,60,61,62,84,85,86,91,101,102,103,107,112,113,114,116,142,164,167,185,186,201,203,211,218,219,234,235,],[-74,-81,76,96,-81,98,-46,127,-44,135,147,-71,-69,152,-75,-77,-80,-78,-113,-41,-40,-70,-68,-47,-45,-112,-76,-79,-43,-42,]),'ID_IN_ID':([232,],[243,]),'AS':([222,],[232,]),'LBRACE':([1,9,23,29,35,39,],[14,31,51,55,65,69,]),'PLACE':([0,],[8,]),'LPAREN':([16,23,29,33,45,63,72,75,84,86,88,89,93,94,],[46,54,58,64,77,99,111,115,126,129,131,133,137,139,]),'ID':([0,4,5,8,10,14,15,31,32,46,47,49,50,51,52,53,55,56,57,64,65,66,67,69,70,71,72,73,74,75,77,99,122,124,125,128,130,132,136,138,148,149,150,151,153,154,158,160,166,173,174,179,180,184,189,192,193,200,215,223,224,225,226,227,228,230,233,],[9,20,21,29,39,43,45,61,63,80,20,20,83,86,29,89,86,29,94,80,103,39,106,103,39,110,43,43,43,43,121,121,80,80,86,86,29,29,29,29,103,103,39,39,39,39,121,121,29,29,29,29,212,39,39,43,43,222,222,86,86,29,29,29,29,222,222,]),'ON':([123,146,],[162,183,]),'SHOW_LINKS':([0,],[7,]),'RSQBRACE':([200,215,220,221,229,230,233,241,243,244,],[-99,-99,-96,231,240,-99,-99,-95,-98,-97,]),'TRANSITION':([0,],[10,]),'SHOW_NETS':([0,],[12,]),'OR':([42,43,61,78,80,],[73,74,74,122,124,]),'SHOW_PLACES':([0,],[2,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'trans_in_net':([10,66,70,150,151,153,154,184,189,],[34,34,34,34,34,34,34,34,34,]),'trans_list_in_net':([65,69,148,149,],[101,107,185,186,]),'element_list_string':([77,99,158,160,],[118,144,196,199,]),'element_eq_list':([200,215,230,233,],[220,220,220,244,]),'trans_list':([10,66,70,150,151,153,154,184,189,],[36,104,108,187,188,190,191,216,217,]),'place_list_id':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'trans_list_id':([10,66,70,150,151,153,154,184,189,],[38,38,38,38,38,38,38,38,38,]),'in_net_link_list':([14,31,72,73,74,75,192,193,],[44,60,112,113,114,116,218,219,]),'union_element_list':([200,215,230,],[221,229,241,]),'place_list_ddot_id':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'place_in_net':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'element_list_id':([77,99,158,160,],[120,145,195,198,]),'net_list':([4,47,49,],[19,81,82,]),'place_list_id_with_capacity':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'place_list_in_net':([51,55,125,128,223,224,],[85,91,164,167,234,235,]),'trans_list_ddot_id':([10,66,70,150,151,153,154,184,189,],[37,37,37,37,37,37,37,37,37,]),'place_list_ddot_id_with_capacity':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'union_net_list':([46,64,122,124,],[79,100,161,163,]),'expression':([0,],[13,]),'place_list':([8,52,56,130,132,136,138,166,173,174,179,225,226,227,228,],[30,87,92,169,171,175,177,202,206,207,210,236,237,238,239,]),'element_value_list':([31,180,],[62,211,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> PETRINET net_list SEMI','expression',3,'p_new_net','./src/PetriNet_parser.py',23),
  ('net_list -> ID , net_list','net_list',3,'p_net_list','./src/PetriNet_parser.py',27),
  ('net_list -> ID','net_list',1,'p_net_list','./src/PetriNet_parser.py',28),
  ('net_list -> ARRAY_ID , net_list','net_list',3,'p_net_list','./src/PetriNet_parser.py',29),
  ('net_list -> ARRAY_ID','net_list',1,'p_net_list','./src/PetriNet_parser.py',30),
  ('expression -> PLACE place_list SEMI','expression',3,'p_new_place','./src/PetriNet_parser.py',45),
  ('place_list -> place_list_id','place_list',1,'p_place_list','./src/PetriNet_parser.py',50),
  ('place_list -> place_list_ddot_id','place_list',1,'p_place_list','./src/PetriNet_parser.py',51),
  ('place_list -> place_list_id_with_capacity','place_list',1,'p_place_list','./src/PetriNet_parser.py',52),
  ('place_list -> place_list_ddot_id_with_capacity','place_list',1,'p_place_list','./src/PetriNet_parser.py',53),
  ('place_list -> place_in_net','place_list',1,'p_place_list','./src/PetriNet_parser.py',54),
  ('place_list_id -> ID , place_list','place_list_id',3,'p_place_list_id','./src/PetriNet_parser.py',60),
  ('place_list_id -> ARRAY_ID , place_list','place_list_id',3,'p_place_list_id','./src/PetriNet_parser.py',61),
  ('place_list_id -> ID','place_list_id',1,'p_place_list_id','./src/PetriNet_parser.py',62),
  ('place_list_id -> ARRAY_ID','place_list_id',1,'p_place_list_id','./src/PetriNet_parser.py',63),
  ('place_list_ddot_id -> ID DDOT ID , place_list','place_list_ddot_id',5,'p_place_list_ddot_id','./src/PetriNet_parser.py',81),
  ('place_list_ddot_id -> ID DDOT ARRAY_ID , place_list','place_list_ddot_id',5,'p_place_list_ddot_id','./src/PetriNet_parser.py',82),
  ('place_list_ddot_id -> ARRAY_ID DDOT ID , place_list','place_list_ddot_id',5,'p_place_list_ddot_id','./src/PetriNet_parser.py',83),
  ('place_list_ddot_id -> ARRAY_ID DDOT ARRAY_ID , place_list','place_list_ddot_id',5,'p_place_list_ddot_id','./src/PetriNet_parser.py',84),
  ('place_list_ddot_id -> ID DDOT ID','place_list_ddot_id',3,'p_place_list_ddot_id','./src/PetriNet_parser.py',85),
  ('place_list_ddot_id -> ID DDOT ARRAY_ID','place_list_ddot_id',3,'p_place_list_ddot_id','./src/PetriNet_parser.py',86),
  ('place_list_ddot_id -> ARRAY_ID DDOT ID','place_list_ddot_id',3,'p_place_list_ddot_id','./src/PetriNet_parser.py',87),
  ('place_list_ddot_id -> ARRAY_ID DDOT ARRAY_ID','place_list_ddot_id',3,'p_place_list_ddot_id','./src/PetriNet_parser.py',88),
  ('place_list_id_with_capacity -> ID LPAREN NUMBER RPAREN , place_list','place_list_id_with_capacity',6,'p_place_list_id_with_capacity','./src/PetriNet_parser.py',123),
  ('place_list_id_with_capacity -> ARRAY_ID LPAREN NUMBER RPAREN , place_list','place_list_id_with_capacity',6,'p_place_list_id_with_capacity','./src/PetriNet_parser.py',124),
  ('place_list_id_with_capacity -> ARRAY_ID LPAREN NUMBER RPAREN','place_list_id_with_capacity',4,'p_place_list_id_with_capacity','./src/PetriNet_parser.py',125),
  ('place_list_id_with_capacity -> ID LPAREN NUMBER RPAREN','place_list_id_with_capacity',4,'p_place_list_id_with_capacity','./src/PetriNet_parser.py',126),
  ('place_list_ddot_id_with_capacity -> ID DDOT ID LPAREN NUMBER RPAREN , place_list','place_list_ddot_id_with_capacity',8,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',145),
  ('place_list_ddot_id_with_capacity -> ARRAY_ID DDOT ID LPAREN NUMBER RPAREN , place_list','place_list_ddot_id_with_capacity',8,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',146),
  ('place_list_ddot_id_with_capacity -> ID DDOT ARRAY_ID LPAREN NUMBER RPAREN , place_list','place_list_ddot_id_with_capacity',8,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',147),
  ('place_list_ddot_id_with_capacity -> ARRAY_ID DDOT ARRAY_ID LPAREN NUMBER RPAREN , place_list','place_list_ddot_id_with_capacity',8,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',148),
  ('place_list_ddot_id_with_capacity -> ARRAY_ID DDOT ID LPAREN NUMBER RPAREN','place_list_ddot_id_with_capacity',6,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',149),
  ('place_list_ddot_id_with_capacity -> ID DDOT ARRAY_ID LPAREN NUMBER RPAREN','place_list_ddot_id_with_capacity',6,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',150),
  ('place_list_ddot_id_with_capacity -> ARRAY_ID DDOT ARRAY_ID LPAREN NUMBER RPAREN','place_list_ddot_id_with_capacity',6,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',151),
  ('place_list_ddot_id_with_capacity -> ID DDOT ID LPAREN NUMBER RPAREN','place_list_ddot_id_with_capacity',6,'p_place_list_ddot_id_with_capacity','./src/PetriNet_parser.py',152),
  ('place_in_net -> ID LBRACE place_list_in_net RBRACE','place_in_net',4,'p_place_in_net','./src/PetriNet_parser.py',187),
  ('place_in_net -> ID LBRACE place_list_in_net RBRACE , place_list','place_in_net',6,'p_place_in_net','./src/PetriNet_parser.py',188),
  ('place_in_net -> ARRAY_ID LBRACE place_list_in_net RBRACE','place_in_net',4,'p_place_in_net','./src/PetriNet_parser.py',189),
  ('place_in_net -> ARRAY_ID LBRACE place_list_in_net RBRACE , place_list','place_in_net',6,'p_place_in_net','./src/PetriNet_parser.py',190),
  ('place_list_in_net -> ID , place_list_in_net','place_list_in_net',3,'p_place_list_in_net','./src/PetriNet_parser.py',212),
  ('place_list_in_net -> ARRAY_ID , place_list_in_net','place_list_in_net',3,'p_place_list_in_net','./src/PetriNet_parser.py',213),
  ('place_list_in_net -> ID LPAREN NUMBER RPAREN , place_list_in_net','place_list_in_net',6,'p_place_list_in_net','./src/PetriNet_parser.py',214),
  ('place_list_in_net -> ARRAY_ID LPAREN NUMBER RPAREN , place_list_in_net','place_list_in_net',6,'p_place_list_in_net','./src/PetriNet_parser.py',215),
  ('place_list_in_net -> ID','place_list_in_net',1,'p_place_list_in_net','./src/PetriNet_parser.py',216),
  ('place_list_in_net -> ID LPAREN NUMBER RPAREN','place_list_in_net',4,'p_place_list_in_net','./src/PetriNet_parser.py',217),
  ('place_list_in_net -> ARRAY_ID','place_list_in_net',1,'p_place_list_in_net','./src/PetriNet_parser.py',218),
  ('place_list_in_net -> ARRAY_ID LPAREN NUMBER RPAREN','place_list_in_net',4,'p_place_list_in_net','./src/PetriNet_parser.py',219),
  ('expression -> TRANSITION trans_list SEMI','expression',3,'p_new_transition','./src/PetriNet_parser.py',268),
  ('trans_list -> trans_list_id','trans_list',1,'p_trans_list','./src/PetriNet_parser.py',273),
  ('trans_list -> trans_list_ddot_id','trans_list',1,'p_trans_list','./src/PetriNet_parser.py',274),
  ('trans_list -> trans_in_net','trans_list',1,'p_trans_list','./src/PetriNet_parser.py',275),
  ('trans_list_id -> ID','trans_list_id',1,'p_trans_list_id','./src/PetriNet_parser.py',281),
  ('trans_list_id -> ID , trans_list','trans_list_id',3,'p_trans_list_id','./src/PetriNet_parser.py',282),
  ('trans_list_id -> ARRAY_ID','trans_list_id',1,'p_trans_list_id','./src/PetriNet_parser.py',283),
  ('trans_list_id -> ARRAY_ID , trans_list','trans_list_id',3,'p_trans_list_id','./src/PetriNet_parser.py',284),
  ('trans_list_ddot_id -> ID DDOT ID','trans_list_ddot_id',3,'p_trans_list_ddot_id','./src/PetriNet_parser.py',302),
  ('trans_list_ddot_id -> ID DDOT ID , trans_list','trans_list_ddot_id',5,'p_trans_list_ddot_id','./src/PetriNet_parser.py',303),
  ('trans_list_ddot_id -> ARRAY_ID DDOT ID','trans_list_ddot_id',3,'p_trans_list_ddot_id','./src/PetriNet_parser.py',304),
  ('trans_list_ddot_id -> ARRAY_ID DDOT ID , trans_list','trans_list_ddot_id',5,'p_trans_list_ddot_id','./src/PetriNet_parser.py',305),
  ('trans_list_ddot_id -> ID DDOT ARRAY_ID','trans_list_ddot_id',3,'p_trans_list_ddot_id','./src/PetriNet_parser.py',306),
  ('trans_list_ddot_id -> ID DDOT ARRAY_ID , trans_list','trans_list_ddot_id',5,'p_trans_list_ddot_id','./src/PetriNet_parser.py',307),
  ('trans_list_ddot_id -> ARRAY_ID DDOT ARRAY_ID','trans_list_ddot_id',3,'p_trans_list_ddot_id','./src/PetriNet_parser.py',308),
  ('trans_list_ddot_id -> ARRAY_ID DDOT ARRAY_ID , trans_list','trans_list_ddot_id',5,'p_trans_list_ddot_id','./src/PetriNet_parser.py',309),
  ('trans_in_net -> ARRAY_ID LBRACE trans_list_in_net RBRACE , trans_list','trans_in_net',6,'p_trans_in_net','./src/PetriNet_parser.py',343),
  ('trans_in_net -> ID LBRACE trans_list_in_net RBRACE , trans_list','trans_in_net',6,'p_trans_in_net','./src/PetriNet_parser.py',344),
  ('trans_in_net -> ID LBRACE trans_list_in_net RBRACE','trans_in_net',4,'p_trans_in_net','./src/PetriNet_parser.py',345),
  ('trans_in_net -> ARRAY_ID LBRACE trans_list_in_net RBRACE','trans_in_net',4,'p_trans_in_net','./src/PetriNet_parser.py',346),
  ('trans_list_in_net -> ID , trans_list_in_net','trans_list_in_net',3,'p_trans_list_in_net','./src/PetriNet_parser.py',368),
  ('trans_list_in_net -> ID','trans_list_in_net',1,'p_trans_list_in_net','./src/PetriNet_parser.py',369),
  ('trans_list_in_net -> ARRAY_ID , trans_list_in_net','trans_list_in_net',3,'p_trans_list_in_net','./src/PetriNet_parser.py',370),
  ('trans_list_in_net -> ARRAY_ID','trans_list_in_net',1,'p_trans_list_in_net','./src/PetriNet_parser.py',371),
  ('expression -> ID LBRACE in_net_link_list RBRACE SEMI','expression',5,'p_new_link_sequence','./src/PetriNet_parser.py',541),
  ('expression -> ARRAY_ID LBRACE in_net_link_list RBRACE SEMI','expression',5,'p_new_link_sequence','./src/PetriNet_parser.py',542),
  ('in_net_link_list -> ARRAY_ID','in_net_link_list',1,'p_in_net_link_list','./src/PetriNet_parser.py',642),
  ('in_net_link_list -> ARRAY_ID LINK in_net_link_list','in_net_link_list',3,'p_in_net_link_list','./src/PetriNet_parser.py',643),
  ('in_net_link_list -> ARRAY_ID LINK LPAREN NUMBER RPAREN in_net_link_list','in_net_link_list',6,'p_in_net_link_list','./src/PetriNet_parser.py',644),
  ('in_net_link_list -> ARRAY_ID OR in_net_link_list','in_net_link_list',3,'p_in_net_link_list','./src/PetriNet_parser.py',645),
  ('in_net_link_list -> ID LINK in_net_link_list','in_net_link_list',3,'p_in_net_link_list','./src/PetriNet_parser.py',646),
  ('in_net_link_list -> ID LINK LPAREN NUMBER RPAREN in_net_link_list','in_net_link_list',6,'p_in_net_link_list','./src/PetriNet_parser.py',647),
  ('in_net_link_list -> ID OR in_net_link_list','in_net_link_list',3,'p_in_net_link_list','./src/PetriNet_parser.py',648),
  ('in_net_link_list -> ID','in_net_link_list',1,'p_in_net_link_list','./src/PetriNet_parser.py',649),
  ('expression -> ID DDOT ID LPAREN element_list_id RPAREN SEMI','expression',7,'p_call_function_on_net','./src/PetriNet_parser.py',685),
  ('expression -> ID DDOT ID LPAREN element_list_string RPAREN SEMI','expression',7,'p_call_function_on_net','./src/PetriNet_parser.py',686),
  ('expression -> ARRAY_ID DDOT ID LPAREN element_list_id RPAREN SEMI','expression',7,'p_call_function_on_net','./src/PetriNet_parser.py',687),
  ('expression -> ARRAY_ID DDOT ID LPAREN element_list_string RPAREN SEMI','expression',7,'p_call_function_on_net','./src/PetriNet_parser.py',688),
  ('element_list_id -> ID','element_list_id',1,'p_element_list_id','./src/PetriNet_parser.py',751),
  ('element_list_id -> ID , element_list_id','element_list_id',3,'p_element_list_id','./src/PetriNet_parser.py',752),
  ('element_list_id -> ID , element_list_string','element_list_id',3,'p_element_list_id','./src/PetriNet_parser.py',753),
  ('element_list_id -> <empty>','element_list_id',0,'p_element_list_id','./src/PetriNet_parser.py',754),
  ('element_list_string -> STRING','element_list_string',1,'p_element_list_string','./src/PetriNet_parser.py',772),
  ('element_list_string -> STRING , element_list_id','element_list_string',3,'p_element_list_string','./src/PetriNet_parser.py',773),
  ('element_list_string -> STRING , element_list_string','element_list_string',3,'p_element_list_string','./src/PetriNet_parser.py',774),
  ('expression -> ID = LPAREN union_net_list RPAREN ON LSQBRACE union_element_list RSQBRACE SEMI','expression',10,'p_union','./src/PetriNet_parser.py',782),
  ('expression -> ARRAY_ID = LPAREN union_net_list RPAREN ON LSQBRACE union_element_list RSQBRACE SEMI','expression',10,'p_union','./src/PetriNet_parser.py',783),
  ('union_element_list -> element_eq_list , union_element_list','union_element_list',3,'p_union_element_list','./src/PetriNet_parser.py',878),
  ('union_element_list -> element_eq_list','union_element_list',1,'p_union_element_list','./src/PetriNet_parser.py',879),
  ('element_eq_list -> ID = element_eq_list','element_eq_list',3,'p_element_eq_list','./src/PetriNet_parser.py',888),
  ('element_eq_list -> ID AS ID_IN_ID','element_eq_list',3,'p_element_eq_list','./src/PetriNet_parser.py',889),
  ('element_eq_list -> <empty>','element_eq_list',0,'p_element_eq_list','./src/PetriNet_parser.py',890),
  ('union_net_list -> ID OR union_net_list','union_net_list',3,'p_union_net_list','./src/PetriNet_parser.py',904),
  ('union_net_list -> ARRAY_ID OR union_net_list','union_net_list',3,'p_union_net_list','./src/PetriNet_parser.py',905),
  ('union_net_list -> ID','union_net_list',1,'p_union_net_list','./src/PetriNet_parser.py',906),
  ('union_net_list -> ARRAY_ID','union_net_list',1,'p_union_net_list','./src/PetriNet_parser.py',907),
  ('expression -> # ID = ID','expression',4,'p_preprocess_directive','./src/PetriNet_parser.py',925),
  ('expression -> COMMENT','expression',1,'p_comment','./src/PetriNet_parser.py',933),
  ('expression -> SEMI','expression',1,'p_empty_line','./src/PetriNet_parser.py',941),
  ('expression -> SHOW_NETS SEMI','expression',2,'p_show_nets','./src/PetriNet_parser.py',956),
  ('expression -> SHOW_PLACES SEMI','expression',2,'p_show_places','./src/PetriNet_parser.py',967),
  ('expression -> SHOW_TRANSITIONS SEMI','expression',2,'p_show_transitions','./src/PetriNet_parser.py',991),
  ('expression -> SHOW_LINKS SEMI','expression',2,'p_show_links','./src/PetriNet_parser.py',1026),
  ('expression -> ID LBRACE element_value_list RBRACE SEMI','expression',5,'p_mark','./src/PetriNet_parser.py',1048),
  ('element_value_list -> ID = NUMBER , element_value_list','element_value_list',5,'p_element_value_list','./src/PetriNet_parser.py',1063),
  ('element_value_list -> ID = NUMBER','element_value_list',3,'p_element_value_list','./src/PetriNet_parser.py',1064),
]