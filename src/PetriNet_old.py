# -*- coding: utf-8 -*-
import sys
import os
#verificare che l'utente non inserisca stati o transizioni con nome  uguale!!!!!!!!!!!

class Obj:
    """un oggetto rappresenta sia uno stato che una transizione"""
    index=-1       #indice globale dell'oggetto, univoco per stati e transizioni
    nome='null'    #nome dell'oggetto
    
    def __init__(self, indice, nome):
        self.index=indice
        self.nome=nome

class State(Obj):
    """classe che rappresenta lo stato di una rete di Petri"""
    token=0   #marcatura dello stato [togliere???]

    def __init__(self, indiceGlobale,nome, token):
        self.index=indiceGlobale
        self.nome=nome
        self.token=token
        
    def __repr__(self):
        return self.nome+"("+str(self.index)+")"

class Trans(Obj):
    """classe che rappresenta una transizione di una rete di Petri"""
    
    def __init__(self, indiceGlobale, nome):
        self.index=indiceGlobale
        self.nome=nome
        
    def __repr__(self):
        return self.nome+"("+str(self.index)+")"

class Link:
    """classe che rappresenta una relazione tra stato e transizione"""
    state=0 #oggetto stato
    trans=0 #oggetto transizione
    pre=True #se True allora identifica una precondizione (stato -> transizione) altrimenti una postcondizione
    
    def __init__(self,stato,transizione,pre):
        self.state=stato
        self.trans=transizione
        self.pre=pre
        
    def __str__(self):
        stringa= ""
        if self.pre==True:
            stringa=self.state.nome +  " -> " +  self.trans.nome
        else:
            stringa=self.trans.nome + " -> "+  self.state.nome
        return stringa
        
    def __repr__(self):
        stringa= ""
        if self.pre==True:
            stringa=self.state.nome +  " -> "+ self.trans.nome
        else:
            stringa=self.trans.nome + " -> " + self.state.nome
        return stringa

class PetriNet:
    P=list()  #lista degli stati della rete
    T=list()  #lista delle transizioni della rete
    F=list()  #lista dei link della rete (relazione di flusso)
    M0=list() #marcatura iniziale della rete indici globali [non ancora utilizzata]
    matrice=list() #matrice di incidenza della rete, generata con toMatrix()
    MaxIndice=0 #Massimo id utile per l'impostazione dell'id globale
    dictN = dict() #dizionario degli indici globali associati al nome
    nome=""
    fileDot=""
    graphDot=""
    
    def __init__(self):
        self.P=list()  
        self.T=list()  
        self.F=list() 
        self.M0=list() 
        self.matrice=list()
        self.dictN= dict()
        self.MaxIndice=0
        self.nome=""
        self.fileDot=""
        self.graphDot=""

    def addState(self,nome,mark):
        """aggiunta di uno stato alla rete"""
        #controllo che il nome non sia già esistente
        cont=0
        for i in self.P:
            if i.nome==nome:
                cont=cont+1
        if cont ==0:
            stato=State(self.MaxIndice,nome,mark) #creazione di un nuovo stato con indice globale, nome, marcatura
        else:
            stato=State(self.MaxIndice,nome+'_'+str(cont),mark) #creazione di un nuovo stato con indice globale, nome, marcatura con nome cambiato
            print 'PetriNet: attenzione nome cambiato in s'+ stato.nome
        self.P.append(stato)                              #inserimento dello stato nella lista della rete
        print 'PetriNet: aggiunto lo stato: '+nome
        self.MaxIndice=self.MaxIndice+1
        self.dictN[stato.index]= stato.nome
        return stato
        
    def removeState(self, index):
        """"rimozione di uno stato"""
        com=0
        for p in self.P:
            if p.index == index:
                print "rimozione stato",  p
                self.P.pop(com)
                self.dictN.pop(index)
                break
                
            com=com+1

  
    def addTrans(self,nome):
        """aggiunta di una transizione alla rete"""
        cont=0
        for i in self.T:
            if i.nome==nome:
                cont=cont+1
        if cont ==0:
            transizione=Trans(self.MaxIndice,nome) #creazione di una nuova transizione con indice globale, nome
        else:
            transizione=Trans(self.MaxIndice,nome+'_'+str(cont)) #creazione di una nuova transizione con indice globale, nome
            print 'PetriNet: attenzione nome cambiato in s'+ transizione.nome
        
        self.T.append(transizione)                         #inserimento della transizione nella lista della rete
        print 'PetriNet: aggiunto la transizione: '+nome
        self.MaxIndice=self.MaxIndice+1
        self.dictN[transizione.index]= transizione.nome
        return transizione
    
    def removeTrans(self, index):
        """"rimozione di uno stato"""
        com=0
        for t in self.T:
            if t.index == index:
                print "rimozione transizione", t
                self.T.pop(com)
                self.dictN.pop(index)
                break
            com=com+1
        
    #funzione che rimuove i nodi isolati
    def check(self):
        """rimozione dei nodi non connessi"""
        
        com=list(False for i in range(self.MaxIndice))
        
        for l in self.F: #se uno stato o transizione compaiono nella relazione di flusso F allora non sono isolati
            if com[l.state.index]== False:
                com[l.state.index]= True
            if com[l.trans.index]== False:
                com[l.trans.index]=True
        
        while True:
            try:
                id=com.index(False)
            except ValueError:
                print "check dei nodi isolati eseguito con successo!"
                break
            else:
                #richiamo la funzione idState che restituisce -1 se l'id non appartiene ad uno stato
                #in modo da controllare velocemente se l'id è stato o transizione
                stato=self.idState(id)
                
                if stato<0:
                    #rimuovo la transizione
                    self.removeTrans(id)
                else:
                    self.removeState(id)
                    #rimuovere lo stato
            com[id]=True
    
    #funzione che controlla i nodi isolati
    #restituisce un array boleano per la funzione toDot di lunghezza MaxIndice
    def mmcheck(self):
        """controllo dei nodi non connessi"""
        
        com=list(False for i in range(self.MaxIndice))
        
        for l in self.F: #se uno stato o transizione compaiono nella relazione di flusso F allora non sono isolati
            if com[l.state.index]== False:
                com[l.state.index]= True
            if com[l.trans.index]== False:
                com[l.trans.index]=True
        
        return com

