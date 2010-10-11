from PetriNet import *
#####################################################
####### Test block is something close to hell #######
####### so don't below look please :D         #######
#####################################################
 

help(PetriNet)      
    
 
#n = PetriNet('net')
#p1 = Place('p1')
#p2 = Place('p2', 2) 
#p3 = Place('p1')
#t1 = Transition('t1')
#t2 = Transition('t1')
#print t1 == t2
#print repr(p1)
#print p1
#print p1.name
#print t1

#n.add(p1)
#n.add(p2)
#n.add(t1)
#n.add('Stringa')
#n.add(p3)

#p = Place('p')
#t = Transition('t')
#r = Transition('r')
#l1 = Link(t1,p1)
#l2 = Link(p2,t1,6)
#n.add(l1)
#n.add(l2)
#n.add(Transition('asdaf'))
#n.add(Transition('asdasfasad'))
#print n


#n.remove_isolated()
#print n
#stringa = '\t'
#for tr in n.transitions:
#    stringa = stringa +tr.name + '\t'
#print stringa 
#x = 0
#for line in n.to_matrix():
#    stringa = n.places[x].name + '\t'
#    for element in line:
#        stringa = stringa + str(element) + '\t'
#    x += 1
#    print stringa
    
#print n.to_matrix()

#m = PetriNet('rete')
#a = Place('a')
#b = Place('b',187)
#c = Place('c')
#d = Place('d')
#t1 = Transition('t1')
#t2 = Transition('t2')
#t3 = Transition('t3')
#t4 = Transition('t4')
#l1 = Link(a,t1)
#l2 = Link(t1,b,5)
#l3 = Link(b,t2)
#l4 = Link(t2,c)
#l5 = Link(c,t3)
#l6 = Link(t3,a)
#
#m.add(a)
#m.add(b)
#m.add(c)
#m.add(d)
#m.add(t1)
#m.add(t2)
#m.add(t3)
#m.add(t4)
#m.add(l1)
#m.add(l2)
#m.add(l3)
#m.add(l4)
#m.add(l5)
#m.add(l6)
#stringa = '\t'
#for tr in m.transitions:
#    stringa = stringa +tr.name + '\t'
#print stringa 
#x = 0
#for line in m.to_matrix():
#    stringa = m.places[x].name + '\t'
#    for element in line:
#        stringa = stringa + str(element) + '\t'
#    x += 1
#    print stringa
#print m.is_occurrency()
#m.to_dot('/home/tosh/Desktop/m','png')
#print m
#for place in m.places:
#    print place
#for transition in m.transitions:
#    print transition
#for link in m.links:
#    print link
#
#new_net = eval(repr(m))
#
#m.remove_isolated()
#stringa = '\t'
#for tr in m.transitions:
#    stringa = stringa +tr.name + '\t'
#print stringa 
#x = 0
#for line in m.to_matrix():
#    stringa = m.places[x].name + '\t'
#    for element in line:
#        stringa = stringa + str(element) + '\t'
#    x += 1
#    print stringa
#m.to_dot('/home/tosh/Desktop/m2','png')
#print m
#for place in m.places:
#    print place
#for transition in m.transitions:
#    print transition
#for link in m.links:
#    print link
#
#print new_net
#
#print new_net.check_balance()

a = Place('a')
b = Place('b')
c = Place('c',5)
d = Place('b')

t1 = Transition('t1')
t2 = Transition('t2')

l1 = Link(a,t1)
l2 = Link(t1,b)

l3 = Link(a,t2)
l4 = Link(t2,d)
l5 = Link(c,t2,5)

m = PetriNet('m')
m.add(a)
m.add(b)
m.add(t1)
m.add(l1)
m.add(l2)
#m.add(Place('m.a'))
n = PetriNet('n')
#n.add(a)
n.add(c)
n.add(d)
n.add(t2)
#n.add(l3)
n.add(l4)
n.add(l5)
#print n
m.to_dot('/home/tosh/Desktop/reti/'+m.name.replace('.','_').replace(' ',''), 'png')
#n.replace_place(c,Place('z'))
#print n
n.to_dot('/home/tosh/Desktop/reti/'+n.name.replace('.','_').replace(' ',''), 'png')
#print m
#print n
x = m.union(n, [d])
x.to_dot('/home/tosh/Desktop/reti/'+x.name.replace('.','_').replace(' ',''), 'png')
#print x

z = PetriNet('z')
e = Place('e')
t3 = Transition('t3')
l6 = Link(e,t3)
t4 = Transition('t4')
l7 = Link(t4,c)

z.add(e)
z.add(c)
z.add(t3)
z.add(t2)
z.add(a)
z.add(Link(t2,a))
z.add(t4)
z.add(l6)
z.add(l7)
print z
e.name='g'
print e in z.places
print z
#------------------------------------------------------------------------------ 
# z.to_dot('/home/tosh/Desktop/reti/'+z.name.replace('.','_').replace(' ',''), 'png')
#------------------------------------------------- y = x.union(z, [a,e,c], [t2])
# y.to_dot('/home/tosh/Desktop/reti/'+y.name.replace('.','_').replace(' ',''), 'png')
#------------------------------------------------------- y.add(Place('cacca',5))
# y.to_dot('/home/tosh/Desktop/reti/'+y.name.replace('.','_').replace(' ','')+'2', 'png')
#----------------------------------------------------------- y.remove_isolated()
# y.to_dot('/home/tosh/Desktop/reti/'+y.name.replace('.','_').replace(' ','')+'3', 'png')
#----------------------------------------------------------------- n.places = []
#------------------------------------------------------------------ n.remove(l1)
#------------------------------------------------------------------ n.remove(t1)
#n.remove(p1)
#print n
#l3 = Link(p,r,2)
#l4 = Link(t,p,1)
#l5 = Place('1',32)
#l6 = Link(r,t,8)


#print p
#print t
#print l1
#print l2
#print l3
#print l4
#print l1 == l2
#print l2 == l3

#print p.__class__.__name__ == 'Place'
