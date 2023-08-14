# Importações
from functools import reduce
from re import search, sub

def operation_strings(string):
    

    # List Comprehension para separar a string a cada sinal de soma (+)
    lsoma = [i for i in string.split('+')]
    # List Comprehension para separar a list de soma a cada sinal de subtração (-)
    lsub = [['0' if x=='' else x for x in i.split('-')] for i in lsoma]
    # List Comprehension para separar a list de subtração a cada sinal de multiplicação (*)
    lmult = [[i.split('*') for i in sublist] for sublist in lsub]
    # List Comprehension para separar a list de multiplicação a cada sinal de divisão (/)
    ldiv = [[[i.split('/') for i in subsublist] for subsublist in sublist] for sublist in lmult]
    # List Comprehension para separar a list de divisão a cada sinal de potência (^)
    lelev = [[[[i.split('^') for i in subsubsublist] for subsubsublist in subsublist] for subsublist in sublist] for sublist in ldiv]
    
    # Reduzindo as lists e suas sublists com a função reduce seguindo a regra de precedência PEMDAS
    resultado = reduce(lambda a,b: float(a)+float(b), [
        reduce(lambda a,b: float(a)-float(b), [
        reduce(lambda a,b: float(a)*float(b), [
        reduce(lambda a,b: float(a)/float(b), [
        reduce(lambda a,b: float(a)**float(b),[i for i in elist])
            for elist in divlist])
            for divlist in multlist])
            for multlist in sublist])
            for sublist in lelev])

    return resultado

def priority(string):
    if '(' in string:
        for index_open in range(len(string)):
            if string[index_open] == '(':
                index_inicio = index_open
        for index_close in range(len(string[index_inicio:])):
            if string[index_inicio:][index_close] == ')':
                index_end = index_close + index_inicio
                break
        string = string[:index_inicio] + str(operation_strings(string[index_inicio+1:index_end])) + string[index_end+1:]


    if '--' in string:
        string = sub(r'--', '+', string)

    elif '+-' in string:
        string = sub(r'\+-', '-', string)

    elif '*-' in string:
        elements_string = search(r'(([-+])\d+)[*][-](\d+)', string).groups()
        if elements_string[1] == '+':
            string = sub('[-+]\d+[*][-]\d+', str(-float(elements_string[0])*float(elements_string[2])), string)
        elif elements_string[1] == '-':
            string = sub('[-+]\d+[*][-]\d+', '+' + str(float(elements_string[0])*float(elements_string[2])*-1), string)
        
    elif '/-' in string:
        elements_string = search(r'(([-+])\d+)[/][-](\d+)', string).groups()
        if elements_string[1] == '+':
            string = sub('[-+]\d+[/][-]\d+', str(-float(elements_string[0])*float(elements_string[2])), string)
        elif elements_string[1] == '-':
            string = sub('[-+]\d+[/][-]\d+', '+' + str(float(elements_string[0])*float(elements_string[2])*-1), string)

    return string

def executor_operation_strings(string):
    try:
        while '(' in string:
            string = priority(string)
        return operation_strings(string)
    except ZeroDivisionError:
        current_value = "Error! Division by Zero"
    except Exception as e:
        current_value = f"Erro: {str(e)}"

