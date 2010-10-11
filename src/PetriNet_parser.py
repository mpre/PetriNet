#! /usr/bin/python
# -*- coding: utf-8 -*-
import ply.yacc as yacc
import PetriNet
import sys
import copy
import optparse

precedence = (('left', 'ON'), ('left',  'SEMI'))

nets = {} # Dizionario delle reti 
places = {} # Tupla dei posti *liberi* da rete
transitions = {} # Tupla delle transizioni *libere* da rete
links = {} # Tupla dei links *liberi* da rete
#foo = [] # Tupla utilizzata per passare valori all'interno di chiamate tra varie regole
# Regole per il parsing

argv = {}
#===============================================================================
# # Regole per le nuove reti
#===============================================================================
def p_new_net(p):
    """expression : PETRINET net_list SEMI"""
    print 'p_new_net'
    
def p_net_list(p):
    """net_list : ID ',' net_list
                | ID 
                | ARRAY_ID ',' net_list
                | ARRAY_ID"""
    if p[1].__class__.__name__ == 'list':
        # È un array di reti
        net_name, dimension = p[1]
        nets[net_name] = [PetriNet.PetriNet('{0}[{1}]'.format(net_name, i)) for i in range(dimension)]
    else:
        nets[str(p[1])] = PetriNet.PetriNet(str(p[1]))
#    nets.append(PetriNet.PetriNet(str(p[1])))
    print 'p_net_list'

#===============================================================================
# # Regole per l'aggiunta di un nuovo posto
# # esempio: Place [...] ;
#===============================================================================
def p_new_place(p):
    """expression : PLACE place_list SEMI
                  """
    print 'p_new_place'
    
def p_place_list(p):
    """place_list : place_list_id
                  | place_list_ddot_id
                  | place_list_id_with_capacity
                  | place_list_ddot_id_with_capacity
                  | place_in_net"""
    print 'p_place_list'
                  
# Lista di posti, il cui primo è dato con il solo id
# esempio [...], x, [...]
def p_place_list_id(p):
    """place_list_id : ID ',' place_list
                     | ARRAY_ID ',' place_list
                     | ID
                     | ARRAY_ID """
    if p[1].__class__.__name__ == 'list':
        place_name, place_dimension = p[1]
        if not place_name in places and not place_name in transitions:
            places[place_name] = [PetriNet.Place('{0}[{1}]'.format(place_name, i)) for i in range(place_dimension)]
        else:
            print 'It seems that element {0} is already declared'.format(place_name)
    else:
        place = PetriNet.Place(str(p[1]))
        if not place in places.values() and not place.name in transitions:
            places[place.name] = place
        else:
            print 'It seems that element {0} is already declared'.format(place.name)
    print 'p_place_list_id'

# Lista di posti, il cui primo è dato dall'id della rete e dal suo nome
# esempio: [...] x::a, [...]
def p_place_list_ddot_id(p):             
    """place_list_ddot_id : ID DDOT ID ',' place_list
                          | ID DDOT ARRAY_ID ',' place_list
                          | ARRAY_ID DDOT ID ',' place_list
                          | ARRAY_ID DDOT ARRAY_ID ',' place_list
                          | ID DDOT ID
                          | ID DDOT ARRAY_ID
                          | ARRAY_ID DDOT ID
                          | ARRAY_ID DDOT ARRAY_ID"""
    if p[1].__class__.__name__ == 'list':
        # Rete interna ad un array
        net_name, net_position = p[1]
        net = nets[net_name][net_position]
        if p[3].__class__.__name__ == 'list':
            place_name, dimension = p[3]
            for i in range(dimension):
                net_place(net,'{0}[{1}]'.format(place_name, i))
        else:
            net_place(net, str(p[3]))
            
    else:
        net_name = p[1]
        if nets[net_name].__class__.__name__ == 'list':
            # Array di reti
            for net in nets[net_name]:
                if p[3].__class__.__name__ == 'list':
                    place_name, dimension = p[3]
                    for i in range(dimension):
                        net_place(net, '{0}[{1}]'.format(place_name, i))
                else:
                    net_place(net, str(p[3]))
        else:
            if p[3].__class__.__name__ == 'list':
                place_name, dimension = p[3]
                for i in range(dimension):
                    net_place(nets[str(p[1])], '{0}[{1}]'.format(place_name, i))
            else:
                net_place(nets[str(p[1])], str(p[3]))
    print 'p_place_list_ddot_id'

# Lista di posti, il cui primo è dato dall'id del posto e dalla sua capacità
# esempio [...] x(7), [...]    
def p_place_list_id_with_capacity(p):
    """place_list_id_with_capacity : ID LPAREN NUMBER RPAREN ',' place_list
                                   | ARRAY_ID LPAREN NUMBER RPAREN ',' place_list
                                   | ARRAY_ID LPAREN NUMBER RPAREN
                                   | ID LPAREN NUMBER RPAREN"""
    if p[1].__class__.__name__ == 'list':
        place_name, dimension = p[1]
        if not place_name in places:
            places[place_name] = [PetriNet.Place('{0}[{1}]'.format(place_name, i), p[3]) for i in range(dimension)]
        else:
            print 'It seems that {0} is already declared'.format(place_name)
    else:
        place = PetriNet.Place(str(p[1]), p[3])
        if not place in places.values() and not place.name in transitions:
            places[place.name] = place
        else:
            print 'It seems that {0} is already declared'.format(place.name)
    print 'p_place_list_id_with_capacity'
    
