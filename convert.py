import sys

# FUNCTIONS


# function to convert the sentences to CNF
def convert_to_cnf(sentence, rule):
    if len(sentence) == 3:
        if len(sentence[1]) == 3:
            new_1 = convert_to_cnf(sentence[1], rule)
            sentence = (sentence[0], new_1, sentence[2])

        if len(sentence[1]) == 2:
            new_1 = rule(sentence[1])
            sentence = (sentence[0], new_1, sentence[2])

        if len(sentence[2]) == 3:
            new_2 = convert_to_cnf(sentence[2], rule)
            sentence = (sentence[0], sentence[1], new_2)

        if len(sentence[2]) == 2:
            new_2 = rule(sentence[2])
            sentence = (sentence[0], sentence[1], new_2)

    if len(sentence) == 2:
        if len(sentence[1]) == 3:
            new_1 = convert_to_cnf(sentence[1], rule)
            sentence = (sentence[0], new_1)

        if len(sentence[1]) == 2:
            new_1 = rule(sentence[1])
            sentence = (sentence[0], new_1)

    sentence = rule(sentence)
    return sentence


# function that apply rules by order
def apply_rules(sentence):
    for rule in rule_list:
        sentence = rule(sentence)
    return sentence


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
# --------------------------------------- DEVERIAM SER SO AS COM sentence[0] = or pq as outras ja sao cnf!!!!!!!!!!!!!!!!!!!!!!!!!
def conv_distributive(sentence):
    # distributive complexas ----------------------------------------------
    if (sentence[0] == 'or') and (sentence[1][0] == 'and') and (sentence[2][0] == 'and'):
        new_sentence = ('and', ('and', ('or', sentence[1][1], sentence[2][1]), ('or', sentence[1][1], sentence[2][2])), ('and', ('or', sentence[1][2], sentence[2][1]), ('or', sentence[1][2], sentence[2][2])))
        return new_sentence
    #if (sentence[0] == 'and') and (sentence[1][0] == 'or') and (sentence[2][0] == 'or'):
    #    new_sentence = ('or', ('or', ('and', sentence[1][1], sentence[2][1]), ('and', sentence[1][1], sentence[2][2])), ('or', ('and', sentence[1][2], sentence[2][1]), ('and', sentence[1][2], sentence[2][2])))
    #    return new_sentence
    # ---------------------------------------------------------------------
    if (sentence[0] == 'or') and (sentence[2][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1], sentence[2][1]), ('or', sentence[1], sentence[2][2]))
        return new_sentence
    if (sentence[0] == 'or') and (sentence[1][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1][1], sentence[2]), ('or', sentence[1][2], sentence[2]))
        return new_sentence
    #if (sentence[0] == 'and') and (sentence[2][0] == 'or'):
    #    new_sentence = ('or', ('and', sentence[1], sentence[2][1]), ('and', sentence[1], sentence[2][2]))
    #    return new_sentence
    #if (sentence[0] == 'and') and (sentence[1][0] == 'or'):
    #    new_sentence = ('or', ('and', sentence[1][1], sentence[2]), ('and', sentence[1][2], sentence[2]))
    #    return new_sentence
    return sentence

def output_format(sentence):
    output_list = []

    if len(sentence) == 1:
        output_list.append("'" + str(sentence) + "'") # para ficar com plicas
        return output_list

    elif len(sentence) == 2: # com [ ] ou juntar com caso len()=1 ????????????
        output_list.append(str(sentence))
        return output_list

    else:
        if sentence[0] == 'and':
            new_1 = output_format(sentence[1])
            new_2 = output_format(sentence[2])

            for sent in new_1:
                output_list.append(sent)

            for sent in new_2:
                output_list.append(sent)

            return output_list

        if sentence[0] == 'or':
            new_1 = output_format(sentence[1])
            new_2 = output_format(sentence[2])

            out_1 = ''

            for sent in new_1:
                out_1 += sent + ', '

            for sent in new_2:
                out_1 += sent + ', '

            out_1 = out_1[0:-2]  # remove virgula e espaço a mais
            out_1 = out_1.replace('[','') # remove [ dos 'or' interiores
            out_1 = out_1.replace(']', '') # remove ] dos 'or' interiores
            
            output_list.append('[' + out_1 + ']')

            return output_list


# -------------------------------------------------

# MAIN


sentence_list = []
converted_list = []
cnf_list = []
# ordered list with functions
rule_list = [conv_equivalence, conv_implication, elim_2neg, morgans_law, conv_distributive] #VERIFICAR: POR DISTRIBUIVA COMPLEXA OU FAZER EM 2 PASSOS?

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
        #print(sentence)

# convert the sentences to CNF
for sentence in sentence_list:
    # applying rules by order
    for rule in rule_list:
        sentence = convert_to_cnf(sentence, rule)
    # append sentence to list
    converted_list.append(sentence)

#  change to the desired output format
for sentence in converted_list:
    print(sentence)
    result_list = output_format(sentence)
    if result_list:
        for sent in result_list:
            print('>>', sent)
        cnf_list += result_list