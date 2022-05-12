import sys
import getopt
import re
import copy

def ConvertNegative(lit):
    
    #['A'] -> ['-A']
    #['-A'] -> ['A']
    
    l = copy.deepcopy(lit)
    if lit[0] == '-':
        return l[1:]
    else:
        return '-' + l
def readFile(input_file):
   

    with open (input_file) as fin:
        alpha = []
        clause = fin.readline().replace('OR', '')
        clause_lst = []
        
        if clause[0][0] == '-':
                clause_lst.append(clause[1])
        else:
                clause_lst.append('-'+clause[0])
        alpha.append(clause_lst)

        n_KB = int(fin.readline())
        KB = []
        for _ in range(n_KB):
            tmp=fin.readline().replace('OR', '').rstrip('\n').split(' ')
            
            clause = list(filter(None,tmp))
            KB.append(clause)

    return alpha, KB
    


def trim(sentence):
    """
    step 1:remove duplicate
    step 2:sort Alphabel
    """
    i = 0
    for i in range(len(sentence)-1):
        j = i+1
        while(j < len(sentence)):
            if sentence[i] == sentence[j]:
                del sentence[j]
                j -= 1
                i -= 1
            j += 1
        
   
    if len(sentence) != 1:
        for i in range(len(sentence) - 1):
            for j in range(i + 1, len(sentence)):
                if sentence[i][-1] > sentence[j][-1]:
                    sentence[i], sentence[j] = sentence[j], sentence[i]
    return sentence

def removeRedundate(clause):
    #
    for literal in clause:
        if ConvertNegative(literal) in clause:
            return True
    return False

def string_convert(clause):
    
    tempSt = ''
    for i in range(len(clause)-1):
        tempSt += clause[i]+' OR '

    tempSt += clause[-1]+'\n'

    return tempSt

def resolve(clause_A, clause_B):
    """
    :param clause_a: clause
    :param clause_b: clause
    :return: res as resolved clause of 2 param
    """
    a = copy.deepcopy(clause_A)
    b = copy.deepcopy(clause_B)
    if (len(a) == 1 and len(b)==1):
        if a[0] == ConvertNegative(b[0]):
            return "{}"

    for literal in clause_A:
        if ConvertNegative(literal) in clause_B:
            
            a.remove(literal)
            b.remove(ConvertNegative(literal))
            result = a + b
            return list(set(result))

    return []

def PL_Resolution(non_alpha, KB, oFile):
    with open(oFile,'w') as f:
        clause=KB
        for c in non_alpha:
            clause.append(c)
        entailed=False
        string_W=''

        while True:
            lists=[]
            num=0

            for i in range(len(clause)-1):
                for j in range(i+1,len(clause)):
                    sentence =resolve(clause[i],clause[j])
                    sentence =trim(sentence)
                    
                    if sentence =='{}':
                        entailed=True
                    if sentence==[] or (sentence in lists) or sentence in clause or removeRedundate(sentence):
                        continue
                    if len(sentence)!=0 and sentence not in clause and sentence not in lists:
                        print('\tResolve',clause[i],'with',clause[j],'get',sentence)
                        num=num+1
                        lists.append(sentence)
                        string_W += string_convert(sentence) if sentence != '{}' else '{}\n'

            string_W=str(num)+'\n'+string_W
            f.write(string_W)

            if lists == []:  # Can not resolve new clause
                string_W += "0\nNO"
                f.write("NO")
                return False
            elif entailed:
                string_W += "\nYES"
                f.write("YES")
                return True

            clause += lists  # Add new clause to KB
            



def main():
    print('Enter your file name input:')
    input_file = input()

    output_file = 'output.txt'
    
    not_alpha, KB = readFile(input_file)
    print(f'[!] Finished read file {input_file}')
    print('[*] KB:', KB)

    print('[*] NOT alpha:', not_alpha)
    p = PL_Resolution(not_alpha, KB, output_file)
    if p:
        print("[+] KB entails alpha.")
    else:
        print("[-] KB does not entail alpha.")
    print(f"[!] Finished write to {output_file}.")


if __name__ == "__main__":
    main()