# Lista di posti, il cui primo è dato dall'id della rete nel quale viene dichiarato, l'id del posto
# e la sua capacità
# esempio [...] net::place(7), [...]
def p_place_list_ddot_id_with_capacity(p):
    """place_list_ddot_id_with_capacity : ID DDOT ID LPAREN NUMBER RPAREN ',' place_list
                                        | ARRAY_ID DDOT ID LPAREN NUMBER RPAREN ',' place_list
                                        | ID DDOT ARRAY_ID LPAREN NUMBER RPAREN ',' place_list
                                        | ARRAY_ID DDOT ARRAY_ID LPAREN NUMBER RPAREN ',' place_list
                                        | ARRAY_ID DDOT ID LPAREN NUMBER RPAREN
                                        | ID DDOT ARRAY_ID LPAREN NUMBER RPAREN
                                        | ARRAY_ID DDOT ARRAY_ID LPAREN NUMBER RPAREN
                                        | ID DDOT ID LPAREN NUMBER RPAREN"""
    if p[1].__class__.__name__ == 'list':
        net_name, net_position = p[1]
        if p[3].__class__.__name__ == 'list':
            # Aggiunta array di posti a rete
            place_name, place_dimension = p[3]
            for i in range(place_dimension):
                net_place(nets[net_name][net_position], '{0}[{1}]'.format(place_name, i), p[5])
        else:
            net_place(nets[net_name][net_position], p[3], p[5])
    else:
        if nets[p[1]].__class__.__name__ == 'list':
            # Array di reti
            for net in nets[p[1]]:
                if p[3].__class__.__name__ == 'list':
                    # Aggiunta array di posti a rete
                    place_name, place_dimension = p[3]
                    for i in range(place_dimension):
                        net_place(net, '{0}[{1}]'.format(place_name, i), p[5])
                else:
                    net_place(net, p[3], p[5])
        else:
            # Rete singola
            if p[3].__class__.__name__ == 'list':
                # Aggiunta array di posti a rete
                place_name, place_dimension = p[3]
                for i in range(place_dimension):
                    net_place(nets[p[1]], '{0}[{1}]'.format(place_name, i), p[5])
            else:
                net_place(nets[p[1]], p[3], p[5])
    print 'p_place_list_ddot_id_with_capacity'

# Dichiarazione comoda di posti interni ad una rete 
# esempio: Place net_name{p1, p2, p3};
def p_place_in_net(p):
    """place_in_net : ID LBRACE place_list_in_net RBRACE
                    | ID LBRACE place_list_in_net RBRACE ',' place_list
                    | ARRAY_ID LBRACE place_list_in_net RBRACE
                    | ARRAY_ID LBRACE place_list_in_net RBRACE ',' place_list 
    """
    if p[1].__class__.__name__ == 'list':
        net_name, net_pos = p[1]
        for index in range(len(p[3]) - 1)[::2]:
            pla = PetriNet.Place(p[3][index], p[3][index+1])
            nets[net_name][net_pos].add(pla)
    else:
        if nets[p[1]].__class__.__name__ == 'list':
            for net in nets[p[1]]:
                for index in range(len(p[3]) - 1)[::2]:
                    pla = PetriNet.Place(p[3][index], p[3][index+1])
                    net.add(pla)
        else:
            net_name = p[1]
            #    print range(p[4]) - 1
            for index in range(len(p[3]) - 1)[::2]:
                pla = PetriNet.Place(p[3][index], p[3][index+1])
                nets[net_name].add(pla)
    print 'p_new_place_in_net'

def p_place_list_in_net(p):
    """place_list_in_net : ID ',' place_list_in_net
                         | ARRAY_ID ',' place_list_in_net
                         | ID LPAREN NUMBER RPAREN ',' place_list_in_net
                         | ARRAY_ID LPAREN NUMBER RPAREN ',' place_list_in_net
                         | ID
                         | ID LPAREN NUMBER RPAREN
                         | ARRAY_ID
                         | ARRAY_ID LPAREN NUMBER RPAREN
                         """
    if p[1].__class__.__name__ == 'list':
        place_name, place_dim = p[1]
        if len(p) == 2:
            # Ultimo ID di array di posti, senza capacità
            p[0] = []
            for i in range(place_dim):
                p[0] += ['{0}[{1}]'.format(place_name, i), 1]
        elif p[2] == ',':
            # ID di array di posti senza capacità
            p[0] = []
            for i in range(place_dim):
                p[0] += ['{0}[{1}]'.format(place_name, i), 1]
            p[0] += p[3]
        elif len(p)  == 5:
            # Ultimo ID di array di posti con capacità
            p[0] = []
            for i in range(place_dim):
                p[0] += ['{0}[{1}]'.format(place_name, i), p[3]]
        else:
            # ID di array di posti con capacità
            p[0] = []
            for i in range(place_dim):
                p[0] += ['{0}[{1}]'.format(place_name, i), p[3]]
            p[0] += p[6]
    else:
        if len(p) == 2:
            # Ultimo ID di posto, senza capacità
            p[0] = [str(p[1]), 1]
        elif p[2] == ',':
            # ID di posto senza capacità
            p[0] = [str(p[1]), 1]
            p[0] += p[3]
        elif len(p)  == 5:
            # Ultimo ID di posto con capacità
            p[0] = [str(p[1]), int(p[3])]
        else:
            # ID di posto con capacità
            p[0] = [str(p[1]), int(p[3])]
            p[0] += p[6]
    print 'p_place_list_in_net'

