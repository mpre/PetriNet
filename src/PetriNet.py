# -*- coding: utf-8 -*-
import copy
import os
import sys
import xml.etree.ElementTree as ET

class PetriNetElement(object):
    """Classe base che astrae i concetti di Posto, Transizione e Arco"""
  
    def __init__(self, name):
        self.__name = name
        
    def __eq__(self, other):
        return self.__name == other.name
        
    @property
    def name(self):
        return '{0}'.format(self.__name)
    
    @name.setter
    def name(self, name):
        self.__name = name
        
         
class Place(PetriNetElement):
    """Classe che rappresenta un Posto in una rete di Petri"""
   
    def __init__(self, name, capacity=1, mark = 0):
        self.name = name
        if int(capacity) > 0:
            self.__capacity = int(capacity)
        else:
            raise Exception('Capacity must be greater than 0.\n' + 
                            'Error occurred while working on Place : {0}'.format(self.name) )
        if int(mark) >= 0:
            self.__mark = mark
        else:
            raise Exception('Mark must be greater or equal than 0.\n' + 
                            'Error occurred while working on Place : {0}'.format(self.name) )
        
    def __repr__(self):
        return 'Place(\'{0}\',{1}, {2})'.format(self.name, self.__capacity, self.__mark)
    
    def __str__(self):
        return '{0}({1}/{2})'.format(self.name, self.__mark, self.__capacity)
    
    def __eq__(self, other):
        if other.__class__.__name__ in ('Place', 'PetriNetElement'):
            return other.name == self.name
        return False
    
    @property
    def capacity(self):
        return self.__capacity
    
    @capacity.setter
    def capacity(self, capacity):
        assert capacity > 0, 'Capacity must be nonzero and non-negative'
        self.__capacity = capacity
        
    @property
    def mark(self):
        return self.__mark
    
    @mark.setter
    def mark(self, mark):
        assert mark >= 0, 'Mark must be non-negative'
        self.__mark = mark
    
    
class Transition(PetriNetElement):
    """Classe che rappresenta una Transizione in una rete di Petri"""
    # Oltre al nome, nessun altro attributo
    
    def __repr__(self):
        return 'Transition(\'{0}\')'.format(self.name)
    
    def __str__(self):
        return '{0}'.format(self.name)
    
    def __eq__(self,other):
        if other.__class__.__name__ in ('Transition', 'PetriNetElement'):
            return other.name == self.name
        return False        
        
class Link(object):
    """Classe che rappresenta un arco della rete di Petri"""
   
    def __init__(self, pre, post, weight = 1):
        # L'arco deve avere un peso minimo di 1
        if int(weight) < 1:
            raise Exception('Link weight must be at least 1.')
        else:
            self.__weight = weight
        # Le reti di petri sono grafi bipartiti tra Posti e Transizioni
        if pre.__class__.__name__ != 'Place' and pre.__class__.__name__ != 'Transition':
            raise Exception('Arc must be from a Place to a Transition or viceversa')
        elif post.__class__.__name__ != 'Place' and post.__class__.__name__ != 'Transition':
            raise Exception('Arc must be from a Place to a Transition or viceversa')  
        elif pre.__class__.__name__ != post.__class__.__name__:
            self.__pre = pre
            self.__post = post
        else:
            raise Exception('Link must be from a Place to a Transition or viceversa')
        
    def __eq__(self, other):
        # Un arco è uguale ad un altro se va dallo stesso elemento nello stesso 
        # e se ha lo stesso peso
        if other.__class__.__name__ != 'Link':
            return False
        if self.__pre == other.pre and self.__post == other.post and self.__weight == other.weight:
            return True
        else:
            return False
    
    def __repr__(self):
        return 'Link({0},{1},{2})'.format(repr(self.__pre), repr(self.__post), self.__weight)
    
    def __str__(self):
        return '{0} ->({2}) {1}'.format(self.__pre.name, self.__post.name, self.__weight)
    
    @property
    def pre(self):
        return self.__pre
    
    @pre.setter
    def pre(self, pre):
        assert pre.__class__.__name__ != self.__post.__class__.__name__, 'PetriNet are bipartite graph so pre must be different than post'
        self.__pre = pre
    
    @property
    def post(self):
        return self.__post
    
    @post.setter
    def post(self, post):
        assert post.__class__.__name__ != self.__pre.__class__.__name__, 'PetriNet are bipartite graph so pre must be different than post'
        self.__post = post  
    
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, weight):
        assert weight > 1, 'Link\'s weight must be major than 1'
        self.__weight = weight
        
    
