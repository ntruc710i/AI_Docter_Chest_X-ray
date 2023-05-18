import numpy as np
from tensorflow import keras

class Covid19ChestXrayDetection():

    def __init__(self):
        self.model = keras.models.load_model('./model/Covid19_model5.h5')
        self.IMAGE_SIZE = 128
  
    def predict(self,image):

        labels = ['NORMAL', 'TUBERCULOSIS', 'PNEUMONIA', 'COVID19']
        image = np.array(image)
        image = image/image.max()
        image = image.reshape(-1,self.IMAGE_SIZE,self.IMAGE_SIZE,3)
        probabilities = self.model.predict(image).reshape(-1)
        print(probabilities)
        pred = labels[np.argmax(probabilities)]
        lbresults = []
        for i in range(len(labels)):
            lbresults.append("{}: {:.2%}".format(labels[i], probabilities[i]))
        return pred, lbresults