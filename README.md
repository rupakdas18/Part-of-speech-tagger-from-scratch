# Part-of-speech-tagger-from-scratch
# Training
**Program Details:** This traning function determine p(tag|word) for every word type in the training data.
It outputs these probabilities to a file named 'tagger-train-probs.txt'.
**Code Usage:** The user should follow below format in a commandline
tagger-train.py pos-train.txt > tagger-train-prob.txt
where, tagger-train.py = Name of the program
pos-train.txt = Name of the training file
tagger-train-prob.txt = output probability file
**Program Algorithm: (training)**
1) For each line of the training file
  - add to a dictionary where key = (word,tag), value = frequecy of the (word,tag)
  - add to another dictionary where key = word, value = frequency of that word
2) for each key of the dictionary
  - add to a dictionary where key = (word,tag), value = probability (count of (word,tag)/count of word)
3) Print that file

# Test
**Code Usage:** The user should follow below format in a commandline
tagger-test.py 1/0 tagger-train-prob.txt pos-test.txt > pos-test-0/1.txt
where, tagger-test.py = Name of the program
1/0 = is the mode
tagger-train-prob.txt = probability file from training program
pos-test-0/1.txt = Name of the predicted output file
**Program Algorithm: (Test)**
1) If Mode is 0:
  - For every word in test file
  - if found in the training data, assign it the POS tag with the maximum value of p(tag|word)
  - else assign it the tag 'NN' (unknown word)
2) If Mode is 1:
  - For every word in test file
    - if found in the training data, assign it the POS tag with the maximum value of p(tag|word)
      - 5 manually created rules that correct errors made by the most frequent tag mode (0) that do not involve unknown words
    - else assign it the tag 'NN' (unknown word)
      - 5 manually created rules that improve the handling of unknown words
3) Print the output in this format: 'word/tag

# Eval
**Code Usage:** The user should follow below format in a commandline
tagger-eval.py pos-key.txt post-test-0/1.txt > pos-test-0/1-eval.txt
where, tagger-eval.py = Name of the program
pos-key.txt = gold standard key tag
post-test-0/1.txt = output predicted file
pos-test-0/1-eval.txt = confusion matrix
**Program Algorithm: (Eval)**
1) Create a list with gold standard key tag. Format: word tag
2) Create a list with predicted key tag. Format word tag
3) For each item of predicted list:
  - compare the words of predicted and gold key standard
    - if match (Must match. Still checking) add to a dictionary where value = (predict_tag, key_tag), value = count
    - print an error message
4) print the dictionry with below format: Predicted_tag Actual_tag : count
