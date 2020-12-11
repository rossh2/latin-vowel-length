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