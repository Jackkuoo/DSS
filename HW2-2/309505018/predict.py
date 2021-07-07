import pandas as pd
import numpy as np 
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential, load_model

model = load_model("309505018_LSTM_2.h5")

test = pd.read_csv(f"test.csv")
testing = test["Headline"]
#print(testing.shape)
#print(testing)

tokenizer = Tokenizer(num_words=10738)
tokenizer.fit_on_texts(testing)
testing_sentences = tokenizer.texts_to_sequences(testing)
testing_padded = sequence.pad_sequences(testing_sentences,maxlen=25,padding="post",truncating="post")
#print(testing_sentences[38])
#print(testing_padded[38])
#print("testing_padded.shape: ",testing_padded.shape)


pr = model.predict(testing_padded)
pr = np.array(pr)
#print("predict.shape: ",pr.shape)
#print(pr)
f = open(f"sampleSubmission.csv","w+")
f.write('ID,Label\n')

def calaccuracy(pr):
    for i in range(227):
        ans = pr[i][0]*1.0 + pr[i][1]*1.3333 + pr[i][2]*1.5 + pr[i][3]*1.6666 + pr[i][4]*2.0 + pr[i][5]*2.3333 \
            + pr[i][6]*2.5 + pr[i][7]*2.6666 + pr[i][8]*3.0 + pr[i][9]*3.3333 + pr[i][10]*3.5 + pr[i][11]*3.6666 \
            + pr[i][12]*4.0 + pr[i][13]*4.3333 + pr[i][14]*4.5 + pr[i][15]*4.6666 + pr[i][16]*5.0

        f.write('{},{}\n'.format(i+1,ans-0.35))
        #print("i: ",i," prob: ",ans-0.3)
        ans = 0


calaccuracy(pr)

f.close()