#idState e idTrans sono gli indici globali
    def addLink(self,idState, idTrans, pre):
        """Aggiunta di un collegamento tra stato e transizione."""
        stato=-1
        transizione=-1
        for s in self.P:  #dati gli id locali di stato e transizione ricerco gli oggetti corrispondenti
            if s.index==idState:
                stato=s
                break
        else:
            print "stato non trovato"
            return None
        for t in self.T:
            if t.index==idTrans:
                transizione=t
                break
        else:
            print "transizione non trovata"
            return None

        if stato.index>=0 and transizione.index>=0:  #se stato e transizione esistono allora hanno un indice maggiore di zero
            freccia=Link(stato,transizione,pre)      #creazione di un nuovo collegamento tra stato e transizione
            self.F.append(freccia)
            print('aggiunto link'+stato.nome+' -> '+transizione.nome+'\n')
            return True
        else:
            print('NON aggiunto link\n')            #se lo stato o la transizione o  entrambi non esistono allora il collegamento non viene creato
            print stato
            print transizione
            return False

    def addPre(self,idStato, idTrans):
        """aggiunta di una precondizione"""
        return self.addLink(idStato,idTrans,True)

    def addPost(self,idStato,idTrans):
        """aggiunta di una postcondizione"""
        return self.addLink(idStato,idTrans,False)

    def idState(self,nomeStato):
        """funzione che restituisce l'indice dello stato di nome o indice nomeStato nella lista P della rete, se non esiste restituisce -1"""
        ret=-1
        if isinstance(nomeStato, int):
            for stato in self.P:
                if stato.index==nomeStato:
                    ret=stato.index
        else:
            for stato in self.P:
                if stato.nome==nomeStato:
                    ret=stato.index
        return ret
    
    def idNome(self, id):
        if self.idState(id)>=0:
            for s in self.P:
                if s.index==id:
                    return s.nome
        elif self.idTrans(id)>=0:
            for s in self.T:
                if s.index==id:
                    return s.nome
        else:
            print 'indice non esistente'
            return False

    def idTrans(self,nomeTrans):
        """funzione che restituisce l'indice della transizione di nome nomeTrans nella lista T della rete, se non esiste restituisce -1"""
        ret=-1
        if isinstance(nomeTrans, int):
            for trans in self.T:
                if trans.index==nomeTrans:
                    ret=trans.index
        else:
            for trans in self.T:
                if trans.nome==nomeTrans:
                    ret=trans.index
        return ret
    
    def setM0(self, lista):
        """funzione che imposta la marcatura iniziale della rete"""
        self.M0= list(0 for i in self.P)
        for i, m in enumerate(lista):
            self.M0[i]=m
     
        
        #place e trans sono due matrici a due colonne che definiscono gli stati da unificare
        #nella prima colonna c'è l'id globale relativo al posto/transizione della prima rete rispettivamente nella seconda
    def union(self, B,  place,  trans):
        """funzione che esegue l'unione tra due reti e restituisce una nuova rete"""
        new=PetriNet() #creazione della nuova rete, unione tra le due
        new.P=self.P[:]  #inizialmente la rete sarà equivalente a self
        new.T=self.T[:]
        new.F=self.F[:] 
        new.MaxIndice=self.MaxIndice
        new.dictN=self.dictN.copy() #dizionario degli indici globali associati al nome
        link=B.F[:] #copia della relazione di flusso della seconda rete
        merge=dict() #dizionario indice globale iniziale, indice globale finale (dei nodi della seconda rete)
        
        for p in B.P: #per ogni stato della seconda rete
            unifica=False
            indice=-1
            for lista in place:
                if lista[1]==p.index:
                    unifica= True
                    indice=lista[0]
            #se il nodo non deve unificarsi nella rete allora lo aggiungo, altrimenti no
            if unifica==False:
                com=new.addState(str(p.nome), bool(p.token)) #creo lo stato nella nuova rete
                merge[p.index]=int(com.index) #aggiungo nel dizionario gli id
            else:
                merge[p.index]=int(indice) #l'indice coincide con l'indice del nodo della prima rete
        
        for t in B.T: #per ogni transizione
            unifica=False
            indice=-1
            for lista in trans:
                if lista[1]==t.index:
                    unifica=True
                    indice=lista[0]
            #se il nodo non deve unificarsi nella rete allora lo aggiungo, altrimenti no        
            if unifica==False:
                com=new.addTrans(str(t.nome))
                merge[t.index]=int(com.index)
            else:
                merge[t.index]=int(indice)
        
        for l in link:
            newIdStato= merge[l.state.index] #recupero i nuovi id di stato e transizione dei link della seconda rete
            newIdTrans= merge[l.trans.index]
            #per tutte le coppie di posti della lista di equivalenza
            for p in place:
                if p[1]== l.state.index: #controllo se lo stato deve essere associato ad un altro
                    newIdStato= p[0]
                    break
            for t in trans:
                if t[1]==l.trans.index:
                    newIdTrans=t[0]
                    break
            #print 'addlink' ,  newIdStato,  newIdTrans
            new.addLink(int(newIdStato),int(newIdTrans), bool(l.pre))
            
        return new
    
    def toMatrix(self):
        """crea la matrice di incidenza della rete"""
        riga=list(list() for x in self.P) #creo la matrice vuota che servirà più avanti
        riga.append(list())
        diz=dict()
        
        print riga
        for s in range(len(self.P)+1):
            for t in range(len(self.T)+1):
                riga[s].append(0)       #inizializzo la matrice creata
        
        s=1
        for p in self.P:
            riga[s][0]=p.index
            diz[p.index]=s
            s=s+1
        s=1
        for t in self.T:
            riga[0][s]=t.index
            diz[t.index]=s
            s=s+1
        print riga
        
        for link in self.F:            #per tutti i collegamenti all'interno della rete
            if link.pre==True:
                riga[diz[link.state.index]][diz[link.trans.index]]=-1   #se è una precondizione allora -1
            else:
                riga[diz[link.state.index]][diz[link.trans.index]]=1    #se è una postcondizione allora 1
        
        self.matrice=riga  #salva la matrice all'interno della rete
        for t in range(len(self.T)+1):
            if t==0:
                print "        ", 
            else:
                print self.idNome(self.matrice[0][t]), " ", 
        for s in range(1, len(self.P)+1):  #stampo la matrice di incidenza 
            for i in range(len(self.T)+1):
                if i==0:
                    print ""
                    print self.idNome(self.matrice[s][i])+ " ", 
                else:
                    print str(self.matrice[s][i])+" ", 
    print ""
    
    def toDot(self, nomeFile,  estensione): #[label = ""];
        """crea il file .dot per la generazione dell'immagine della rete con graphviz"""
        self.check()
        self.fileDOT=nomeFile+".dot"
        f=open(nomeFile+".dot", 'w')  #apertura del file di output in modalità scrittura
        f.write('digraph g{\n') #scrittura all'interno del file, indica un grafo orientato
        f.write('\nnode [shape=circle];' ) #specifica che gli stati sono rappresentati come nodi circolari
        marked=list()
        if self.M0==[]:
            for stato in self.P: 
                    f.write(str(stato.index) +'[label = "'+stato.nome+'"];') #inserimento dei nomi degli stati
        else:
            for i, stato in enumerate(self.P): 
                if self.M0[i]==0:
                    f.write(str(stato.index) +'[label = "'+stato.nome+'"];') #inserimento dei nomi degli stati
                else:
                    f.write(str(stato.index) +'[label = <<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\"> \
    <TR><TD><IMG SRC=\"img/mark1.png\"/></TD></TR> \
    <TR><TD>'+stato.nome+'</TD></TR> </TABLE>>];') #inserimento dei nomi degli stati e marche
                    
            
        f.write('\nnode [shape=box];') #specifica che le transizioni sono rappresentate come nodi rettangolari
        for trans in self.T:
            f.write(str(trans.index) +'[label = "'+trans.nome+'"];') #inserimento dei nomi delle transizioni