#===============================================================================
# # Regole per l'aggiunta di una nuova transizione
#===============================================================================
#
# esempio: Transition [...] ;
def p_new_transition(p):
    """expression : TRANSITION trans_list SEMI
                  """
    print 'p_new_transition'
    
def p_trans_list(p):
    """trans_list : trans_list_id
                  | trans_list_ddot_id
                  | trans_in_net """
    print 'p_trans_list'
    
# Transizione con il solo ID
# esempio: [...] x, [...]
def p_trans_list_id(p):
    """trans_list_id : ID
                     | ID ',' trans_list
                     | ARRAY_ID
                     | ARRAY_ID ',' trans_list"""
    if p[1].__class__.__name__ == 'list':
        trans_name, trans_dim = p[1]
        if not trans_name in transitions and not trans_name in places:
            transitions[trans_name] = [PetriNet.Transition('{0}[{1}]'.format(trans_name, i)) for i in range(trans_dim)]
        else:
            print 'It seems that {0} is already declared'.format(trans_name)
    else:
        trans = PetriNet.Transition(str(p[1]))
        if not trans in transitions.values() and not trans.name in places:
            transitions[trans.name] = trans
        else:
            print 'It seems that {0} is already declared'.format(trans.name)
    print 'p_trans_list_id'

# Transitione dichiarata con ID della rete e della transizione
# esempio: [...] net::trans, [...]
def p_trans_list_ddot_id(p):
    """trans_list_ddot_id : ID DDOT ID
                          | ID DDOT ID ',' trans_list 
                          | ARRAY_ID DDOT ID
                          | ARRAY_ID DDOT ID ',' trans_list
                          | ID DDOT ARRAY_ID
                          | ID DDOT ARRAY_ID ',' trans_list
                          | ARRAY_ID DDOT ARRAY_ID
                          | ARRAY_ID DDOT ARRAY_ID ',' trans_list"""
    if p[1].__class__.__name__ == 'list':
        net_name, net_position = p[1]
        net = nets[net_name][net_position]
        if p[3].__class__.__name__ == 'list':
            trans_name, dimension = p[3]
            for i in range(dimension):
                net_trans(net,'{0}[{1}]'.format(trans_name, i))
        else:
            net_trans(net, str(p[3]))
            
    else:
        net_name = p[1]
        if nets[net_name].__class__.__name__ == 'list':
            # Array di reti
            for net in nets[net_name]:
                if p[3].__class__.__name__ == 'list':
                    trans_name, dimension = p[3]
                    for i in range(dimension):
                        net_trans(net, '{0}[{1}]'.format(trans_name, i))
                else:
                    net_trans(net, str(p[3]))
        else:
            if p[3].__class__.__name__ == 'list':
                trans_name, dimension = p[3]
                for i in range(dimension):
                    net_trans(nets[str(p[1])], '{0}[{1}]'.format(trans_name, i))
            else:
                net_trans(nets[str(p[1])], str(p[3]))
    print 'p_trans_list_ddot_id'

# Dichiarazione comoda di transizione interni ad una rete 
# esempio: Transition net_name{t1, t2, t3};
def p_trans_in_net(p):
    """trans_in_net : ARRAY_ID LBRACE trans_list_in_net RBRACE ',' trans_list
                    | ID LBRACE trans_list_in_net RBRACE ',' trans_list
                    | ID LBRACE trans_list_in_net RBRACE
                    | ARRAY_ID LBRACE trans_list_in_net RBRACE
    """
    if p[1].__class__.__name__ == 'list':
        net_name, net_pos = p[1]
        for index in range(len(p[3])):
            tr = PetriNet.Transition(p[3][index])
            nets[net_name][net_pos].add(tr)
    else:
        if nets[p[1]].__class__.__name__ == 'list':
            for net in nets[p[1]]:
                for index in range(len(p[3])):
                    tr = PetriNet.Transition(p[3][index])
                    net.add(tr)
        else:
            net_name = p[1]
            #    print range(p[4]) - 1
            for index in range(len(p[3])):
                tr = PetriNet.Transition(p[3][index])
                nets[net_name].add(tr)
    print 'p_new_trans_in_net'

