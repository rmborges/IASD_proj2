# MAIN

sentence_list = []
cnf_list = []
rule_list = [conv_equivalence, conv_implication, elim_2neg, morgans_law, conv_distributive]

# read the file
with open("sentences.txt", "r") as file:
    for line in file:
        sentence = eval(line)
        sentence_list.append(sentence)

# convert the sentences to CNF
for sentence in sentence_list:
    cnf_sentence = convert_to_cnf(sentence)
    # append sentence in CNF to list
    cnf_list.append(cnf_sentence)

# --------------------------------------------------

# FUNCTIONS

# function to convert the sentences to CNF
def convert_to_cnf(sentence):
    if complex_sentence(sentence):
        convert_to_cnf(sentence)
    else:
        sentence = apply_rules(sentence)
    return sentence

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

    return sentence

# convert implication
def conv_implication(sentence):

    return sentence

# eliminate double negation
def elim_2neg(sentence):
    if sentence[0] == 'not' and sentence[1][0] == 'not':
        sentence = sentence[1][1]
    return sentence

# applying Morgan's law
def morgans_law(sentence, type):
    #if type == 'or':

    #if type == 'and':

    return sentence

# applying distributive properties
def conv_distributive(sentence):

    return sentence
