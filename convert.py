import sys

# FUNCTIONS


# recursive function to convert the sentences to CNF, applying the given rule
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
    if (sentence[0] == 'or') and (sentence[1][0] == 'and') and (sentence[2][0] == 'and'):
        new_sentence = ('and', ('and', ('or', sentence[1][1], sentence[2][1]), ('or', sentence[1][1], sentence[2][2])), ('and', ('or', sentence[1][2], sentence[2][1]), ('or', sentence[1][2], sentence[2][2])))
        return new_sentence
    if (sentence[0] == 'or') and (sentence[2][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1], sentence[2][1]), ('or', sentence[1], sentence[2][2]))
        return new_sentence
    if (sentence[0] == 'or') and (sentence[1][0] == 'and'):
        new_sentence = ('and', ('or', sentence[1][1], sentence[2]), ('or', sentence[1][2], sentence[2]))
        return new_sentence
    return sentence


# function to convert sentences to the desired output format
def output_format(sentence):
    output_list = []

    if len(sentence) == 1:
        output_list.append("'" + str(sentence) + "'") # para ficar com plicas
        return output_list

    elif len(sentence) == 2:
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

# ordered list with functions
rule_list = [elim_2neg, conv_equivalence, elim_2neg, conv_implication, elim_2neg, morgans_law, elim_2neg, conv_distributive, elim_2neg]

# read input
for line in sys.stdin.readlines():
    sentence = eval(line)
    sentence_list.append(sentence)

# conversion to cnf
for sentence in sentence_list:
    # applying rules by order
    for rule in rule_list:
        # keep same rule while changing result of convert_to_cnf
        while 1:
            new = convert_to_cnf(sentence, rule)
            if new == sentence:
                break
            sentence = new
    # store converted sentences
    converted_list.append(sentence)


#  change to the desired output format and print results
for sentence in converted_list:
    result_list = output_format(sentence)
    if result_list:
        for sent in result_list:
            print(sent)