class PetriNet(object):
    """Classe che rappresenta una rete di Petri"""
    
    def __init__(self, name, places = [], transitions = [], links = []):
        self.__name = name
        self.__places = list() + places
        self.__transitions = list() + transitions
        self.__links = list() + links
        
    def __str__(self):
        return 'PetriNet : {0} \nPlaces : {1} \nTransitions : {2} \nLinks : {3}'.format(self.__name,
                                                                                        list('{0}({1})'.format(place.name, place.capacity) for place in self.__places),
                                                                                        list(transition.name for transition in self.__transitions),
                                                                                        list(str(link) for link in self.__links))
    
    def __repr__(self):
        return('PetriNet(\'{0}\',{1},{2},{3})'.format(self.name,
                                                  self.places,
                                                  self.transitions,
                                                  self.links))
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name
        
    @property
    def places(self):
        return self.__places
    
    @places.setter
    def places(self, places):
        raise Exception('Can\'t assign places list in this way, use add method instead')
    
    @property
    def transitions(self):
        return self.__transitions
    
    @transitions.setter
    def transitions(self, transitions):
        raise Exception('Can\'t assign transitions list in this way, use add method instead')
    
    @property
    def links(self):
        return self.__links
    
    @links.setter
    def links(self, links):
        raise Exception('Can\'t assign links list in this way, use add method instead')
        
    def add(self, element):
        """Aggiunta posti e transizioni alla rete di Petri"""
#        print self.__places 
#        print self.__transitions
        if element.__class__.__name__ == 'Place':
            if element in self.__places:
                raise Exception('{0} is already in {1}'.format(element.name, self.__name))
            else:
                self.__places.append(element)
        elif element.__class__.__name__ == 'Transition':
            if element in self.__transitions:
                pass
#                raise Exception('{0} is already in {1}'.format(element.name, self.__name))
            else:
                self.__transitions.append(element)
        elif element.__class__.__name__ == 'Link':
            if element in self.__links:
                print '{0} is already in {1} : skip'.format(element, self.__name)
            elif element.pre in self.__places and element.post in self.__transitions:
                self.__links.append(element)    
            elif element.pre in self.__transitions and element.post in self.__places:
                self.__links.append(element)
            else:
                print '{0} or {1} not in {2} : skip'.format(element.pre.name, element.post.name, self.__name)
        else:
            raise Exception('{0}\'s aren\'t PetriNet elements'.format(element.__class__.__name__))
        
    def remove(self, element):
        """Rimozione posti e transizioni dalla rete di Petri"""
        if element.__class__.__name__ in ('Place', 'Transition', 'PetriNetElement'):
            for link in [link for link in self.__links if element == link.pre or element == link.post]:
                self.remove(link)