def p_trans_list_in_net(p):
    """trans_list_in_net : ID ',' trans_list_in_net
                         | ID
                         | ARRAY_ID ',' trans_list_in_net
                         | ARRAY_ID
                         """
    if p[1].__class__.__name__ == 'list':
        if len(p) == 2:
            # Ultimo ID di array di transizioni
            trans_name, trans_dim = p[1]
            p[0] = []
            for i in range(trans_dim):
                p[0] += ['{0}[{1}]'.format(trans_name, i)]
        else:
            # ID di array di transizioni
            trans_name, trans_dim = p[1]
            p[0] = []
            for i in range(trans_dim):
                p[0] += ['{0}[{1}]'.format(trans_name, i)]
            p[0] += p[3]
    else:
        if len(p) == 2:
            # Ultimo ID di transizione
            p[0] = [str(p[1])]
        else:
            # ID di transizione
            p[0] = [str(p[1])]
            p[0] += p[3]
    print 'p_trans_list_in_net'

#===============================================================================
# # Creazione Link
#===============================================================================
#===============================================================================
# def p_new_link(p):
#    """expression : link_list
#    """
#    
#    #              | link_ddot_list
#    #              """
#    
#    # In p[1] avremo una lista di elementi (vedi p_link_list per più dettagli)
#    # 
#    if str(p[1][len(p[1]) - 1]) in nets.keys():
#        # Serie di elementi interni ad una rete.
#        # I link vengono creati all'interno della rete stessa
#        net_name = p[1].pop()
#        for index in range(len(p[1]) - 1)[::2]:
#            link = PetriNet.Link(p[1][index], p[1][index + 2], int(p[1][index + 1]))
#            nets[net_name].add(link)
#    else:
#        # Serie di elementi non interno ad una rete
#        for index in range(len(p[1]) - 1)[::2]:
#            if index >= len(p[1]) - 2:
#                pass
#            else:
#                if p[1][index] in places:
#                    actual_place = p[1][index]
#                    actual_trans = p[1][index + 2]
#                else:
#                    actual_place = p[1][index + 2]
#                    actual_trans = p[1][index]
#                link = PetriNet.Link(actual_place, actual_trans, int(p[1][index + 1]))
#                link_name = '{0}->({1}){2}'.format(link.pre.name, link.weight, link.post.name)
#                if not link_name in links:
#                    links[link_name] = link
# #    print link_name, link
#    print 'p_new_link'
# 
# def p_link_list(p):
#    """link_list : ID LINK link_list
#                 | ID LINK LPAREN NUMBER RPAREN link_list
#                 | ID SEMI
#                 | ARRAY_ID LINK link_list
#                 | ARRAY_ID LINK LPAREN NUMBER RPAREN link_list
#                 | ARRAY_ID SEMI"""
#    if p[1].__class__.__name__ == 'list':
#        p[1] = '{0}[{1}]'.format(p[1][0], str(p[1][1]))
#    # Link tra posti esterni ad ogni rete, utilità nulla?
#    actual_element = PetriNet.PetriNetElement(str(p[1]))
#    if not actual_element.name in places and not actual_element.name in transitions:
#        print 'ID {0} not recognized'.format(actual_element.name)
#    else:
#        p[0] = []
#        if actual_element.name in places:
#            p[0] += [places[actual_element.name]]
#            #===================================================================
#            # # E' un posto
#            # # TODO : Migliorare il seguente pezzo
#            # for place in places.values():
#            #    if actual_element == place:
#            #        pl = place
#            #        break
#            # p[0] += [pl]
#            #===================================================================
#        else:             
#            # E' una transizione
#            # TODO : Migliorare il seguente pezzo
#            #===================================================================
#            # for trans in transitions.values():
#            #    if actual_element == trans:
#            #        tr = trans
#            #        break
#            #===================================================================
#            p[0] += [transitions[actual_element.name]]
#        if p[2] != ';':
#            if p[3] == '(':
#                p[0] += str(p[4])
#                p[0] += p[6]
#            else:
#                p[0] += str(1)
#                p[0] += p[3]      
#    print 'p_link_list'
#===============================================================================

#===============================================================================
# def p_link_ddot_list(p):
#    """link_ddot_list : ID DDOT ID LINK link_ddot_list
#                      | ID DDOT ID LINK LPAREN NUMBER RPAREN link_ddot_list
#                      | ID DDOT ID SEMI"""
#    p[0] = []
#    actual_net = nets[str(p[1])] # Rete alla quale appartiene il posto
# #    position = -1 
#    # Ricerca della rete all'interno dell'array delle reti
# #    for net in nets:
# #        if actual_net.name == net.name:
# #            position = nets.index(net)
# #            break
#    if actual_net.name in nets: #position != -1:
#        # Rete trovata
#        actual_element = PetriNet.PetriNetElement(str(p[3]))
#        if actual_element in nets[actual_net.name].places:
#            # E' un posto
#            # TODO : Migliorare il seguente pezzo
#            for place in nets[actual_net.name].places:
#                if actual_element == place:
#                    pl = place
#                    break
#            p[0] += [pl]
#        elif actual_element in nets[actual_net.name].transitions:
#            # E' una transizione
#            # TODO : Migliorare il seguente pezzo
#            for trans in nets[actual_net.name].transitions:
#                if actual_element == trans:
#                    tr = trans
#                    break
#            p[0] += [tr]
#        else:
#            print 'It seems that an element named {0} is not in {1}-named Petri net yet'.format(actual_element.name, actual_net.name)
#    else:
#        print 'No net named {0} found. Did you declared it?'.format(actual_net.name)
#    if p[4] == ';':
#        # In questo caso è l'ultimo elemento, salvo in fondo alla lista il nome della rete
#        p[0] += [actual_net.name]
#    elif p[5] == '(':
#        # E' presente il peso dell'arco
#        p[0] += str(p[6])
#        p[0] += p[8]
#    else:
#        # Non è presente il peso dell'arco
#        # di default lascio 1
#        p[0] += str(1)
#        p[0] += p[5]
#    print 'p_link_ddot_list' 
#===============================================================================
    