#        f.write('\nnode [shape=doublecircle];') #specifica che gli stati marcati sono rappresentati come nodi con doppio cerchio
#        if marked>0:
#            for marca in marked:
#                f.write(str(marca.index) +'[label = "'+marca.nome+'"];')

        for freccia in self.F:   #scrittura all'interno del file dei collegamenti tra stati e transizioni nella forma a->B
            f.write('\n')
            if freccia.pre==True:
                f.write(str(freccia.state.index) + '->' + str(freccia.trans.index))
            else:
                f.write(str(freccia.trans.index) + '->' + str(freccia.state.index))
        
        f.write('}\n')
        f.close()
        os.system('dot -T'+estensione+' -O '+nomeFile+'.dot')

    def addFromUser(self):
        """inserimento della specifica della rete da terminale"""
        print('inserire gli stati della rete separati da spazi:\n')
        stringa=sys.stdin.readline()
        listaStati=stringa.split(' ')
        for s in listaStati:
            self.addState(s.replace('\n',''),0)
   
        print('\ninserisci le transizioni separate da spazi:\n')
        stringa=sys.stdin.readline()
        listaTrans=stringa.split(' ')
        for t in listaTrans:
            self.addTrans(t.replace('\n',''))
    
      
        print('inserisci un collegamento (es. stato > transizione)')
        stringa=sys.stdin.readline()
    
        j=0
        s=-1
        t=-1
        pre=True
    
        while stringa!='\n':
            link=stringa.split(' ')
            s=self.idState(link[j])
            if s>=0:
                pre=True
            else:
                t=self.idTrans(link[j])
                if t>=0:
                    pre=False
                else:
                    print('ERRORE(1): lo stato o transizione '+ link[j] + ' non esiste')
      
            j=2
            link[j]=link[j].replace('\n','')
            
            if pre==True:
                t=self.idTrans(link[j])
                if t<0:
                    print('ERRORE(2): non può essere inserito un collegamento tra due stati o due transizioni')
            else:
                s=self.idState(link[j])
                if s<0:
                    print('ERRORE(3): non può essere inserito un collegamento tra due stati o due transizioni')

            print('stato: ', s , 'transizione: ', t, '\n')
            if s>=0 and t>=0:
                self.addLink(s,t,pre)
            
            j=0
            s=-1
            t=-1
            pre=True    
            print('\ninserisci un collegamento:')
            stringa=sys.stdin.readline()

    def isOccurrency(self):
        """ritorna True se la rete è una rete di occorrenza False altrimenti"""
        #affinchè una rete sia di occorrenza devono valere le seguenti proprietà:
        #-gli stati hanno massimo una precondizione e una postcondizione
        #-non esistono cicli
        print self.F
        if self.matrice==list():
            self.toMatrix()

        #controllo che tutti gli stati abbiano al massimo una pre e/o una post condizione
        #utilizzando la matrice di incidenza questo si può determinare sommando gli elementi di ogni riga
        #e controllando che la loro somma sia compresa tra -1 e 1 e che il loro conteggio non sia superiore a 2
        somma =0
        count=0
        #contr=0
        for riga in self.matrice[1:len(self.matrice)]:
            for i in range(1, len(riga)):
                if riga[i]!=0:
                    somma=somma+riga[i]
                    count=count+1
                if somma>1 or somma<-1 or count>2:
                    print 'La rete non è di occorrenza (gli stati hanno più di una pre e una post condizione)'
                    print somma
                    return False
            somma=0
            count=0
            

        print 'Tutti gli stati della rete hanno al più una pre e/o una post condizione'
    
    #controllo che la rete non abbia cicli
        link=self.F[:] #faccio una copia della lista che rappresenta la relazione di flusso
        obj=-1
        state=False
        if link[0].pre==True:
            obj=link[0].state.index
            state=True
        else:
            obj=link[0].trans.index
            state=False

        if RicercaCicli(obj,state,link,list())==True:
            print "La rete è di occorrenza (non sono stati riscontrati cicli)"#id del primo oggetto, se è uno stato, id di partenza della lista visitati
            return True
        else:
            print "La rete non è di occorrenza"
            return False


