# -*- coding: utf-8 -*-
"""
Program Details: It compares the output of tagger-test to the gold standard key data (pos-key.txt) and report overall 
                tagging accuracy and also provide information equivalent to what you find in a confusion matrix in the following format :
                PREDICT_TAG KEY_TAG : count     
                
Code Usage: The user should follow below format in a commandline 
            tagger-eval.py pos-key.txt post-test-0/1.txt > pos-test-0/1-eval.txt
            where, tagger-eval.py = Name of the program
                   pos-key.txt = gold standard key tag
                   post-test-0/1.txt = output predicted file
                   pos-test-0/1-eval.txt = confusion matrix
                   
Program Algorithm: (Eval)
                1) Create a list with gold standard key tag. Format: word tag
                2) Create a list with predicted key tag. Format word tag
                3) For each item of predicted list:
                    3.1) compare the words of predicted and gold key standard
                        3.1.1) if match (Must match. Still checking) add to a dictionary where value = (predict_tag, key_tag), value = count
                        3.1.2) print an error message
                4) print the dictionry with below format: Predicted_tag Actual_tag : count

"""
#import Libraries
import argparse
import sys

# open file and make a list
def make_dic(filename):
    with open(filename, encoding='utf-8') as file:
        
       lst = [] 
       for line in file:
           line = line.rstrip() # To remove the new line
           x = line.rfind('/') # Separate the word and tag
           word = line[0:x].strip()
           #word = word.lower()
           tag = line[x+1:].strip()
           lst.append([word,tag])
           
    return lst

# Create a dictionary based on predicted and actual tag matching
def eval_dic(pred_list,eval_list):

    for i in range(len(pred_list)):
        a = (pred_list[i][0]).rstrip().strip() # Word of Predicted list
        b = (eval_list[i][0]).rstrip().strip() # Word of Actual list
        
 #3.1.1) if match (Must match. Still checking) add to a dictionary where value = (predict_tag, key_tag), value = count        
        if a == b: # If both words match
            eval_tuple = tuple([pred_list[i][1],eval_list[i][1]]) # Create a tuple (predicted_tag, Actual_tag)
                       
            if eval_tuple not in result_dic:
                result_dic[eval_tuple] = 1 # Add tuple to the dictionary with frequency count
            else:
                result_dic[eval_tuple] = result_dic[eval_tuple] +1
                
        else:
            print("The word doesn't match")

# Print the dictionary and find the accuracy
def print_result(result_dic):
    
    acurate = 0
    total = sum(result_dic.values())
    for item in result_dic.keys():

        if item[0] == item [1]: # if both tag match, then accurate
            acurate = acurate + result_dic[item]
    
    print("Accuracy = ", acurate/total)

    # Print the dictionary. Format: Predicted_tag Actual_tag : count
    # Sorted on PREDICT_TAG and then KEY_TAG in ascending alphabetic order
    sorted_dic = dict(sorted(result_dic.items(), key=lambda item: (item[0][0],item[0][1]))) 
    
#4) print the dictionry with below format: Predicted_tag Actual_tag : count
    for val in sorted_dic:
        print(val[0],val[1],':',sorted_dic[val])    
            
result_dic = {}

if __name__ == "__main__":

    # Parser to create command line arguments.
    parser = argparse.ArgumentParser(description='Eval Program of POS tagging.') # This is the description
    parser.add_argument('Eval', type = str,help='The name of the test file')  # Output File selection
    parser.add_argument('Predict', type = str,help='The name of the Probability file')  # Input File selection
    args = parser.parse_args()
    
    if args.Predict and args.Eval:
        if args.Predict == 'pos-test-0.txt': # For Mode 0
            sys.stdout = open('pos-test-0-eval.txt', "w", encoding = 'utf8') # Open output file to write
#1) Create a list with gold standard key tag. Format: word tag
            pred_list = make_dic(args.Predict)
#2) Create a list with predicted key tag. Format word tag
            eval_list = make_dic(args.Eval)
            eval_dic(pred_list,eval_list)
            print_result(result_dic)
            sys.stdout.close()
            
        elif args.Predict == 'pos-test-1.txt': #For mode 1
            sys.stdout = open('pos-test-1-eval.txt', "w", encoding = 'utf8') # Open output file to write
            pred_list = make_dic(args.Predict)
            eval_list = make_dic(args.Eval)
            eval_dic(pred_list,eval_list)
            print_result(result_dic)
            sys.stdout.close()
            
        else:
            print("Provide Correct file name")
