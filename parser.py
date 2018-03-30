from model import Constituent
from model import TableNode


def read_grammar():
    global grammar
    grammar = {}
    f = open("grammar.txt", "r")
    for line in f.readlines():
        tokens = [x.strip() for x in line.strip().split("->")]
        if len(tokens) != 2:
            continue
        left, right = tokens
        if right not in grammar:
            grammar[right] = list()
        grammar[right].append(tokens)

    for e in grammar:
        print(e, grammar[e])
    f.close()


def read_input():
    f = open("input.txt", "r")
    inputs = [line.strip() for line in f.readlines()]
    f.close()
    return inputs


def initialize_table(length):
    table = list()
    for i in range(0, length):
        temp = list()
        for j in range(0, length+1):
            temp.append(TableNode(i, j))
        table.append(temp)
    return table


def dfs(node):
    if node is None:
        return ""
    if node.is_leaf():
        return "({} {})".format(node.pos, node.word)
    else:
        output=""
        output += dfs(node.left)
        output += dfs(node.right)
        return "({}{})".format(node.pos, output)


def print_parse_tree(table, length):
    for cons in table[0][length].cons:
        if cons.pos == 'S':
            print(dfs(cons))


def parsing(sentence):
    global grammar
    words = sentence.split(" ")
    length = len(words)
    # initialize table
    table = initialize_table(length)
    for j in range(1, length+1):
        for i in range(j-1, -1, -1):
            if i+1 == j:
                if words[i] in grammar:
                    for g in grammar[words[i]]:
                        table[i][j].cons.append(Constituent(i, j, words[j-1], g[0]))
                    for c in table[i][j].cons:
                        if c.pos in grammar:
                            for g2 in grammar[c.pos]:
                                table[i][j].cons.append(Constituent(i, j, words[j-1], g2[0]))
            elif j-i > 2:
                for k in range(i+1, j-1):
                    left = table[i][k].cons
                    right = table[k][j].cons
                    if len(left) > 0 and len(right) > 0:
                        for l_g in left:
                            for r_g in right:
                                candidate = "{} {}".format(l_g.pos, r_g.pos)
                                if candidate in grammar:
                                    for gram in grammar[candidate]:
                                        cons = Constituent(i, j, words[j-1], gram[0], l_g, r_g)
                                        table[i][j].cons.append(cons)
            else:
                left = table[i][j-1].cons
                right = table[i+1][j].cons
                for l_g in left:
                    for r_g in right:
                        candidate = "{} {}".format(l_g.pos, r_g.pos)
                        if candidate in grammar:
                            for gram in grammar[candidate]:
                                cons = Constituent(i, j, words[j-1], gram[0], l_g, r_g)
                                table[i][j].cons.append(cons)
    print_parse_tree(table, length)


if __name__ == "__main__":
    read_grammar()
    #inputs = read_input()
    #for sentence in inputs:
    #    parsing(sentence)
    parsing('time flies like an arrow')
    parsing('the man saw the boy with the telescope')

