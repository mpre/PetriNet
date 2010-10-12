#! /usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import copy

def find_expand(text, var={}):
    """Trova i cicli for e li espande ricorsivamente"""
    # 1. Ricerca un for
    # 2. Trova la graffa che chiude il for
    # 3. Espande ricorsivamente il blocco di codice
    # 4. Ripete finché i for di *primo livello* non sono finiti
    expanded_txt = ""
    while len(text) != 0:
        if text.find("for(") == -1:
            expanded_txt = expanded_txt + expand(text, vars)
            text = ""
        else:
            blk_begin = text.find("for(") + 4
            try:
                blk_end = find_balanced_rbrace(text, text.find("){"))
            except Exception:
                print "Unbalanced {"
                exit()
            init_conds, end_conds, incr_conds = text[blk_begin: text.find("){")].split(";")
            init_conds = dictionarize(init_conds.split(','))
            end_conds = dictionarize(end_conds.split(','))
            incr_conds = dictionarize(incr_conds.split(','))

            expanded_txt = expanded_txt + expand(text[:blk_begin - 4], var) + "\n"

            cd_blk = text[text.find("){") + 2 :blk_end]
            for cond in init_conds:
                exec(cond)
            while reached_conds(end_conds, var):
                expanded_txt = expanded_txt + expand(cd_blk, var)
                var = increase_var(incr_conds, var)
            text = text[blk_end + 1:]
    return expanded_txt
                
        
def expand(text, var):
    """Espande un blocco di codice con i valori delle variabili contenuti nel dizionario var.
    Se vengono trovati cicli for viene richiamata la funzione find_expand"""
    sub_for_begin = text.find("for(")
    while sub_for_begin != -1:
        if sub_for_begin != -1:
            try:
                sub_for_end = find_balanced_rbrace(text, sub_for_begin)
                text = text[:sub_for_begin] + find_expand(text[sub_for_begin: sub_for_end + 1], var) + text[sub_for_end + 1:]
            except Exception:
                print "Unbalanced {"
            try:
                sub_for_begin = text.find("for(")
            except Exception:
                sub_for_begin = -1

    expanded_txt = ""

    while len(text) != 0:
        if "[" in text:
            expanded_txt = expanded_txt + text[:text.find("[") + 1]
            #print text[text.find("["): find_balanced_rsqbrace(text[text.find("["))]
            #print text[text.find("[") + 1: find_balanced_rsqbrace(text, text.find("["))]
            expanded_txt = expanded_txt + str(simplify(expand(text[text.find("[") + 1: find_balanced_rsqbrace(text, text.find("["))], var), var)) + "]"
            text = text[find_balanced_rsqbrace(text,text.find("[")) + 1:]
        else:
            expanded_txt = expanded_txt + text
            text = ""
            
    return expanded_txt

def find_balanced_rbrace(text, begin = 0):
    """Trova l'indice della } bilanciata con la prima { trovata in text a partire dall'indice begin"""
    deep = -1
    index = begin
    for char in text[begin:]:
        if char == "}" and deep == 0:
            return index
        elif char == "}":
            deep = deep - 1
            index = index + 1
        elif char == "{":
            deep = deep + 1
            index = index + 1
        else:
            index = index + 1
    if index == len(text):
        raise Exception("Unbalanced {")

def find_balanced_rsqbrace(text, begin = 0):
    """Trova l'indice della [ bilanciata con la prima { trovata in text a partire dall'indice begin"""
    deep = -1
    index = begin
    for char in text[begin:]:
        if char == "]" and deep == 0:
            return index
        elif char == "]":
            deep = deep - 1
            index = index + 1
        elif char == "[":
            deep = deep + 1
            index = index + 1
        else:
            index = index + 1
    if index == len(text):
        raise Exception("Unbalanced [")
        
def simplify(exp, vars):
    """Semplifica l'espressione exp con i valori delle variabili contenuti nel dizionario var"""
    # Se leggendo qui sotto ti chiedi cosa stiano a significare
    # car e cdr... beh, è meglio che ti dai una ripassata
    # al corso di Linguaggi di programmazione
    #print exp
    try:
        exp = int(exp)
        return exp
    except Exception:
        app = copy.deepcopy(exp)
        exp = exp.replace(" ","").replace("\t", "")
        if "%" in exp:
            car, cdr = exp.split("%", 1)
            return simplify(car, vars) % simplify(cdr, vars)
        elif "/" in exp:
            car, cdr = exp.split("/", 1)
            return simplify(car, vars) / simplify(cdr, vars)
        elif "*" in exp:
            car, cdr = exp.split("*", 1)
            return simplify(car, vars) * simplify(cdr, vars)
        elif "+" in exp:
            car, cdr = exp.split("+", 1)
            return simplify(car, vars) + simplify(cdr, vars)
        elif "-" in exp:
            car, cdr = exp.split("-", 1)
            return simplify(car, vars) - simplify(cdr, vars)
        else:
            try:
                if str(exp) in vars:
                    return int(vars[exp])
                else:
                    return app
            except Exception:
                return app