def RicercaCicli(obj, state, link, oldVisitati):
    """ricerca in profondità dei cicli della rete""" 
    com=-1
    visitati=oldVisitati[:]
    visitati.append(obj)
#    for com in link:
#        if  com !=-1:
#            if com.pre==True:
#                print "link:", com.state.nome,  "->", com.trans.nome
#            else:
#                print "link:", com.state.nome,  "<-", com.trans.nome
#        else:
#            print '-1'
#    print '\n'
    for i in range(len(link)):
        if link[i]!=-1:
            #if state==True:
            if link[i].state.index==obj and link[i].pre==True:
                try:
                    com=visitati.index(link[i].trans.index) #controllo che il nodo in cui mi sto spostando 
                    if com>=0:                              #non sia già stato visitato nel percorso che sto seguendo
                        print "La rete presenta un ciclo quindi non è una rete di occorrenza"
                        return False
                except ValueError:
                    ap=link[i].trans.index #prelevo la transizione in cui mi sposto
                    link[i]=-1 #elimino il link che ho utilizzato per spostarmi
                    if RicercaCicli(ap,False,link,visitati)==False: #chiamata ricorsiva
                        return False
            elif link[i].trans.index==obj and link[i].pre==False:
                try:
                    com=visitati.index(link[i].state.index) #controllo che il nodo in cui mi sto spostando 
                    if com>=0:                              #non sia già stato visitato nel percorso che sto seguendo
                        print "La rete presenta un ciclo quindi non è una rete di occorrenza"
                        return False
                except ValueError:
                    ap=link[i].state.index
                    link[i]=-1
                    if RicercaCicli(ap,True,link,visitati)==False: #chiamata ricorsiva
                        return False
    return True

