# -*- coding: utf-8 -*-
import ply.yacc as yacc
import PetriNet
import sys

precedence = (('left', 'ON'), ('left',  'SEMI'))
#variabili globali
actualNet = None #rete attuale, è la rete che si sta considerando per non dover aggiungere in tutti i comandi rete.comando
#inizialmente è l'ultima rete creata, ma si può modificare con il comando workOn(nomeRete);
UnionA = None #variabili di appoggio per l'unione 
UnionB= None #variabili di appoggio per l'unione 
net = {} #dizionario dei nomi delle reti create con associato l'oggetto rete definito sotto
var = {} #dizionario delle variabili


class rete:
    net = None
    place = {} #dizionario dei nomi dei posti
    transition = {} #dizionario dei nomi delle transizioni
    mark= {} #dizionario delle marcature
    objMark = [] #lista degli oggetti che rappresentano le marcature

    def __init__(self,  rete):
        self.net=rete
        self.place= dict()
        self.transition = dict()
        self.mark = dict()
        self.objMark= list()

#regole per il parsing

#creazione di una nuova rete
#PetriNet g;
def p_new_net(p):
    '''expression : PETRINET listaReti SEMI'''
    print 'parser: new_net'

#creazione di una nuova rete tramite una lista di nomi
#PetriNet a,b,c;
def p_listaReti(p):
    '''listaReti : ID ',' listaReti
                    | ID'''
    global actualNet
    print 'parser: listaReti'
    com= rete(PetriNet.PetriNet())
    net[p[1]] = com
    actualNet = p[1] #la rete attuale è sempre l'ultima definita
    print 'parser: rete attuale: ' + p[1]

#creazione di uno o più nuovi stati
def p_new_place(p):
    '''expression : PLACE ON ID setActualNet listaPosti  SEMI
                            | PLACE listaPosti SEMI'''
    print 'parser: new_place'

def p_setActualNet(p):
    '''setActualNet : '''
    global actualNet
    if p[-1] in net:
        actualNet= p[-1]
        print 'parser: rete attuale:' + actualNet
    else: print 'parser: la rete' + p[-1] +'non esiste'
    
#creazione di uno o più stati tramite una lista
#derivante da p_new_place
#Place posto; oppure
#Place posto1, posto2, ...;
def p_listaPosti(p):
    '''listaPosti : ID ',' listaPosti
                | ID'''
    global actualNet
    print 'parser: listaPosti'
    net[actualNet].place[p[1]] = net[actualNet].net.addState(p[1], False)
    
#creazione di una o più nuove transizioni
def p_new_transition(p):
    '''expression : TRANSITION ON ID setActualNet listaTrans SEMI
                            | TRANSITION listaTrans SEMI'''
    print 'parser: new_transition'
    
#creazione di uno o più stati tramite una lista
#Tansition t; oppure
#Transition t1, t2, ...;
def p_listaTrans(p):
    '''listaTrans : ID ',' listaTrans
                        | ID'''
    global actualNet
    print 'parser: listaTrans'
    net[actualNet].transition[p[1]] = net[actualNet].net.addTrans(p[1])

#cambiare la rete che si sta considerando durante la definizione del file
def p_workOn(p):
    '''expression : WORKON LPAREN ID RPAREN SEMI
    '''
    global actualNet
    if p[3] in net:
        actualNet= p[3]
        print 'parser: rete attuale:' + actualNet
    else: print 'parser: la rete' + p[3] +'non esiste'
    
def p_link(p):
    '''expression : listaLink
    '''
    print 'parser: link'
    
#regola per la lista dei di link nella forma ID -> ID -> ...;
def p_listaLink(p):
    '''listaLink : ID LINK listaLink
                    | ID SEMI'''
    
    print 'parser: listaLink'
    if p[2]==';':
        p[0]=p[1]
    else:
        if p[1] in net[actualNet].place: #controllo se il primo ID è uno stato
        #se il primo ID è uno stato allora necessariamente quello successivo sarà una transizione
            if p[3] in net[actualNet].transition: 
                net[actualNet].net.addPre(net[actualNet].place[p[1]].index,  net[actualNet].transition[p[3]].index)
        elif p[1] in net[actualNet].transition: #altrimenti il primo ID è una transizione e quello successivo uno stato
            if p[3] in net[actualNet].place:
                net[actualNet].net.addPost(net[actualNet].place[p[3]].index,  net[actualNet].transition[p[1]].index)
        else: #nel caso i nomi non esistano o si sta creando un link tra due tipi uguali allora si segnala l'errore e il link non viene creato
            print "SYNTAX ERROR: errore durante la definizione del link"
        p[0]=p[1]
        