#            if element in [link.pre for link in self.__links] or element in [link.post for link in self.__links]:
#                raise Exception('You must remove every link where {0} is in before you can delete it'.format(element.name))
        if element.__class__.__name__ == 'Place':
            if element not in self.__places:
                raise Exception('No place {0} in {1} net'.format(element.name, self.__name))
            else:
                self.__places.remove(element)
        elif element.__class__.__name__ == 'Transition':
            if element not in self.__transitions:
                raise Exception('No transition {0} in {1} net'.format(element.name, self.__name))
            else:
                self.__transitions.remove(element)
        elif element.__class__.__name__ == 'Link':
            if element not in self.__links:
                raise Exception('No link {0} in {1} net'.format(element, self.__name))
            else:
                self.__links.remove(element)   
        elif element.__class__.__name__ == 'PetriNetElement':
            if element in self.__places:
                self.__places.remove(element)
            elif element in self.__transitions:
                self.__transitions.remove(element)
        else:
            raise Exception('{0}s aren\'t PetriNet elements'.format(element.__class__.__name__))
        
    def replace_place(self, old_place, new_place):
        """Cambia tutte le occorrenze di old_place in occorrenze di new_place"""
        if old_place not in self.places:
            raise Exception('{0} not in {1}'.format(old_place.name, self.name))
#        modified = False
        new_links = []
        remove_links = []
        for link in self.__links:
            modified = False
            if link.pre.__class__.__name__ == 'Place':
                if link.pre == old_place:
                    new_link = Link(new_place, link.post, link.weight)
                    new_links += [new_link]
                    modified = True
            else:
                if link.post == old_place:
                    new_link = Link(link.pre, new_place, link.weight)
                    new_links += [new_link]
                    modified = True
            if modified:
                remove_links += [link]
        self.add(new_place)
        for link in remove_links:
            self.__links.remove(link)
        for link in new_links:
            self.add(link)
        self.remove(old_place)

            
    def duplicate_place(self, old_place, new_place):
        """Duplica tutte le occorrenze di old_place con occorrenze di new_place"""
        if old_place not in self.places:
            raise Exception('{0} not in {1}'.format(old_place.name, self.name))
        link_to_add = []
        for link in self.__links:
            if link.pre.__class__.__name__ == 'Place':
                if link.pre == old_place:
                    new_link = Link(new_place, link.post, link.weight)
                    link_to_add.append(new_link)
            else:
                if link.post == old_place:
                    new_link = Link(link.pre, new_place, link.weight)
                    link_to_add.append(new_link)
        self.add(new_place)
        for link in link_to_add:
            self.add(link)
            
    def duplicate_transition(self, old_trans, new_trans):
        """Duplica tutte le occorrenze di old_trans in occorrenze di new_trans"""
        if old_trans not in self.transitions:
            raise Exception('{0} not in {1}'.format(old_trans.name, self.name))
        link_to_add = []        
        for link in self.__links:
            if link.pre.__class__.__name__ == 'Transition':
                if link.pre == old_trans:
                    new_link = Link(new_trans, link.post, link.weight)
                    link_to_add.append(new_link)
            else:
                if link.post == old_trans:
                    new_link = Link(link.pre, new_trans, link.weight)
                    link_to_add.append(new_link)
        self.add(new_trans)
        for link in link_to_add:
            self.add(link)
            
    def replace_transition(self, old_trans, new_trans):
        """Cambia tutte le occorrenze di old_trans in occorrenze di new_trans"""
        if old_trans not in self.transitions:
            raise Exception('{0} not in {1}'.format(old_trans.name, self.name))