#classe che rappresenta un nodo del grafo dei casi
class nodeGraph:
    prox=list()  #lista dei nodi raggiungibili da questo nodo con associata la transizione che scatta
    stati=set() #stati marcati in questo nodo
    visited=False #variabile di appoggio per la visita del grafo
    
    def __init__(self,stati):
        self.prox=list()
        if isinstance(stati,list): #può essere richiamata con una lista oppure con un set di elementi
            for stato in stati:
                self.stati.add(stato)
        else:
            self.stati=stati.copy()
        print "creato nuovo nodo",  self.stati    
        
        
    def __str__(self): #rappresentazione del nodo con una stringa (metodo chiamato automaticamente dalla funzione print)
        """rappresentazione dell'oggetto sotto forma di stringa"""
        stringa= "{"+str(list(self.stati))+"}"
        return stringa

    def addNext(self, prossimoStato, transizione):
        """aggiunge un nuovo collegamento ad un nodo."""
        lista=[prossimoStato, transizione]
        self.prox.append(lista[:])
        #print "add-next:" , self,  prossimoStato.stati,  "con",  transizione
        
def createCaseGraph(rete, marcatura):
    """crea il grafo dei casi a partire dalla marcatura iniziale"""
    root=nodeGraph(marcatura[:]) #crea il nodo iniziale
    ok=True
    for m in marcatura:
        if rete.idState(m)<0:
            print m
            print "All'interno della marcatura possono esserci solo stati e non transizioni"
            ok=False
    if ok:
        M=set(marcatura[:]) #crea la marcatura del nodo iniziale, la marcatura è un insieme di indici globali che indicano uno stato
        lista=list()
        rete.toMatrix()
        graphCase=createCaseGraphRic(rete,  M,  root,  lista) #chiamata risorsiva per la creazione del grafo dei casi
        print "è stato creato il grafo dei casi a partire dalla marcatura iniziale:" ,  marcatura
        return graphCase[:]
    