#regola per la creazione della marcatura iniziale
#M0 = {a,b,c..};
#M0 = mark;
#rete.M0 = {a,b,c..};
#rete.M0 = mark;
def p_M0(p):
    """expression : M0 '=' Hmark SEMI
                            | M0 '=' ID SEMI
                            | ID '.' M0 '=' Hmark SEMI
                            | ID '.' M0 '=' ID SEMI"""
    print "parser : M0"
    global actualNet
    #imposta la marcatura iniziale della rete
    if p[1]=='M0':
        if isinstance(p[3], set):
            #richiamo la funzione per la creazione dello speciale array per M0
            net[actualNet].net.setM0(creaM0(actualNet, p[3]))
            #imposto M0 nel dizionario 
            net[actualNet].mark['M0']=p[3]
        else:
            net[actualNet].net.setM0(creaM0(actualNet, net[actualNet].mark[p[3]]))
            net[actualNet].mark['M0']=mark[p[3]]
    else: #caso ri rete.M0
        if p[1] in net:
            if isinstance(p[5], set):
                net[p[1]].net.setM0(creaM0(p[1], p[5]))
                net[p[1]].mark['M0']=p[5]
            else:
                net[p[1]].net.setM0(creaM0(p[1], net[p[1]].mark[p[5]]))
                net[p[1]].mark['M0']=mark[p[5]]
        else: #nel caso che la rete in rete.M0 non esista
            print "SYNTAX ERROR: La rete "+ p[1] + " non esiste"

def creaM0(rete, marca): #creazione della lista per la marcatura iniziale
    com= list(0 for i in net[rete].net.P) 
    #la lista per la marcatura iniziale è composta da 0 e 1, 
    #0 quando lo stato associato in P non è marcato
    #1 quando lo stato associato in P è marcato
    for i, item in enumerate(net[rete].net.P):
        for m in marca:
            if item.nome==m:
                com[i]=1
                break
    return com[:]
    
#nuova marcatura con nome associato (m={a,b,c...};)
def p_new_mark(p):
    '''expression : ID '=' markList SEMI'''
    print 'parser: new_mark'
    
    if net[actualNet].mark.has_key(p[1]):
        net[actualNet].mark[p[1]].clear() #sovrascrivo nel caso in cui il nome esista già
    net[actualNet].mark[p[1]]=p[3].copy()

#creazione di una nuova marcatura
#restituisce una lista in p[0]
def p_mark(p):
    '''markList : LBRACE ID ','  markList
                    | ID ',' markList
                    | LBRACE ID RBRACE
                    | ID RBRACE
    '''
    print 'parser: mark'
    
    if p[2]=='}': # ID RBRACE
        net[actualNet].objMark.append(set())
        p[0]=net[actualNet].objMark[len(net[actualNet].objMark)-1]
        p[0].add(p[1])
    elif p[3]=='}': #LBRACE ID RBRACE
        net[actualNet].objMark.append(set())
        p[0]=net[actualNet].objMark[len(net[actualNet].objMark)-1]
        p[0].add(p[2])
        #| ID ',' markList
    elif net[actualNet].place.has_key(p[1]): #controllo che siano tutti posti e non transizioni
        p[3].add(p[1])
        p[0]=p[3]
            #LBRACE ID ','  markList
    elif net[actualNet].place.has_key(p[2]): #controllo che siano tutti posti e non transizioni
        p[4].add(p[2])
        p[0]=p[4]
    
#scatto con marche senza nome
#{place1,place2,..} [transition> {placem,placen,..};
def p_Hscatto(p):
    '''expression : Hmark LSQBRACE ID '>'  Hmark SEMI'''
    #scatto con marche anonime ({a,b,..}[t> {c,d,..};)
    print 'parser: HScatto'
    
    global actualNet
    for i in p[1]:
        #aggiunta delle precondizioni ritornate come lista in p[1]
        net[actualNet].net.addPre(net[actualNet].place[i].index,  net[actualNet].transition[p[3]].index)
    for i in p[5]:
        #aggiunta delle postcondizioni ritornate come lista in p[5]
        net[actualNet].net.addPost(net[actualNet].place[i].index,  net[actualNet].transition[p[3]].index)

#definizione di una marca che non viene inizializzata con un nome
def p_new_Hmark(p):
    'Hmark : markList'
    print 'parser: new_Hmark'
    p[0]= p[1].copy()
    