#===============================================================================
# # Flusso di esecuzione
# # Serve a descrivere in maniera compatta una serie di link
# # esemmpio:
# # nome_rete { p1 -> t1 -> p2 -> t2
# #            |p3 -> t4 -> p1}; 
#===============================================================================
def p_new_link_sequence(p):
    #===========================================================================
    # TODO : MIGLIORARE QUESTA REGOLA
    # 
    #===========================================================================
    """expression : ID LBRACE in_net_link_list RBRACE SEMI 
                  | ARRAY_ID LBRACE in_net_link_list RBRACE SEMI
    """
    is_weight = False
    if p[1].__class__.__name__ == 'list':
        net_name, net_pos = p[1]
        if net_name in nets:
            net = nets[net_name][net_pos]
            for index in range(len(p[3]) - 1):
                if is_weight:
                    is_weight = False
                    pass
                else:
                    if p[3][index] == '|' or p[3][index + 1] == '|':
                        index = index + 1
                    element_a = PetriNet.PetriNetElement(p[3][index])
                    if element_a in net.places:
                        # Link tra posto e transizione
                        element_a = net.places[net.places.index(element_a)]
                        weight = int(p[3][index + 1])
                        element_b = PetriNet.Transition(p[3][index+2])
                        link = PetriNet.Link(element_a, element_b, weight)
                        net.add(link)
                    elif element_a in net.transitions:
                        # Link tra transizione e posto
                        element_a = PetriNet.Transition(p[3][index])
                        weight = int(p[3][index + 1])
                        element_b = PetriNet.PetriNetElement(p[3][index + 2])
                        element_b = net.places[net.places.index(element_b)]
                        link = PetriNet.Link(element_a, element_b, weight)
                        net.add(link)
                    is_weight = True
        else:
            print 'No {0}-named net declared yet'.format(str(p[1]))
    else:
        if nets[p[1]].__class__.__name__ == 'list':
            # Caso di link generalizzati su array di reti
            for net in nets[p[1]]:
                for index in range(len(p[3]) - 1):
                    if is_weight:
                        is_weight = False
                        pass
                    else:
                        if p[3][index] == '|' or p[3][index + 1] == '|':
                            index = index + 1
                        element_a = PetriNet.PetriNetElement(p[3][index])
                        if element_a in net.places:
        #                    print 'here'
                            # Link tra posto e transizione
                            element_a = net.places[net.places.index(element_a)]
                            weight = int(p[3][index + 1])
                            element_b = PetriNet.Transition(p[3][index+2])
                            link = PetriNet.Link(element_a, element_b, weight)
                            net.add(link)
                        elif element_a in net.transitions:
                            # Link tra transizione e posto
                            element_a = PetriNet.Transition(p[3][index])
                            weight = int(p[3][index + 1])
                            element_b = PetriNet.PetriNetElement(p[3][index + 2])
                            element_b = net.places[net.places.index(element_b)]
                            link = PetriNet.Link(element_a, element_b, weight)
                            net.add(link)
                        is_weight = True
        else:
            # Caso di ID di rete
            if str(p[1]) in nets.keys():
                net_name = str(p[1])
                for index in range(len(p[3]) - 1):
                    if is_weight:
                        is_weight = False
                        pass
                    else:
                        if p[3][index] == '|' or p[3][index + 1] == '|':
                            index = index + 1
                        element_a = PetriNet.PetriNetElement(p[3][index])
                        if element_a in nets[net_name].places:
        #                    print 'here'
                            # Link tra posto e transizione
                            element_a = nets[net_name].places[nets[net_name].places.index(element_a)]
                            weight = int(p[3][index + 1])
                            element_b = PetriNet.Transition(p[3][index+2])
                            link = PetriNet.Link(element_a, element_b, weight)
                            nets[net_name].add(link)
                        elif element_a in nets[net_name].transitions:
                            # Link tra transizione e posto
                            element_a = PetriNet.Transition(p[3][index])
                            weight = int(p[3][index + 1])
                            element_b = PetriNet.PetriNetElement(p[3][index + 2])
                            element_b = nets[net_name].places[nets[net_name].places.index(element_b)]
                            link = PetriNet.Link(element_a, element_b, weight)
                            nets[net_name].add(link)
                        is_weight = True
            else:
                print 'No {0}-named net declared yet'.format(str(p[1]))
    print 'p_new_link_sequence'
    