def createCaseGraphRic(rete, marcatura, nodoAttuale, listGC):
    """chiamata ricorsiva della creazione del grafo"""
    #creo il nodo della marcatura iniziale
    M=marcatura.copy()
    #lista di tutti i nodi, restituita alla fine dalla funzione
    listGC.append(nodoAttuale)
    
    scatto=list() #lista degli eventi che devono scattare
    contr=True #variabile di appoggio
    pre=list() #lista delle precondizioni
    post=list() #lista delle postcondizioni
  
    for t in range(len(rete.T)):
        for s in range(len(rete.P)):
            #print t, s
            com=rete.matrice[s+1][0] #com è l'id globale dello stato che stiamo prendendo in considerazione
            #print "id globale: ", com,  "M:",  M,  contr
            #print rete.matrice[s][t] ,"s=", s, "t=" ,t
            
            #esploro tutta la matrice di incidenza creata precedentemente
            if rete.matrice[s+1][t+1]==-1 and com in M: #se il posto è una precondizione per lo stato ed è presente nella marcatura
                pre.append(com)
            elif rete.matrice[s+1][t+1]==1 and com not in M: #se il posto è una postcondizione per lo stato e non è presente nella marcatura
                post.append(com) 
            elif rete.matrice[s+1][t+1]==0: #il posto non è connesso alla transizione in alcun modo
                pass
            else:
                contr=False  #se entra qui allora lo stato non può scattare
                #print "break"
                break
                
                #se lo stato può scattare
        if contr==True:
            lista=[rete.matrice[0][t+1], pre[:], post[:]]
            #print pre, "->", lista[0],  "->", post
            scatto.append(lista[:]) #appendo lo stato che può scattare con le sue pre e post-condizioni
        contr=True
        del pre[:]
        del post[:]
    
    newMark=set()
    setVuoto=set()
    for e in scatto:
        if set(e[1])!=setVuoto or set(e[2])!=setVuoto: #se c'è almeno uno stato che può scattare
            prec=set(e[1])
            postc=set(e[2])
            #print "M",  M,  e[1],e[2],"precondizioni: ", prec ,  "postcondizioni",  postc,  "scatta:",  e[0]
            newMark=M.difference(prec) #tolgo le precondizioni
            newMark=newMark.union(postc) #aggiungo le postcondizioni
            nodoEx=existNode(listGC, newMark) #controllo che se il nuovo nodo (nuova marcatura) esiste già
            if nodoEx==-1:
                #il nodo non esiste allora ne creo uno nuovo
                newNode=nodeGraph(newMark.copy())
                nodoAttuale.addNext(newNode,e[0])
                createCaseGraphRic(rete,newMark,newNode, listGC) #chiamata ricorsiva sul nuovo nodo creato
            else:
                #il nodo esiste già quindi collego quello attuale con il nodo esistente
                #non faccio chiamate ricorsive in quanto se esiste già allora sarà in fase di esplorazione e già esplorato
                nodoAttuale.addNext(nodoEx,e[0])
    return listGC

def existNode(listaNodi,marcatura):
    """Controlla se all'interno della lista dei nodi creati esiste un nodo con una certa marcatura."""
    for nodo in listaNodi:
        if marcatura.issubset(nodo.stati) and marcatura.issuperset(nodo.stati): 
            #controllo che l'insieme degli stati della marcatura sia esattamente lo stesso 
            return nodo
    return -1

def esplora(nodo):
    """Esplora il grafo dei casi."""
    esploraRic(nodo)
    azzeraVisite(nodo)
    
def azzeraVisite(nodo):
    """Azzera i campi di controllo utili per la visita del grafo."""
    nodo.visited=False
    for prossimo in nodo.prox:
        if prossimo[0].visited==True:
            azzeraVisite(prossimo[0])
            
