## NLP - Sentence Completion 

An NLP implementation of a sentence completion with language model targeted for
customer service applications.

See demo below, and demo_nlp_sentence_completion.webm.

An auto-complete server python 2.7 realization:

### R E Q U I R E M E N T S - implementation
-------------------------------------------------------
Python implementation requires python modules,
sqlite3, kenlm, nltk

pip install requests
pip install nltk
pip install kenlm

### Sentence autocompletion:
-------------------------
consists of 4 implementation files, python implementation =>
db.py, implementation for generating sentence completions, utilizes sql dbs for
       possible utterences (sentences) and ngram (trigram) models;  generates
       scores for possible sentence completions using ngram language model

generate_completions.py, wrapper for function to 'generate_completions';
                         Usage: python generate_completions.py <key entry>
                         (satisfies Realtime Autocomplete)
                         REQUIRES language model generated by parse.py and
                         kenlm (language model)

parse.py,  creates sentence completion training file (utt.txt) from json
           training file (supplied sample_conversations.json);
	   (satisfies  Offline data processing)
           Corresponding language model (utt.arpa) generated by using 
           stdout from parse.py to 'pipe' into kenlm binary lmplz eg.
           LANGUAGE MODEL : python parse.py ./NLP\ ML\ Engineering\ ASAPP\ Challenge/sample_conversations.json ./utt.txt | ./lmplz -S 20% -o 5 > utt.arpa

webs.py,   web server to establish web server serving autocomplete GET requests
           for given port and ip (satisfies Autocomplete server) 

	   eg. python webs.py 13000 127.0.0.1 ./utt.arpa ./utt.txt
 
           curl http://localhost:13000/autocomplete?q=what


<p align="center">
  <img src="https://github.com/neils2019/nlp-sentence-completion/blob/master/sentenceCompletion_demo.gif" alt="Zappa Demo Gif"/>
</p>


### --------------------------------------------

1.) Offline data processing - create language model and sentence completion
                              (utterence) file from training json file,
                              sample_conversations.json;  
                              Files generated: './utt.txt' and './utt.arpa

    EXECUTE:
    python parse.py ./sample_conversations.json ./utt.txt | ./lmplz -S 20% -o 5 > utt.arpa

    REQUIRES : json conversation training file, kenlm binary, 'lmplz' in 
                current directory

2.) Realtime autocomplete -  perform sentence completion estimation from partial
                             words/phrases, user keystrokes.

    EXECUTE:
    python generate_completions.py "is there"

    REQUIRES : './utt.txt' and '/utt.arpa' or sentence completion training file
               and language model arpa file respectively (see Offline data processing)

3.) Autocomplete server   - realtime autocomplete in an HTTP server,GET requests
                           serviced with JSON completions

     EXECUTE:
     python webs.py 13000 127.0.0.1 ./utt.arpa ./utt.txt

     curl http://localhost:13000/autocomplete?q=what

     REQUIRES:  './utt.txt' and '/utt.arpa' or sentence completion training file
               and language model arpa file respectively (see Offline data processing)
	       