#scatto di una transizione attraverso nomi di marche
#mark1 [transition> mark2;
def p_scatto(p):
    '''expression : ID LSQBRACE ID '>' ID SEMI'''
    global actualNet
    print 'parser: scatto'

    for i in mark[p[5]]:
         #aggiunta delle postcondizioni ritornate come lista in p[5]
        net[actualNet].net.addPost(net[actualNet].place[i].index,  net[actualNet].transition[p[3]].index)
        
    for i in mark[p[1]]:
         #aggiunta delle precondizioni ritornate come lista in p[1]
        net[actualNet].net.addPre(net[actualNet].place[i].index,  net[actualNet].transition[p[3]].index)

 
#g = union(a,b) on [a=b, b=c, c=d];
#unione complessa, dopo le parentesi quadre il priimo termine si riferisce alla rete a e il secondo alla rete b
def p_ComplexUnion(p):
    '''expression : ID '=' UNION LPAREN ID ',' ID RPAREN  continue ON listUnion SEMI'''
    global UnionA,  UnionB
    print 'parser:union'
    print p[11]
    
    #p[11] è una lista di liste p[11][0] è la lista delle associazioni tra condizioni
    #p[11][1] è la lista delle associazioni tra transizioni
    com = net[UnionA].net.union(net[UnionB].net, p[11][0], p[11][1])
    net[p[1]]= rete(com)
    UnionA = None
    UnionB = None

#salvataggio dei nomi delle reti che prendono parte al'unione
#richiamato da ComplexUnion
#listUnon altrimenti non funziona
def p_continue(p):
    '''continue : '''
    global UnionA,  UnionB
    UnionA = p[-4] #recupera i valori dei token precedenti la chiamata
    UnionB = p[-2]

#unione semplice tra due reti senza uguaglianze tra stati o transizioni
#reteNew= union (reteA,reteB);
def p_SimpleUnion(p): 
    '''expression : ID '=' UNION LPAREN ID ',' ID RPAREN SEMI'''
    print 'parser: SimpleUnion'
    com = net[p[5]].net.union(net[p[7]].net, [], [])
    net[p[1]] = rete(com)
    
#creazione della lista di unificazione per l'unione complessa [a=b,c=d]
#restituisce una lista [[],[]] (a ComplexUnion) con al posto dei nomi gli indici degli stati
#divide la lista in due sottoliste una per i posti e una per le transizioni
def p_listUnion(p):
    '''listUnion : LSQBRACE ID '=' ID listUnion
                    | ',' ID '=' ID listUnion
                    | RSQBRACE'''
                    
    print 'parser: listUnion'
    
    if p[1] == ']':
        com=[ [] for i in range(2)] 
        #creazione di una lista di appoggio nella forma [[],[]]
        #la prima sottolista è per i posti
        #la seconda sottolista è per le transizioni
        #questa lista verrà trasmessa tramite il parametro p[0] durante il matching della regola
        #alla funzione p_complexUnion
        p[0]=com
    elif p[1]== '[': #inizio della lista
        if p[2] in net[UnionA].place and p[4] in net[UnionB].place: #controllo che siano entrambi stati altrimenti salto
            print p[5]
            lcom=list()
            lcom.append(net[UnionA].place[p[2]].index) 
            lcom.append(net[UnionB].place[p[4]].index)
            p[5][0].append(lcom)
        elif p[2] in net[UnionA].transition and p[4] in net[UnionB].transition: #controllo che siano entrambe transizioni altrimenti salto
            lcom=list()
            lcom.append(net[UnionA].transition[p[2]].index)
            lcom.append(net[UnionB].transition[p[4]].index)
            p[5][1].append(lcom)
        else:
            print 'Sintax Error : '+p[2]+' e '+p[4]+' non associabili'
        p[0]=p[5]
        print p[0]
    else: #',' ID '=' ID listUnion
        if p[2] in net[UnionA].place and p[4] in net[UnionB].place: #controllo che siano entrambi stati altrimenti salto
            lcom=list()
            lcom.append(net[UnionA].place[p[2]].index)
            lcom.append(net[UnionB].place[p[4]].index)
            p[5][0].append(lcom)
        elif p[2] in net[UnionA].transition and p[4] in net[UnionB].transition: #controllo che siano entrambe transizioni altrimenti salto
            lcom=list()
            lcom.append(net[UnionA].transition[p[2]].index)
            lcom.append(net[UnionB].transition[p[4]].index)
            p[5][1].append(lcom)
        else:
            print 'Sintax Error : '+p[2]+' e '+p[4]+' non associabili'
        p[0]=p[5]
    
