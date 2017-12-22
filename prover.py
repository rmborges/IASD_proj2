import sys

# Atom class and functions
class Atom:
    def __init__(self,name,neg):
        self.name = name
        self.neg = neg

    def is_equal(self,other):
        if ((self.name == other.name) and (self.neg == other.neg)):
            return 1
        return 0

    def is_neg(self,other):
        if ((self.name == other.name) and (self.neg != other.neg)):
            return 1
        return 0


# Reading File
def convert_to_atoms(sentence):
    atom_list=[]
    if(isinstance(sentence, str)):
        atom_list.append( Atom(sentence,0) )
    elif(isinstance(sentence, tuple) and (sentence[0]=='not')):
        atom_list.append( Atom(sentence[1],1) )
    elif(isinstance(sentence, list)):
        for part in sentence:
            if (isinstance(part, str)):
                atom_list.append(Atom(part, 0))
            elif (isinstance(part, tuple) and (part[0] == 'not')):
                atom_list.append(Atom(part[1], 1))
    return atom_list


# Sentence Functions
def clear_list(list):
    N=len(list)
    for i in range(N):
        list.remove(list[0])


def sent_attach(main_sent,new_block):
    for atom in new_block:
        main_sent.append(atom)


def search_atom(sentence,atom):
    for atom_s in sentence:
        if (atom.is_equal(atom_s)):
            return 1
    return 0


def is_trivial(sentence):
    for atom1 in sentence:
        for atom2 in sentence:
            if atom1.is_neg(atom2):
                return 1
    return 0


def s1_in_s2(sent1,sent2):
    for atom in sent1:
        if not search_atom(sent2,atom):
            return 0
    return 1


def resol_possible(sent1,sent2):
    for atom1 in sent1:
        for atom2 in sent2:
            if atom1.is_neg(atom2):
                return 1
    return 0


# List Functions
def replace(list1,list2):
    clear_list(list1)
    if len(list2)!=0:
        sent_attach(list1,list2)


def order_by_size(sentence_list):
    aux = []
    troca = 1
    while troca:
        troca = 0
        for i in range(len(sentence_list)-1):
            if len(sentence_list[i])>len(sentence_list[i+1]):
                aux=sentence_list[i]
                sentence_list[i]=sentence_list[i+1]
                sentence_list[i+1]=aux
                troca = 1


def clean_trivial(sentence_list):
    new=[]
    for sentence in sentence_list:
        if not is_trivial(sentence):
            new.append(sentence)
    clear_list(sentence_list)
    sent_attach(sentence_list,new)


def clean_repeated(sentence_list):
    new=[]

    for sentence in sentence_list:
        teste = 1

        for new_sent in new:
            if s1_in_s2(new_sent,sentence):
                teste=0
                break
        if teste:
            for new_sent in new:
                if s1_in_s2(sentence,new_sent):
                    new.remove(new_sent)
            new.append(sentence)

    if len(new)<len(sentence_list):
        replace(sentence_list,new)


# Algorithm Functions
def resolution(sent1,sent2):
    new_sent=[]
    for atom1 in sent1:
        for atom2 in sent2:
            if (atom1.is_neg(atom2)):
                sent_attach(new_sent,sent1)
                sent_attach(new_sent,sent2)
                new_sent.remove(atom1)
                new_sent.remove(atom2)
                return new_sent
    return new_sent


def factoring(sentence):
    new = []
    for atom in sentence:
        if not(search_atom(new,atom)):
            new.append(atom)
    if len(new)<len(sentence):
        replace(sentence, new)


def cnf_solver(sentence_list):
    new=[]
    while(len(sentence_list)>1):
        test=0
        i = 0
        for sent1 in sentence_list:
            if test:
                break
            i=i+1
            j=0
            for sent2 in sentence_list:
                j=j+1
                if (resol_possible(sent1,sent2) and (i!=j)):
                    new=resolution(sent1,sent2)
                    if (len(new)==0):
                        return True
                    sentence_list.remove(sent1)
                    sentence_list.remove(sent2)
                    factoring(new)
                    if not is_trivial(new):
                        sentence_list.append(new)
                    test = 1
                    break
        if test==0:
            return False

        clean_repeated(sentence_list)
        order_by_size(sentence_list)

    return False


# -------------------------------------

# MAIN

sentence_list = []

# read input
for line in sys.stdin.readlines():
    sentence = eval(line)
    atom_list = convert_to_atoms(sentence)
    sentence_list.append(atom_list)

# simplify the input list
clean_trivial(sentence_list)
clean_repeated(sentence_list)
order_by_size(sentence_list)
for sentence in sentence_list:
    factoring(sentence)

# solve the theorem prover
result = cnf_solver(sentence_list)

print(result)