def p_in_net_link_list(p):
    """in_net_link_list : ARRAY_ID
                        | ARRAY_ID LINK in_net_link_list
                        | ARRAY_ID LINK LPAREN NUMBER RPAREN in_net_link_list
                        | ARRAY_ID OR in_net_link_list
                        | ID LINK in_net_link_list
                        | ID LINK LPAREN NUMBER RPAREN in_net_link_list
                        | ID OR in_net_link_list
                        | ID
    """
    if p[1].__class__.__name__ == 'list':
        p[1] = '{0}[{1}]'.format(p[1][0], p[1][1])
#        print 'ci sono'
#        print p[1]
#        p[0] = [p[1]]
#        
    if len(p) <= 2:
        # Solo ID finale
        p[0] = [str(p[1])]
    elif str(p[2]) == '|':                        
        # Nuovo flusso
        p[0] = [p[1], '|']
        p[0] += p[3]
    elif str(p[3]) == '(':
        # Link con peso
        p[0] = [str(p[1])]
        p[0] +=[str(p[4])]
        p[0] += p[6]
    else:
        # Link senza peso
        p[0] = [str(p[1])]
        p[0] +=[str(1)]
        p[0] += p[3]
    print 'p_in_net_link_list'
    
#===============================================================================
# # Chiamata funzioni su rete, questa funzione permette di chiamare tutti i metodi
# # interno alla classe PetriNet tramite l'utilizzo della funzione eval().
# # In questo modo è possibile dover riscrivere solo le i metodi all'interno della
# # classe Python e poter avere nuove funzionalità per il linguaggio.
# # esempio net::add(element);
# # esempio net::remove(element);
#===============================================================================
def p_call_function_on_net(p):
    """expression : ID DDOT ID LPAREN element_list_id RPAREN SEMI
                  | ID DDOT ID LPAREN element_list_string RPAREN SEMI
                  | ARRAY_ID DDOT ID LPAREN element_list_id RPAREN SEMI
                  | ARRAY_ID DDOT ID LPAREN element_list_string RPAREN SEMI
                    """
    # Rete sulla quale si lavora
#    actual_net = PetriNet.PetriNet(str(p[1]))
#    position = -1
    # Ricerca rete all'interno della tupla delle reti
    #===========================================================================
    # for net in nets:
    #    if actual_net.name == net.name:
    #        position = nets.index(net)
    #        break
    #===========================================================================
    array = False
    if p[1].__class__.__name__ == 'list':
        array = True
    if array:
        net_name, net_pos = p[1]
    else:
        net_name = p[1]
    if net_name in nets: #position != -1:
        # E' stata trovata le rete
        if array:
            actual_net = nets[net_name][net_pos]
        else:
            actual_net = nets[net_name]
        function = str(p[3])
        if hasattr(actual_net, function):
            # La rete contiene la funzione di nome function
            if array:
                to_evaluate = 'nets[\'{0}\'][{1}].{2}('.format(net_name, net_pos, function)                
            else:
                to_evaluate = 'nets[\'{0}\'].{1}('.format(net_name, function)
            # foo contiene i parametri passati all'interprete da 
            # *rigirare* al metodo python
            for x in p[5]:
                if hasattr(x, 'name'):
                    if x.name in places:
                        to_evaluate = '{0}places[\'{1}\'],'.format(to_evaluate, places[x.name])
                    elif x.name in transitions:
                        to_evaluate = '{0}transitions[\'{1}\'],'.format(to_evaluate, transitions[x.name])
                    elif x.name in links:
                        to_evaluate = '{0}links[\'{1}\'],'.format(to_evaluate, links[x.name])   
                else:
                    to_evaluate = '{0}{1},'.format(to_evaluate, x)   
            to_evaluate = '{0})'.format(to_evaluate[:-1])
            try:
                eval(to_evaluate)
            except Exception as e:
                print 'Execution of {0} failed \nError: {1}\n'.format(to_evaluate, e)
        else:
            '{0} doesn\'t have {1} method'.format(actual_net.name, function)
    # reset_foo server a cancellare i parmetri salvati momentaneamente
#    reset_foo()
    print 'p_call_function_on_net'


#===============================================================================
# # Lista di elementi il cui primo è riferito tramite un ID
# # dichiarato precedentemente.
# # Serve per poter passare gli argomenti delle funzioni in linguaggio PetriNet
# # alle classi in python
#===============================================================================
def p_element_list_id(p):
    """element_list_id : ID
                       | ID ',' element_list_id
                       | ID ',' element_list_string
                       |"""
    if len(p) > 1:
        x = PetriNet.PetriNetElement(str(p[1]))
        if x.name in places:
            x = PetriNet.Place(places[x.name].name, places[x.name].capacity)
        elif x in transitions:
            x = PetriNet.Transition(x.name)
        elif x in links:
            x = PetriNet.Link(links[x.name].pre, links[x.name].post, links[x.name].weight)
        p[0] = list()
        p[0] += [x]
        if len(p) > 2:
            p[0] += p[3]
    print 'p_element_list_id'
    
# In questo caso il parametro è una stringa e non un elemento delle reti
# di petri. Ad esempio può essere il percorso in cui salvare il fil dot
def p_element_list_string(p):
    """element_list_string : STRING
                           | STRING ',' element_list_id
                           | STRING ',' element_list_string"""
    p[0] = list()
    p[0] += [str(p[1])]
    if len(p) > 2:
        p[0] += [p[3]]
    print 'p_element_list_string'
    