#creazione del file .dot e relativa immagine .estensione
#rete.toDot(nomeFile,estensione);
def p_toDot(p):
    '''expression : ID '.' TODOT LPAREN ID ',' ID RPAREN SEMI
                        | TODOT LPAREN ID ',' ID RPAREN SEMI'''
    global net,  actualNet
    print 'parser: toDot'
    if p[1]=='toDot': #toDot della rete attuale
        net[actualNet].net.toDot(p[3], p[5])
    else:
        if p[1] in net: #toDot della rete specificata
            net[p[1]].net.toDot(p[5], p[7])
        else: 
            print "SYNTAX ERROR: la rete "+p[1]+" non esiste "
    

#verifica che la rete sia di occorrenza
#rete.isOccurrency()
def p_isOccurrency(p):
    '''expression : ID '.' ISOCCURRENCY LPAREN RPAREN SEMI'''
    global net
    print 'parser: isOccurrency'
    net[p[1]].net.isOccurrency()

#creazione e visualizzazione della matrice di incidenza della rete
#rete.matrix;
def p_matrix(p):
    '''expression : ID '.' MATRIX SEMI'''
    global net
    print 'parser: matrix'
    if net[p[1]].net.matrice==[]:
        net[p[1]].net.toMatrix()
    else:
        for t in range(len(net[p[1]].net.T)+1):
            if t==0:
                print "        ", 
            else:
                print net[p[1]].net.idNome(net[p[1]].net.matrice[0][t]), " ",  
        for s in range(1, len(net[p[1]].net.P)+1):  #stampo la matrice di incidenza 
            for i in range(len(net[p[1]].net.T)+1):
                if i==0:
                    print ""
                    print net[p[1]].net.idNome(net[p[1]].net.matrice[s][i])+ " ", 
                else:
                    print str(net[p[1]].net.matrice[s][i])+" ", 
    print ""
    

#creazione del grafo dei casi della rete (ritorna la lista che rappresenta il grafo)
#g=rete.createCaseGraph(mark);
#g=rete.createCaseGraph(M0);
#g=rete.createCaseGraph({a,b,c});
def p_graph(p):
    '''expression : ID '=' ID '.' GRAPH LPAREN ID RPAREN SEMI
                            | ID '=' ID '.' GRAPH LPAREN M0 RPAREN SEMI
                            | ID '=' ID '.' GRAPH LPAREN Hmark RPAREN SEMI'''
    global net
    print 'parser: graph'
    com=list()
    if isinstance(p[7], set): #caso Hmark
        for i in p[7]:
            com.append(net[p[3]].place[i].index)
        
    elif p[7]=='M0': #caso M0
        print net[p[3]].mark.keys()
        for i in net[p[3]].mark['M0']:
            com.append(net[p[3]].place[i].index)
            
    elif p[7] in net[p[3]].mark: #caso marcatura esistente
        for i in net[p[3]].mark[p[7]]:
            com.append(net[p[3]].place[i].index)
    else: 
        print "SYNTAX ERROR: la marca"+p[7]+"non esiste"
    print com
    var[p[1]]=PetriNet.createCaseGraph(net[p[3]].net, com)
    
# convertire il grafo dei casi in dot e creazione del file immagine
#rete.CGtoDot(g,nomeFileImmagine,estensione); DOVE g è l'oggetto restituito da createCaseGraph
def p_graphToDot(p):        
    '''expression : ID '.' GRAPHDOT LPAREN ID ',' ID ',' ID RPAREN SEMI'''
    PetriNet.CGToDot(net[p[1]].net, var[p[5]][0],  p[7],  p[9])
    
#nel caso non si abbia nessun matching con le regole precedenti si individua un syntax error
def p_error(p):
    print "SYNTAX ERROR in input: ",  p

#necessario: import dei token 
from PetriNet_lex import tokens

#utilizza il modulo sys per importare l'argomento passato da shell
#se richiamo petriNet_parser.py -f nomeFile (che deve essere un file di testo)
#preleva le istruzioni di specifica dal file
#altrimenti le preleva da shell tramite la riga di comando
data= None
if len(sys.argv)>1:
    if sys.argv[1] == "-f":  
        try: 
            data=open(sys.argv[2], 'r') #apertura del file in lettura
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
