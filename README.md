# Latin Vowel Length Classifier

Since vowel length in Classical Latin is phonemic, Latin vowel length 
annotation efforts to date rely on dictionary lookup, with the 
exception of a small number of rules of thumb.
In this squib, I explore the possibility of predicting the length of Latin 
syllable nuclei based only on phonological features available from the 
orthography, without recourse to a dictionary. 
I show that a simple machine learning classifier is able to score remarkably 
well on this task, showing that Latin vowel length is in fact predictable 
for 95% of previous seen and 89% of unseen syllables. 
Further, by using interpretable machine learning architectures in the form of 
decision trees, random forests and (structured) perceptron, we can extract 
the linguistic features judged most predictive for the task.

Special thanks to Kevin Ryan for sharing his compiled dataset of Latin text
annotated with macrons.

## How to run

This project uses Anaconda to manage dependencies. Clone this repository, then use
```
conda env create -f environment.yml
```
to install the dependencies. Activate your new conda environment with
```
conda activate latin-vowel-classifier
```

If the `/data` folder only contains `Ryan_Latin_master.txt`,  run
```
python preprocess.py
```
to create the two corpus files `Latin_words_preprocessed.txt` and `Latin_words_preprocessed_unique.txt`. 

Then run `model.py` to train and evaluate a model:
```
python model.py
```
Various variables can be set in `model.py`,
including the type of classifier, its 
hyperparameters, which features to use, and whether or not to plot the tree 
(only applicable for a decision tree). These are set in the main body of the script.
Tree plotting options can be changed in the `plot_fitted_tree()` method.
Logs will be output both to the console and to a log file under `/experiments`
with the current timestamp.

## Unit tests

Unit tests for syllabification are contained in `test_syllabify.py`. 
The file `test_syllabify_corpus.py` contains an integration test which checks
that the entire corpus can be syllabified without errors.