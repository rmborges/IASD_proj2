import sys

# FUNCTIONS


# function to convert the sentences to CNF
def convert_to_cnf(sentence):
    if len(sentence) == 3:
        convert_to_cnf(sentence[1])
        convert_to_cnf(sentence[2])
    else:
        return apply_rules(sentence)


# function that apply rules by order
def apply_rules(sentence):
    for rule in rule_list:
        sentence = rule(sentence)
    return sentence


# check if sentence is complex (length = 3)
def complex_sentence(sentence):
    return len(sentence) == 3


# convert equivalence
def conv_equivalence(sentence):
    if(sentence[0] == "<=>"):
        new_sentence = ('and', ('=>', sentence[1], sentence[2]), ('=>', sentence[2], sentence[1]))
        return new_sentence
    return sentence


# convert implication
def conv_implication(sentence):
    if(sentence[0] == "=>"):
        new_sentence = ('or', ('not', sentence[1]), sentence[2])
        return new_sentence
    return sentence


# eliminate double negation
def elim_2neg(sentence):
    if sentence[0] == 'not' and sentence[1][0] == 'not':
        sentence = sentence[1][1]
    return sentence


# applying Morgan's law
def morgans_law(sentence):
    if(sentence[0] == 'not') and (sentence[1][0] == 'or'):
        new_sentence = ('and', ('not', sentence[1][1]), ('not', sentence[1][2]))
        return new_sentence
    if(sentence[0] == 'not') and (sentence[1][0] == 'and'):
        new_sentence = ('or', ('not', sentence[1][1]), ('not', sentence[1][2]))
        return new_sentence
    return sentence


# applying distributive properties
def conv_distributive(sentence):
    if (sentence[0] == 'or') and (sentence[2][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1], sentence[2][1]), ('or', sentence[1], sentence[2][2]))
        return new_sentence
    if (sentence[0] == 'or') and (sentence[1][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1][1], sentence[2]), ('or', sentence[1][2], sentence[2]))
        return new_sentence
    if (sentence[0] == 'and') and (sentence[2][0] == 'or'):
        new_sentence = ('or', ('and', sentence[1], sentence[2][1]), ('and', sentence[1], sentence[2][2]))
        return new_sentence
    if (sentence[0] == 'and') and (sentence[1][0] == 'or'):
        new_sentence = ('or', ('and', sentence[1][1], sentence[2]), ('and', sentence[1][2], sentence[2]))
        return new_sentence


# -------------------------------------------------

# MAIN


sentence_list = []
cnf_list = []
rule_list = [conv_equivalence, conv_implication, elim_2neg, morgans_law, conv_distributive]

# read the input - ESTE É O CERTO! (FUNCIONA)
#for line in sys.stdin.readlines():
#    sentence = eval(line)
#    print(sentence)
#    sentence_list.append(sentence)

# read input - para testar sem linha de comandos
with open("sentences.txt", "r") as file:
    for line in file:
        sentence = eval(line)
        sentence_list.append(sentence)
        print(sentence)

# convert the sentences to CNF
for sentence in sentence_list:
    cnf_sentence = convert_to_cnf(sentence)
    #teste = conv_implication(sentence)
    print(' ',conv_distributive(sentence))
    #print(' ',cnf_sentence)
    # append sentence in CNF to list
    cnf_list.append(cnf_sentence)