def reached_conds(end_conds, var):
    """Ritorna vero se almeno una condizione di end_conds è stata raggiunta"""
    for cond in end_conds:
        if not eval(cond):
            return False
    return True

def increase_var(incr_conds, var):
    """Ritorna le variabili contenute in var aumentate secondo le condizioni contenute in incr_conds"""
    for cond in incr_conds:
        exec(cond)
    return var

def dictionarize(conds):
    # Futuro me, futuro sviluppatore che leggerai questo
    # codice, futuro lurkatore di file:
    # So benissimo che questa funzione potrebbe venire
    # migliorata DECISAMENTE.
    # Ho perso 4 giorni a scrivere un modulo che
    # avesse la parvenza di un precompilatore
    # funzionante, migliorare 'sta porcheria è l'ultimo dei
    # miei pensieri ora.
    # Come spesso mi è capitato leggere sui libri di testo di
    # matematica (soprattutto quelli maledetti di Matematica
    # Discreta):
    # Si lascia al lettore la dimostrazione (in questo caso
    # il miglioramento) per esercizio.
    new_conds = []
    for cond in conds:
        cond = cond.replace(" ","").replace("\t","")
        if "==" in cond:
            cond_name, cond_value = cond.split("==")
        elif "%" in cond:
            cond_name, cond_value = cond.split("%")
        elif "+=" in cond:
            cond_name, cond_value = cond.split("+=")
        elif "-=" in cond:
            cond_name, cond_value = cond.split("-=")
        elif "<=" in cond:
            cond_name, cond_value = cond.split("<=")
        elif ">=" in cond:
            cond_name, cond_value = cond.split(">=")
        elif "=" in cond:
            cond_name, cond_value = cond.split("=")
        elif "<" in cond:
            cond_name, cond_value = cond.split("<")
        elif ">" in cond:
            cond_name, cond_value = cond.split(">")

        try:
            cond_name = int(cond_name)
        except Exception:
            
            cond_name = "var['{0}']".format(cond_name)
        try:
            cond_value = int(cond_value)
        except Exception:
            cond_value = "var['{0}']".format(cond_value)
            
        if "==" in cond:
            new_conds = new_conds + ["{0}=={1}".format(cond_name, cond_value)]
        elif "%" in cond:
            new_conds = new_conds + ["{0}%{1}".format(cond_name, cond_value)]
        elif "+=" in cond:
            new_conds = new_conds + ["{0}+={1}".format(cond_name, cond_value)]
        elif "-=" in cond:
            new_conds = new_conds + ["{0}-={1}".format(cond_name, cond_value)]
        elif "<=" in cond:
            new_conds = new_conds + ["{0}<={1}".format(cond_name, cond_value)]
        elif ">=" in cond:
            new_conds = new_conds + ["{0}>={1}".format(cond_name, cond_value)]
        elif "=" in cond:
            new_conds = new_conds + ["{0}={1}".format(cond_name, cond_value)]
        elif "<" in cond:
            new_conds = new_conds + ["{0}<{1}".format(cond_name, cond_value)]
        elif ">" in cond:
            new_conds = new_conds + ["{0}>{1}".format(cond_name, cond_value)]
    return new_conds

# t = "for(x=0;x<=2;x+=1){ciao[x] ->(4) cacca[x - 1];  for(y=x;y<=3;y+=1){mamma[y];}} for(z=7;z>=3;z-=1){ciao[z];}   "

# t = t.replace("\n","").replace("\t","").replace(" ","")
# print find_expand(t).replace(";",";\n")

def main():
    usage = "usage: %prog -i INPUT_FILE -o OUTPUT_FILE"
    arg_par = optparse.OptionParser(usage=usage)
    arg_par.add_option("-i", "--input", action="store",
                       type="string", dest="input_file",
                       help="Source file")
    arg_par.add_option("-o", "--output", action="store",
                       type="string", dest="output_file",
                       help="Destination file")
    arg_par.add_option("-p", "--print-output", action="store_true",
                       dest="print_output", default=False)
    opts, args = arg_par.parse_args()
    
    file_content = ""
    for line in open(opts.input_file, 'r'):
        if line.replace(" ","").replace("\t","")[0:2] == "//":
            pass
        else:
            file_content += line
    file_content = file_content.replace("\n","").replace("\t","")
    output_content = find_expand(file_content)
    output_content=output_content.replace(";",";\n")
    if opts.print_output:
        print output_content
    else:
        of = open(opts.output_file, 'w')
        of.write(output_content)
        of.close()
    
if __name__ == "__main__":
    main()