def p_union(p):
    """expression : ID '=' LPAREN union_net_list RPAREN ON LSQBRACE union_element_list RSQBRACE SEMI

    """
    # union_net_list è la lista di N reti sulle quali si chiama l'unione
    # union_element_list è una lista di N+1 elementi, N elementi
    # sono gli elementi sui quali si deve fare l'unione degli elementi
    # mentre l'ultimo è il nome dell'elemento nella nuova rete
    un_nets = p[4]
    un_el = p[8]
    
    for element in un_el:
        if not len(element) == len(un_nets) + 1:
            print 'Error in union definition:', p[1]
            exit()
        cap, mark = None, None
        for i in range(len(element) -1):
            if PetriNet.Place(element[i]) in un_nets[i].places:
                index = un_nets[i].places.index(PetriNet.Place(element[i]))
                if argv['union_type'] == 'only_when_equal':
                    
                    if cap == None:
                        cap = un_nets[i].places[index].capacity
                    else:
                        if cap !=  un_nets[i].places[index].capacity:
                            print element[i],' capacity not equal to other one'
                            exit()
                    if mark == None:
                        mark =  un_nets[i].places[index].mark
                    else:
                        if mark !=  un_nets[i].places[index].mark:
                            print element[i],' mark not equal to other one'
                            exit()
                new_place = PetriNet.Place(element[len(element) -1], un_nets[i].places[index].capacity, un_nets[i].places[index].mark)
                un_nets[i].replace_place(un_nets[i].places[index], new_place)
            elif PetriNet.Transition(element[i]) in un_nets[i].transitions:
                index = un_nets[i].transitions.index(PetriNet.Transition(element[i]))
                new_trans = PetriNet.Transition(element[len(element) -1])
                un_nets[i].replace_transition(un_nets[i].transitions[index], new_trans)
                
            elif element[i] != 'null':
                print element[i], ' not in ',un_nets[i].name
                exit()
    # A questo punto avremo che tutti i i posti e tutte le transizioni sono stati modificati
    # correttamente. Non ci resta che creare una nuova rete e aggiungere ogni posto esistente
    # nelle reti dell'unione.
    new_net = PetriNet.PetriNet(p[1])
    for n in un_nets:
        for pl in n.places:
            if not pl in new_net.places:
                new_net.add(pl)
        for t in n.transitions:
            if not t in new_net.transitions:
                new_net.add(t)
        for l in n.links:
            new_net.add(l)
    nets[p[1]] = new_net
    print 'p_union'

def p_union_element_list(p):
    """ union_element_list : element_eq_list ',' union_element_list
                                       | element_eq_list    
    """
    el = [p[1]]
    if len(p) > 2:
        el += p[3]
    print 'p_union_element_list'
    p[0] = el

def p_element_eq_list(p):
    """ element_eq_list : ID '=' element_eq_list
                                  | ID AS element_eq_list
                                  | ID
    """
    ids = [p[1]]
    if len(p) > 2:
        ids += p[3]
    p[0] = ids
        
def p_union_net_list(p):
    """ union_net_list : ID OR union_net_list
                                | ARRAY_ID OR union_net_list
                                | ID
                                | ARRAY_ID"""
    net_list = []
    if p[1].__class__.__name__ == 'list':
        net_name, net_position = p[1]
        net_list += [nets[net_name][net_position]]
    else:
        net_list += [nets[p[1]]]
    if len(p) > 2:
        net_list += p[3]
    print 'p_union_net_list'
    p[0] = net_list
#===============================================================================
# # Commenti
#===============================================================================
def p_comment(p):
    """expression : COMMENT"""
    print 'p_comment'

#===============================================================================
# # Linea vuota
# # TODO: Verificarne il funzionamento
#===============================================================================
def p_empty_line(p):
    """expression : SEMI"""
    print 'p_empty_line'

#===============================================================================
# # Errore generico.
#===============================================================================
def p_error(p):
    if p is not None:
        print "SYNTAX ERROR in input: ",  p

#===============================================================================
# # Comandi per l'interprete PetriNet.
# # Utili per il debug
#===============================================================================
def p_show_nets(p):
    """expression : SHOW_NETS SEMI """
    for net in nets.values():
        if net.__class__.__name__ == 'list':
            for n1 in net:
                print n1
                print
        else:
            print net    
            print
    
def p_show_places(p):
    """expression : SHOW_PLACES SEMI"""
    net_places = []
    for net in nets.values():
        if net.__class__.__name__ == 'list':
            for n1 in net:
                for place in n1.places:
                    temp_place = copy.deepcopy(place)
                    temp_place.name = '{0}::{1}'.format(n1.name, temp_place.name) 
                    net_places.append(temp_place)
        else:
            for place in net.places:
                temp_place = copy.deepcopy(place)
                temp_place.name = '{0}::{1}'.format(net.name, temp_place.name) 
                net_places.append(temp_place)
    for element in places.values():
        if element.__class__.__name__ == 'list':
            for n in element:
                net_places.append(n)
        else:
            net_places.append(element)
    for p in net_places:
        print p#, p.capacity