#        modified = False
        new_links = []
        remove_links = []
        for link in self.__links:
            modified = False
            if link.pre.__class__.__name__ == 'Transition':
                if link.pre == old_trans:
                    new_link = Link(new_trans, link.post, link.weight)
                    new_links += [new_link]
                    modified = True
            else:
                if link.post == old_trans:
                    new_link = Link(link.pre, new_trans, link.weight)
                    new_links += [new_link]
                    modified = True
            if modified:
                remove_links += [link]
        self.add(new_trans)
        for link in remove_links:
            self.__links.remove(link)
        for link in new_links:
            self.add(link)
        self.remove(old_trans)
        #=======================================================================
        # if old_trans not in self.transitions:
        #    raise Exception('{0} not in {1}'.format(old_trans.name, self.name))
        # for link in self.__links:
        #    modified = False
        #    if link.pre.__class__.__name__ == 'Transition':
        #        if link.pre == old_trans:
        #            new_link = Link(new_trans, link.post, link.weight)
        #            modified = True
        #    else:
        #        if link.post == old_trans:
        #            new_link = Link(link.pre, new_trans, link.weight)
        #            modified = True
        #    if modified:
        #        self.remove(link)
        # self.remove(old_trans)
        # self.add(new_trans)
        # if modified:
        #    self.add(new_link)
        #=======================================================================
                    
    def check_isolated(self):
        """Controllo elementi isolati"""
        # Un nodo si dice isolato se non fa parte di nessuna transizione di flusso
        isolated = []
        #aggiunta posti isolati
        isolated += [place for place in self.places 
                     if place not in [link.post for link in self.links] 
                     and place not in [link.pre for link in self.links]]
        #aggiunta transizioni isolate
        isolated += [transition for transition in self.transitions
                     if transition not in [link.post for link in self.links]
                     and transition not in [link.pre for link in self.links]]
        return isolated
    
    def remove_isolated(self):
        """Eliminazione elementi isolati"""
        isolated = self.check_isolated()
        for element in isolated:
            self.remove(element)
        return
    
    def to_matrix(self):
        """Crea e fornisce la matrice di incidenza"""
        matrix = [[0 for _ in self.__transitions] for _ in self.__places]
        for link in self.__links:
            if link.pre.__class__.__name__ == 'Place':
                matrix[self.__places.index(link.pre)][self.__transitions.index(link.post)] = -link.weight
            else:
                matrix[self.__places.index(link.post)][self.__transitions.index(link.pre)] = link.weight
        return matrix
     
    def to_dot(self, file_name, ext):
        """Crea il file .dot per la generazione dell'immagine della rete con graphviz
        e relativa immagine"""
        file_name = os.path.expanduser(file_name)
        f = open(file_name + '.dot', 'w')
        f.write('digraph g{\n') #scrittura all'interno del file, indica un grafo orientato
        f.write('\nnode [shape=circle];' ) #specifica che gli stati sono rappresentati come nodi circolari
        for place in self.places:
            f.write(place.name.replace('.','_').replace(' ','').replace('[','___').replace(']','___') + '[label = "' + place.name)
            if place.capacity != sys.maxint:
                f.write('[{0}]'.format(place.capacity))
            f.write('"]')
        f.write('\nnode [shape=box];') 
        for trans in self.transitions:
            f.write(trans.name.replace('.','_').replace(' ','').replace('[','___').replace(']','___') +'[label = "'+trans.name+'"];') #inserimento dei nomi delle transizioni
        for link in self.links:
            f.write('\n' +
                    link.pre.name.replace('.','_').replace(' ','').replace('[','___').replace(']','___') + ' -> ' + link.post.name.replace('.','_').replace(' ','').replace('[','___').replace(']','___'))
            if link.weight > 1:
                f.write('[label="{0}"]'.format(link.weight))
        f.write('}')
        f.close()
        os.system('dot -T' + ext + ' -O ' + file_name + '.dot')
        return
    
    def to_pnml(self, file_name):
        """Salva il file pnml della rete"""
        file_name = os.path.expanduser(file_name)
        ET._namespace_map['http://www.pnml.org/version-2009/grammar/pnml'] = 'pnml'
        #root = ET.Element('{http://www.pnml.org/version-2009/grammar/pnml}')
        root = ET.Element('{http://www.pnml.org/version-2009/grammar/pnml}')
        root.name = 'pnml'
        # Nodo della rete
        net = ET.SubElement(root, 'net', id = 'PetriNet.{0}'.format(self.name), type = 'http://www.pnml.org/version-2009/grammar/ptnet')
        # Nome della rete
        net_name_text = ET.SubElement(ET.SubElement(net, 'name'), 'text')
        net_name_text.text = self.name
        # Aggiunta dei posti
        for place in self.places:
            place_el = ET.SubElement(net, 'place', id = '{0}.{1}'.format(self.name, place.name))
            # Posizione del posto, tutto a 0 perché manca un algoritmo di posizionamento.
            # Sarà tutto sovrapposto
            place_pos = ET.SubElement(ET.SubElement(place_el, 'graphics'), 'position', x = '0', y = '0')
            place_mark = ET.SubElement(ET.SubElement(place_el, 'initialMarking'), 'text')
            place_mark.text = str(place.mark)
            place_mark_text = ET.SubElement(ET.SubElement(place_mark, 'graphics'), 'offset', x = '22', y = '-10')
            # Nome del posto e posizione
            # Viene usato l'attributo value invece che text perché pipe non 
            # è completamente conforme allo standard
            place_name_text = ET.SubElement(ET.SubElement(place_el, 'name'), 'text')
            place_name_text.text = place.name
            place_name_pos = ET.SubElement(ET.SubElement(ET.SubElement(place_el, 'name'), 'graphics'), 'offset', x = '22', y = '-10')
            # Capacità del posto
	    place_cap = ET.SubElement(ET.SubElement(place_el, 'capacity'), 'text')
            if place.capacity == sys.maxint:
                place_cap.text = str(0)
            else:
                place_cap.text = str(place.capacity)
                
        for trans in self.transitions:
            trans_el = ET.SubElement(net, 'transition', id = '{0}.{1}'.format(self.name, trans.name))
            # Posizione della transizione, tutto a 0 perché manca un algoritmo di posizionamento.
            # Sarà tutto sovrapposto
            trans_pos = ET.SubElement(ET.SubElement(trans_el, 'graphics'), 'position', x = '0', y = '0')
            # Nome della transizione e posizione
            trans_name_text = ET.SubElement(ET.SubElement(trans_el, 'name'), 'text')
            trans_name_text.text = trans.name
            trans_name_pos = ET.SubElement(ET.SubElement(ET.SubElement(trans_el, 'name'), 'graphics'), 'offset', x = '22', y = '-10')
        
        for link in self.links:
            link_el = ET.SubElement(net, 'arc', id = '{0}.{1} ->{2} {3}'.format(self.name, link.pre.name, link.weight, link.post.name),
                                    source = '{0}.{1}'.format(self.name, link.pre.name),
                                    target = '{0}.{1}'.format(self.name, link.post.name))
            link_weight_text = ET.SubElement(ET.SubElement(link_el, 'inscription'), 'text')
            link_weight_text.text = str(link.weight)
        ET.ElementTree(root).write(file_name)
     
    def to_pnml_pipe(self, file_name):
        """Salva il file pnml della rete [versione adattata a creare codice funzionante con il software pipe]"""
        file_name = os.path.expanduser(file_name)
        ET._namespace_map['http://www.pnml.org/version-2009/grammar/pnml'] = 'pnml'
        #root = ET.Element('{http://www.pnml.org/version-2009/grammar/pnml}')
        root = ET.Element('pnml')
        root.name = 'pnml'
        # Nodo della rete
        net = ET.SubElement(root, 'net', id = 'PetriNet.{0}'.format(self.name), type = 'http://www.pnml.org/version-2009/grammar/ptnet')
        # Nome della rete
        net_name_text = ET.SubElement(ET.SubElement(net, 'name'), 'text')
        net_name_text.text = self.name
        # Aggiunta dei posti
        for place in self.places:
            place_el = ET.SubElement(net, 'place', id = '{0}.{1}'.format(self.name, place.name))
            # Posizione del posto, tutto a 0 perché manca un algoritmo di posizionamento.
            # Sarà tutto sovrapposto
            place_pos = ET.SubElement(ET.SubElement(place_el, 'graphics'), 'position', x = '100', y = '100')
            place_mark = ET.SubElement(ET.SubElement(place_el, 'initialMarking'), 'value')
            place_mark.text = str(place.mark)
            place_mark_text = ET.SubElement(ET.SubElement(place_mark, 'graphics'), 'offset', x = '22', y = '-10')
            # Nome del posto e posizione
            # Viene usato l'attributo value invece che text perché pipe non 
            # è completamente conforme allo standard
            place_name_text = ET.SubElement(ET.SubElement(place_el, 'name'), 'value')
            place_name_text.text = place.name
            place_name_pos = ET.SubElement(ET.SubElement(ET.SubElement(place_el, 'name'), 'graphics'), 'offset', x = '22', y = '-10')
	    # Capacità del posto
	    place_cap = ET.SubElement(ET.SubElement(place_el, 'capacity'), 'value')
            if place.capacity == sys.maxint:
                place_cap.text = str(0)
            else:
                place_cap.text = str(place.capacity)
	    #place_cap_pos = ET.SubElement(ET.SubElement(ET.SubElement(place_el, 'name'), 'graphics'), 'offset', x = '22', y = '-10')
        
        for trans in self.transitions:
            trans_el = ET.SubElement(net, 'transition', id = '{0}.{1}'.format(self.name, trans.name))
            # Posizione della transizione, tutto a 0 perché manca un algoritmo di posizionamento.
            # Sarà tutto sovrapposto
            trans_pos = ET.SubElement(ET.SubElement(trans_el, 'graphics'), 'position', x = '0', y = '0')
            # Nome della transizione e posizione
            trans_name_text = ET.SubElement(ET.SubElement(trans_el, 'name'), 'value')
            trans_name_text.text = trans.name
            trans_name_pos = ET.SubElement(ET.SubElement(ET.SubElement(trans_el, 'name'), 'graphics'), 'offset', x = '22', y = '-10')
        
        for link in self.links:
            link_el = ET.SubElement(net, 'arc', id = '{0}.{1} ->{2} {3}'.format(self.name, link.pre.name, link.weight, link.post.name),
                                    source = '{0}.{1}'.format(self.name, link.pre.name),
                                    target = '{0}.{1}'.format(self.name, link.post.name))
            link_weight_text = ET.SubElement(ET.SubElement(link_el, 'inscription'), 'value')
            link_weight_text.text = str(link.weight)
        ET.ElementTree(root).write(file_name)

        
    def is_occurrency(self):
        """Verifica che la rete sia una rete di occorrenze"""
        # Affinchè una rete sia di occorrenza devono valere le seguenti proprietà:
        # ·Gli stati hanno massimo una precondizione e una postcondizione
        # ·Non esistono cicli
        matrix = self.to_matrix()
        # 
        for line in matrix:
            pre_found = False
            post_found = False
            for weight in line:
                if weight > 0:
                    if not pre_found:
                        pre_found = True
                    else:
                        return False
                elif weight < 0:
                    if not post_found:
                        post_found = True
                    else:
                        return False
        # Controllo mancanza di cicli
        test_net = copy.deepcopy(self)
        test_net.remove_isolated()
        post_links = []
        while post_links == [] and len(test_net.places) > 0:
            initial_place = test_net.places[0]
            post_links = [link for link in test_net.links if link.pre == initial_place]
            if len(post_links) == 0:
                test_net.remove(initial_place)
        if len(test_net.places) == 0:
            return True 
        else:
            first_link = post_links[0]
            return self.deep_search(test_net, initial_place, [], first_link)
    
    def get_post_places(self, test_net, transition):
        """Funzione di supporto a is_occurrency"""
        links = [link for link in test_net.links if link.pre == transition]
        p = [place for place in [link.post for link in links]]
        return p
        
    def deep_search(self, test_net, current_element, old_place, actual_link):
        """Funzione di supporto a is_occurrency"""
        if current_element.__class__.__name__ == 'Place':
            if current_element in old_place:
                return False
            else:
                old_place.append(current_element)
                outgoing_link = [link for link in test_net.links if link.pre == current_element]
                for link in outgoing_link:
                    next_places = self.get_post_places(test_net, link.post) # Che sarà sicuramente una Transizione
                    for new_place in next_places:
                        return self.deep_search(test_net, new_place, old_place, link)
        return True 
    
    def check_balance(self):
        """Controlla che i pesi degli archi siano compatibili con le capacità dei posti"""
        for link in self.__links:
            if link.pre.__class__.__name__ == 'Place': # Cerco il posto del link
                actual_place = link.pre
            else:
                actual_place = link.post
            if actual_place.capacity < link.weight: # Capacità non compatibile con il peso del link
                return False
        return True

    def union(self, other, places = [], transitions = []):
        """Effettua l'unione tra la rete su cui viene chiamato e la rete other. 
        Places e transitions sono tuple contenenti posti e transizioni che verranno uniti. 
        In caso di conflitti i nomi resteranno quelli della rete self."""
        nnet = PetriNet('{0}_union_{1}'.format(self.name, other.name)) # Creo una copia della rete attuale
        # Creo due copie per non modificare le reti originali
        net_one = eval(repr(self))
        net_two = eval(repr(other))
        for place in places:
            if place in net_one.places and place in net_two.places:
                nnet.add(place)
            else:
                raise Exception('{0} not in {1} or {2}'.format(place.name, net_one.name, net_two.name))
        for transition in transitions:
            if transition in net_one.transitions and transition in net_two.transitions:
                nnet.add(transition)
            else:
                raise Exception('{0} not in {1} or {2}'.format(transition.name, net_one.name, net_two.name))  
        # Modifica nomi dei posti in net1
        place_to_remove_n1 = []
        place_to_add_n1 = []
        for place in net_one.places:
            if place in net_one.places and not place in places:
                new_place = eval(repr(place))
                while new_place in net_two.places:
                    # Creo un nuovo nome univoco all'interno di net_one per new_places
                    new_place.name = '{0}_{1}'.format(net_one.name, new_place.name)
                if not (place == new_place):
                    place_to_add_n1.append([place,new_place])
                    # Schedulo la rimozione dell'ormai inutile
                    # posto place
                    place_to_remove_n1.append(place)
                
        for [place,new_place] in place_to_add_n1:
            net_one.duplicate_place(place,new_place)
            

        # Modifica dei posti in net2
        place_to_remove_n2 = []
        place_to_add_n2 = []        
        for place in net_two.places:
            if place in net_two.places and not place in places:
                new_place = eval(repr(place))       
                while new_place in net_one.places:
                    new_place.name = '{0}_{1}'.format(net_two.name, new_place.name)
                if not place == new_place:
                    place_to_add_n2.append([place,new_place])
                
                    # Schedulo la rimozione dell'ormai inutile
                    # posto place
                    place_to_remove_n2.append(place)
        for [place,new_place] in place_to_add_n2:        
            net_two.duplicate_place(place, new_place)     
        #Modifica transizioni in net1
        trans_to_remove_n1 = []
        trans_to_add_n1 = []
        for transition in net_one.transitions:
            if transition in net_one.transitions and not transition in transitions:
                # Transizione presente sia in net_one che in net_two ma sulla quale non si deve
                # unire la rete
                new_transition = eval(repr(transition))
                while new_transition in net_two.transitions:
                    # Creo un nuovo nome univoco all'interno di net_one per new_transitions
                    new_transition.name = '{0}_{1}'.format(net_one.name, new_transition.name)
                if not transition == new_transition:
                    trans_to_add_n1.append([transition, new_transition])
                
                    # Schedulo la rimozione di transition
                    trans_to_remove_n1.append(transition)
                
        for [transition, new_transition] in trans_to_add_n1:
            net_one.duplicate_transition(transition, new_transition)
            
        trans_to_remove_n2 = []
        trans_to_add_n2 = []
        for transition in net_two.transitions:
            if transition in net_two.transitions and not transition in transitions:        
                new_transition = eval(repr(transition))
                while new_transition in net_one.transitions:
                    # Creo un nuovo nome univoco all'interno di net_one per new_transitions
                    new_transition.name = '{0}_{1}'.format(net_two.name, new_transition.name)
                if not transition == new_transition:
                    trans_to_add_n2.append([transition, new_transition])
                    trans_to_remove_n2.append(transition)
        
        for [transition, new_transition] in trans_to_add_n2:
            net_two.duplicate_transition(transition, new_transition)     
        # Rimozione link relativi a posti e transizioni da eliminare 
        # della rete net_one
        link_to_remove_net_one = []
        for link in net_one.links:
            if link.pre.__class__.__name__ == 'Place':
                if link.pre in place_to_remove_n1 or link.post in trans_to_remove_n1:
                    link_to_remove_net_one.append(link)
            else:
                if link.pre in trans_to_remove_n1 or link.post in place_to_remove_n1:
                    link_to_remove_net_one.append(link)
        for link in link_to_remove_net_one:
            net_one.remove(link)
        # Rimozione link relativi a posti e transizioni da eliminare 
        # della rete net_two
        link_to_remove_net_two = []
        for link in net_two.links:
            if link.pre.__class__.__name__ == 'Place':
                if link.pre in place_to_remove_n2 or link.post in trans_to_remove_n2:
                    link_to_remove_net_two.append(link)
            else:
                if link.pre in trans_to_remove_n2 or link.post in place_to_remove_n2:
                    link_to_remove_net_two.append(link)
        for link in link_to_remove_net_two:
            net_two.remove(link)
        # Rimozione posti duplicati
        for place in place_to_remove_n1:
            net_one.remove(place)
        for place in place_to_remove_n2:
            net_two.remove(place)
        # Rimozione transizioni duplicate
        for transition in trans_to_remove_n1:
            net_one.remove(transition)
        for transition in trans_to_remove_n2:
            net_two.remove(transition)                        
        # Aggiunta posti di net_one
        for place in net_one.places:
            # Ora si può essere sicuri che i posti sono univoci, quindi
            # è possibile inserirli immediatamente nella rete unione se non già presenti
            if place not in nnet.places:
                nnet.add(place)
        # Aggiunta transizioni di net_one
        for transition in net_one.transitions:
            # Ora si può essere sicuri che le transizioni sono univoche, quindi
            # è possibile inserirle immediatamente nella rete unione
            if transition not in nnet.transitions:
                nnet.add(transition)
        # Aggiunta link di net_one
        for link in net_one.links:
            # A questo punto non ci sono posti e transizioni *equivalenti* tra le due reti 
            # e di conseguenza si può aggiungere il link direttamente non essendoci problemi
            nnet.add(link)
        # Aggiunta posti di net_two
        for place in net_two.places:
            # A questo punto i posti con nomi in conflitto tra net_two e net_one
            # dovrebbero essere già stati sistemati, di conseguenza è possibile
            # inserire ogni posto non ancora presente in nnet
            if place not in nnet.places:
                nnet.add(place)
        # Aggiunta transizioni di net_two
        for transition in net_two.transitions:
            # Equivalentemente a quanto detto prima
            if transition not in nnet.transitions:
                nnet.add(transition)
        # Aggiunta link di net_two
        for link in net_two.links:
            if link not in nnet.links:
                nnet.add(link)
        return nnet
    
    def set_mark(self, place_name, mark):
        assert mark >=0, 'Mark must be non-negative'
        assert PetriNetElement(place_name) in self.__places, '{0] not in {1}'.format(place_name, self.__name)
        assert self.__places[self.__places.index(PetriNetElement(place_name))].capacity >= mark, 'Capacity must be greater or equal to mark'
        self.__places[self.__places.index(PetriNetElement(place_name))].mark = mark
