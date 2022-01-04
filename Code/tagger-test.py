# -*- coding: utf-8 -*-
"""
Program Details: This Test function operate in two modes, most frequent tag (mode 0) and most frequent tag + enhancements (mode 1)
                It outputs the predicted POS tag to a file named 'tagger-test-0/1.txt'.
                
Code Usage: The user should follow below format in a commandline 
            tagger-test.py 1/0 tagger-train-prob.txt pos-test.txt  > pos-test-0/1.txt
            where, tagger-test.py = Name of the program
                   1/0 = is the mode                   
                   tagger-train-prob.txt = probability file from training program
                   pos-test-0/1.txt = Name of the predicted output file
                   
Program Algorithm: (Test)
            1) If Mode is 0:
                1.1) For every word in test file
                    1.1.2) if found in the training data, assign it the POS tag with the maximum value of p(tag|word)
                    1.1.3) else assign it the tag 'NN' (unknown word) 

            2) If Mode is 1:
                2.1)  For every word in test file
                    2.1.1) if found in the training data, assign it the POS tag with the maximum value of p(tag|word)  
                        2.1.1.1) 5 manually created rules that correct errors made by the most frequent tag mode (0) that do not involve unknown words
                    2.1.2) else assign it the tag 'NN' (unknown word) 
                        2.1.2.1) 5 manually created rules that improve the handling of unknown words  
    
            3) Print the output in this format: 'word/tag'

"""
# Import libraries

import argparse
import sys
import re

# This function is used to predict the POS when the Mode = '0' is selected
def predict_POS_0(probfile,testfile):
    
    # Open the probability file and add add values in a list in this format: [probability, tag, word] 
    with open(probfile,encoding='utf-8') as file:        
        prob_list = []
        for line in file:
            prob_list.append([float(line.split()[0]),line.split()[1],line.split()[2]])
            
            
    with open(testfile,encoding='utf-8') as file:  
        # Open the test file
# 1.1) For every word in test file
        for pos in file: # For each value in testfile
            tem_list = [] # create a temporary list
            pos = pos.rstrip() # remove newline

            for lst in prob_list: #For each value in probability list
               if pos == lst[2]: # if the word is found in probability list
                   tem_list.append(lst) # add that list in the temporary list

# 1.1.3) else assign it the tag 'NN' (unknown word)            
            if len(tem_list) == 0: # if unknow word that means temporary list is empty
                print(pos,'/','NN') # Assign 'NN'

# 1.1.2) if found in the training data, assign it the POS tag with the maximum value of p(tag|word)                
            else: # if temporary list non-empty means known word
                temp = (max(tem_list, key=lambda x: x[0])) # find the tag with most probability
                print(pos + '/' + temp[1]) # Write the word and tag (word/tag)               
 
        
# This function is used to predict the POS when the Mode = '1' is selected 
def predict_POS_1(probfile,testfile):
    
    # Same as Mode 0
    with open(probfile,encoding='utf-8') as file:
        prob_list = []
        for line in file:
            prob_list.append([float(line.split()[0]),line.split()[1],line.split()[2]])
            
    # Same as Mode 0
    with open(testfile,encoding='utf-8') as file:  
# 2.1)  For every word in test file        
        for pos in file:
            tem_list = []
            pos = pos.rstrip()
            for lst in prob_list:
               if pos == lst[2]:
                   tem_list.append(lst)
                   
#2.1.2) else assign it the tag 'NN' (unknown word) 
#2.1.2.1) 5 manually created rules that improve the handling of unknown words                   
            if len(tem_list) == 0: # if the word is unknown       
            
                # U1: If the unknown word is numeric, tag it as CD. Example '274,963'
                if re.search(r'[0-9]+',pos):
                    print(pos + "/" + 'CD')
                    
                # U2: if found "-" between 2 words, mark it as JJ. Example: page-one     
                elif re.search(r'\b\w*[-]\w*\b',pos):
                    print(pos + "/" + 'JJ')
                    
                # U3: Normally a NNP starts with capital letter. Example: 'Erickson'   
                elif re.search(r'[A-Z]+[a-z]+$', pos):
                    print(pos + "/" + 'NNP')
                    
                # U4: Noun ends with s is a plural Noun (NNS). Example 'powders'
                elif re.search(r'\b\w+s\b', pos): 
                    print(pos + "/" + 'NNS')
                
                # U5: Word ends with 'ed' are assumed as VBD. Example: 'peppered'
                elif re.search(r'\b\w+ed\b', pos): 
                    print(pos + "/" + 'VBD')
                    
                     
                else:
                    print(pos,'/','NN')
                    
 #2.1.1) if found in the training data, assign it the POS tag with the maximum value of p(tag|word)
 #2.1.1.1) 5 manually created rules that correct errors made by the most frequent tag mode (0) that do not involve unknown words             
            else: # if the word is known
                
                temp = (max(tem_list, key=lambda x: x[0])) # find the POS with highest probability. Format [word,tag,max_probability]
                #print(temp)
                #print(type(temp[1]))
                
                
                # E1: If the word is predicted as 'JJR' but starts with a capital letter and ends with 'er', tag it with 'NNP': Example: 'Higher'
                if temp[1] == 'JJR' and re.search(r'[A-Z]+(er)$',pos):
                    print(pos+ "/" + 'NNP')
                    
                # E2: If the word is predicted as 'CD' and the numeric value ends with a 's', tag it 'NNS'. Example: '1960s'    
                elif temp[1] == 'CD' and re.search(r'[0-9]+s$', pos):
                   print(pos + "/" + 'NNS')             
                          
                # E3: If predicted RBR and word not ends with 'lier', then it is tagged with 'JJR'. Example: 'faster', but not 'earlier'
                elif temp[1] == 'RBR' and not pos.endswith('lier'):
                   print(pos + "/" + 'JJR')                
                    
                # E4: If the word is predicted as 'NNPS' and starts with Uppercase and ends with 's', tag it as 'NNP'. Example: 'Machines'
                elif temp[1] == 'NNPS' and re.search('[A-Z].+s$', pos):
                    print(pos + "/" + 'NNP') 
                    
                # E5: If the word is predicted as 'NNS' and starts with Uppercase and ends with 's', tag it as 'NNP'. Example: 'Comments'
                elif temp[1] == 'NNS' and re.search('[A-Z].+s$', pos):
                    print(pos + "/" + 'NNP')
                
                else:
                    print(pos + '/' + temp[1])       
                   
                   

if __name__ == "__main__":

    # Parser to create command line arguments.
    parser = argparse.ArgumentParser(description='Test Program of POS tagging.') # This is the description
    parser.add_argument('Mode', type = str,help='The Mode of the program')
    parser.add_argument('ProbFile', type = str,help='The name of the Probability file')  # Input File selection
    parser.add_argument('Test', type = str,help='The name of the test file')  # Output File selection
    args = parser.parse_args()
    
    if args.Mode and args.ProbFile and args.Test:
# 1) If Mode is 0:
        if args.Mode == '0':
            output_file = 'pos-test-0.txt'
            sys.stdout = open(output_file, "w", encoding = 'utf8') # Open output file to write
            predict_POS_0(args.ProbFile,args.Test)
 # 2) If Mode is 1:           
        if args.Mode == '1':
            output_file = 'pos-test-1.txt'
            sys.stdout = open(output_file, "w", encoding = 'utf8') # Open output file to write
            predict_POS_1(args.ProbFile,args.Test)
            
    sys.stdout.close() # close the output file
        
        