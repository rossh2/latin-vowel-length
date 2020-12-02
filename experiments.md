# Decision Tree

Features: syllable, syllable type, ((ante)pen)ultimate
max_depth = 50

              precision    recall  f1-score   support

       short       0.86      0.95      0.90     32274
        long       0.85      0.67      0.75     14787

    accuracy                           0.86     47061
   macro avg       0.86      0.81      0.82     47061
weighted avg       0.86      0.86      0.85     47061

Feature ranking:
1. feature TYPE=VC (0.06521828883263142)
2. feature ULT (0.062416035650692966)
3. feature TYPE=CVC (0.046244352107498214)
4. feature TYPE=CVV (0.034378210276202886)
5. feature que (0.024709781747860884)
6. feature o (0.022280664764537557)
7. feature PENULT (0.021431487399845153)
8. feature non (0.020810028460263506)
9. feature TYPE=VV (0.020710981838085375)
10. feature TYPE=CLVV (0.019990851493468513)
11. feature re (0.019002396702081276)
12. feature na (0.01840142017146625)
13. feature ANTEPENULT (0.017125672744593944)
14. feature TYPE=V (0.016890214178771883)
15. feature ra (0.01646259957052485)
16. feature TYPE=CLV (0.015757799686028758)
17. feature TYPE=CV (0.015509911868944667)
18. feature is (0.012512661568476123)
19. feature os (0.012045210030221534)
20. feature tes (0.011766762232438367)
21. feature tis (0.011567267657868028)
22. feature to (0.011538542902015742)
23. feature nes (0.011349667327403456)
24. feature as (0.010595617105146843)
25. feature ma (0.01042882758435685)

# Random Forest

Features: syllable, syllable type, ((ante)pen)ultimate
max_depth = 50, n_estimators = 100

              precision    recall  f1-score   support

       short       0.82      0.97      0.89     32461
        long       0.90      0.53      0.67     14600

    accuracy                           0.84     47061
   macro avg       0.86      0.75      0.78     47061
weighted avg       0.85      0.84      0.82     47061

Feature ranking:
1. feature ULT (0.09157834944915223)
2. feature TYPE=CVV (0.05301384072254251)
3. feature PENULT (0.046917877478615706)
4. feature o (0.03866920894314346)
5. feature TYPE=CVC (0.037847624841621824)
6. feature TYPE=VC (0.037005946315262446)
7. feature ANTEPENULT (0.030016084516046572)
8. feature TYPE=CLVV (0.024366049429932434)
9. feature TYPE=CV (0.021791450669970094)
10. feature que (0.02087761361074333)
11. feature TYPE=VV (0.020116998090197766)
12. feature non (0.018624831078603438)
13. feature TYPE=CLV (0.013776396747631113)
14. feature to (0.013686390064549964)
15. feature ae (0.01306099820026396)
16. feature ro (0.012389485785852581)
17. feature tes (0.011243742470663464)
18. feature is (0.011229633677661128)
19. feature os (0.010877541924863681)
20. feature TYPE=V (0.010402227535330493)
21. feature tis (0.009595534908577492)
22. feature ta (0.009259755309795833)
23. feature nes (0.008954236286774992)
24. feature as (0.008778244406527363)
25. feature de (0.008590394754655235)

Features: syllable, syllable type, ((ante)pen)ultimate
min_samples_split=10, n_estimators=50

              precision    recall  f1-score   support

       short       0.88      0.93      0.91     32344
        long       0.83      0.72      0.77     14717

    accuracy                           0.87     47061
   macro avg       0.85      0.83      0.84     47061
weighted avg       0.86      0.87      0.86     47061

Feature ranking:
1. feature ULT (0.07301549883361744)
2. feature PENULT (0.042687217133467306)
3. feature TYPE=CVV (0.03357972933078848)
4. feature TYPE=CVC (0.0266597925021095)
5. feature ANTEPENULT (0.02263747151698124)
6. feature TYPE=VC (0.021965179915272054)
7. feature o (0.020508473526508482)
8. feature non (0.016902299993458436)
9. feature TYPE=CV (0.015807074199819443)
10. feature TYPE=VV (0.014226913259030147)
11. feature que (0.0135110544705999)
12. feature TYPE=CLVV (0.013021665838725365)
13. feature re (0.012383023704524022)
14. feature tis (0.011101472174154003)
15. feature tes (0.010647624520795216)
16. feature to (0.010557572210850933)
17. feature ti (0.01022904472093615)
18. feature ta (0.01005305498663374)
19. feature nes (0.009592165177690164)
20. feature TYPE=CLV (0.00954080761682417)
21. feature ro (0.009461264826217994)
22. feature is (0.009350402142752472)
23. feature res (0.009175504347592402)
24. feature na (0.008896811277101194)
25. feature TYPE=V (0.00866626004368503)

# Logistic Regression

Using features: {'syllable_type', 'vocab', 'antepenultimate'}
Extracted 1385 features, of which 1363 syllables in vocabulary
Hyperparameters: max_iter=1000
              precision    recall  f1-score   support

       short       0.83      0.91      0.87     32438
        long       0.75      0.60      0.67     14623

    accuracy                           0.81     47061
   macro avg       0.79      0.75      0.77     47061
weighted avg       0.81      0.81      0.81     47061

Feature ranking:
1. feature cui (7.14042010520028)
2. feature ins (6.38946007855965)
3. feature non (6.381638635775249)
4. feature pug (6.212615736909357)
5. feature que (5.956729804818907)
6. feature nul (5.859669057037156)
7. feature cons (5.657019685509451)
8. feature reg (5.471568020009741)
9. feature tos (5.429835746761356)
10. feature ras (5.408462331931875)
11. feature nun (5.263229890554984)
12. feature ens (5.111743079126196)
13. feature fir (5.049774831199065)
14. feature huic (4.967814297304138)
15. feature tec (4.888013563245636)
16. feature his (4.854944594893577)
17. feature rur (4.826420439220475)
18. feature ros (4.822845657549641)
19. feature hac (4.791091857291606)
20. feature tas (4.782189333022945)
21. feature huc (4.695550804131583)
22. feature mos (4.694968390598182)
23. feature jis (4.628592188671637)
24. feature os (4.620301751124037)
25. feature los (4.474681433214981)