def esploraRic(nodo):
    """Esplora il grafo dei casi."""
    nodo.visited=True
    print "esplora:",nodo.stati
    for prossimo in nodo.prox:
        if prossimo[0].visited==False:
            print prossimo[1], ">>\n"
            esploraRic(prossimo[0])
            
            
def CGToDot(rete, nodoAttuale,  nomeFile,  estensione):
    """Crea il file .dot del grafo dei casi."""
    graphDOT=nomeFile+'.dot'
    f=open(nomeFile+'.dot', 'w') #apertuta in scrittura del file .dot
    f.write('digraph g{\n') #indica un grafo orientato
    f.write('\nrankdir = LR;')
    f.write('\nnode [shape=box];\n' ) 
    CGToDotRic(rete, f, nodoAttuale) #chiamata alla funzione ricorsiva della creazione del grafo dei casi
    f.write('}' )
    f.close()
    os.system('dot -T'+estensione+' -O '+nomeFile+'.dot')
    print 'creato il grafo dei casi'+nomeFile+'.dot e la relativa immagine '+ estensione
    
def CGToDotRic(rete,  f, root):
    """Crea il file .dot del grafo dei casi."""
    root.visited=True 
    #print root
    #itero su tutti i nodi che possono essere raggiunti dal nodo del grafo attuale
    for prossimo in root.prox:
        statiR=list(root.stati)
        statiP=list(prossimo[0].stati)
        f.write('"[')
                
        for i in statiR:
            f.write(rete.dictN[i])
            f.write(' ')
        
        f.write(']"->"[')
        for i in statiP:
            f.write(rete.dictN[i])
            f.write(' ')
            
        f.write(']"[label="')
        f.write(rete.dictN[prossimo[1]])
        f.write('"]\n')
        #print "else:",  root ,  "->" ,  prossimo[0],  "scatta:", prossimo[1]
        #print prossimo,  "nodo:",  root
        #controllo che il prossimo nodo non sia già stato visitato altrimenti non devo eseguire la chiamata ricorsiva
        if prossimo[0].visited==False:
            CGToDotRic(rete,  f, prossimo[0]) #chiamata ricorsiva sul prossimo nodo
                
                
##Esempio di utilizzo del modulo
#g=PetriNet() #creazione di una nuova istanza della rete
##f=PetriNet()
###g.addFromUser() #docommentare per inserire la rete da terminale
###g.isOccurrency()
##g.addFromUser()
####inserimento della rete
#print "creazione rete g"
#g.addState("Sp,Bp",False) #0
#g.addState("Sp,Bv",False) #1
#g.addState("Sv,Bv",False) #2
#g.addState("Sv,Bp",False) #3
#g.addTrans("A") #4
#g.addTrans("B") #5
#g.addTrans("C") #6
#g.addTrans("D") #7
#g.addTrans("E") #8
#g.addPre(1,4)
#g.addPre(1,5)
#g.addPre(3,8)
#g.addPre(0,6)
#g.addPre(2,7)
#g.addPost(0,4)
#g.addPost(3,6)
#g.addPost(3,7)
#g.addPost(1,8)
#g.addPost(2,5)
#g.toMatrix()
##grafo=createCaseGraph(g,[0, 1])
#g.setM0([1, 1])
#g.toDot('daPy', 'jpg')
#CGToDot(grafo[0], 'nuovo', 'jpg')
#
#g.toDot('daPy')
#
#
##
#print "creazione rete f"
#f.addState("0B",False) #0
#f.addState("1B",False) #1
#f.addState("2B",False) #2
#f.addState("3B",False) #3
#f.addTrans("AB") #4
#f.addTrans("BB") #5
#f.addTrans("CB") #6
#f.addTrans("DB") #7
#f.addPre(0,4)
#f.addPre(1,4)
#f.addPre(1,5)
#f.addPre(2,6)
#f.addPost(2,4)
#f.addPost(3,5)
#f.addPost(1,6)
#f.addPost(0,6)
##
###
#print "unione"
#p=[[0, 0]]
#t=[[5, 5], [6, 6]]
#
#print p
#print t
#nuova=g.union(f, p, t)
#nuova.toDot()
#e se usassimo  • per le marche??
##g.toMatrix()
##f.toDot()
##grafo=createCaseGraph(g,[0, 1])
##esplora(grafo[0])
##CGToDot(grafo[0])