def p_show_transitions(p):
    """expression : SHOW_TRANSITIONS SEMI """
    net_trans = []
    for net in nets.values():
        if net.__class__.__name__ == 'list':
            for n1 in net:
                for tr in n1.transitions:
                    temp_tr = copy.deepcopy(tr)
                    temp_tr.name = '{0}::{1}'.format(n1.name, temp_tr.name) 
                    net_trans.append(temp_tr)
        else:
            for tr in net.transitions:
                temp_tr = copy.deepcopy(tr)
                temp_tr.name = '{0}::{1}'.format(net.name, temp_tr.name) 
                net_trans.append(temp_tr)
    for element in transitions.values():
        if element.__class__.__name__ == 'list':
            for n in element:
                net_trans.append(n)
        else:
            net_trans.append(element)
    for p in net_trans:
        print p
    #===========================================================================
    # net_trans = []
    # for net in nets.values():
    #    for trans in net.transitions:
    #        temp_trans = copy.deepcopy(trans)
    #        temp_trans.name = '{0}::{1}'.format(net.name, temp_trans.name)
    #        net_trans.append(temp_trans)
    # for trans in transitions:
    #    net_trans.append(trans)
    # print net_trans
    #===========================================================================
    
def p_show_links(p):
    """expression : SHOW_LINKS SEMI """
    net_links = []
    for net in nets.values():
        for link in net.links:
            temp_link = copy.deepcopy(link)
            net_links.append(temp_link)
    for link in links:
        net_links.append(link)
    print net_links
    
#===============================================================================
# 
#===============================================================================
# #===============================================================================
#===============================================================================
# #===============================================================================
#===============================================================================
# #===============================================================================
#===============================================================================
# #===============================================================================
#===============================================================================
def p_mark(p):
    """expression : ID LBRACE element_value_list RBRACE SEMI
    """
    net_name = p[1]
    if nets[net_name].__class__.__name__ == 'list':
        # ID di array di reti
        for net in nets[net_name]:
            for place, mark in p[3]:
                net.set_mark(place, mark)
    else:
        net = nets[net_name]
        for place, mark in p[3]:
            net.set_mark(place, mark)
    print 'p_mark'
    
def p_element_value_list(p):
    """element_value_list : ID '=' NUMBER ',' element_value_list
                          | ID '=' NUMBER
    """
#    p[0] = []
    p[0] = [[p[1], p[3]]]
    if len(p) > 4:
        p[0] += p[5]
#===============================================================================
# # Funzioni di supporto
#===============================================================================

def net_place(net, place_name, place_cap=1):
    """Aggiunge un posto di nome place_name e capacità place_cap alla rete net"""
    place = PetriNet.Place(place_name, place_cap)
    if not place in net.places and not PetriNet.Transition(place_name) in net.transitions:
        net.add(place)
    else:
        print 'It seems that an element named {0} is already in {1}'.format(place.name, net.name) 
    return 

def net_trans(net, trans_name):
    """Aggiunge una transizione di nome trans_name alla rete net"""
    transition = PetriNet.Transition(trans_name)
    # Ricerca l'indice della rete che si chiama come acutal_net
    # all'interno di nets
#    position = -1
#    for net in nets:
#        if actual_net.name == net.name:
#            position = nets.index(net)
#            break
    if not transition in net.transitions and not PetriNet.Place(trans_name) in net.places:
        net.add(transition)
    else:
        print 'It seems that an element named {0} is already in {1}'.format(transition.name, net.name)
    return 

#===============================================================================
# # Main loop
#===============================================================================
from PetriNet_lex import tokens

def main():
    usage = "usage: %prog [-f INPUT_FILE] [-u UNION_STYLE] "
    arg_par = optparse.OptionParser(usage=usage)
    arg_par.add_option("-u", "--union-type", action="store",
                       type="choice", dest="union_type", choices=("only_when_equal", "override"),
                       default="only_when_equal",
                       help="Rappresenta il comportamento nell'unione su posti. \n only_when_equal[default]: permette l'unione solo se i posti hanno la stessa marcatura e la stessa capacita' \n override: il posto avra' capacita' e marcatura del primo posto dichiarato")
    arg_par.add_option("-f", "--file", action="store",
                       type="string", dest="input_file",
                       help="File su cui richiamare il parser")
    arg_par.add_option("-i", "--interactive", action="store_true",
                       dest="interactive", default=False,
                       help="Esegue il parser in modo interattivo (in questo caso il file passato non viene preso in considerazione")
    opts, args = arg_par.parse_args()
    argv['union_type'] = opts.union_type
    if not opts.interactive:
        try: 
            data=open(opts.input_file, 'r') #apertura del file in lettura
        except IOError: 
            print "Problem in opening the file"


        yacc.yacc() #faccio partire il parser
        s=data.readlines() #s è un array di tutte le righe del file
        for riga in s: #per tutte le righe eseguo il parsing
            if riga != '': 
                yacc.parse(riga+'\n') 
    else:
        yacc.yacc() 
        while 1: 
            try: #inserisco i comandi da riga di comando
                s = raw_input('petriNet > ') 
            except EOFError:
                break 
            if s=="":
                break
            yacc.parse(s+'\n')  

if __name__ == "__main__":
    main()
