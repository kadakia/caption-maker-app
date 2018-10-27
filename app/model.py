# from pickle import load
import numpy as np
# from keras.applications.vgg16 import VGG16, preprocess_input
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.image import load_img, img_to_array
from keras.preprocessing.text import Tokenizer
from keras.models import Model # load_model

def extract_features_2(filename):
    """Extract features for just one photo, unlike extract_features"""
    # instantiate ResNet CNN model
    model = ResNet50()
    model.layers.pop()
    model = Model(inputs = model.inputs, outputs = model.layers[-1].output) # not strictly necessary
    
    # reshape image before passing through pretrained ResNet model
    image = load_img(filename, target_size=(224,224))
    image = img_to_array(image)
    image = image.reshape((1,image.shape[0],image.shape[1],image.shape[2]))
    image = preprocess_input(image)
    
    features_2 = model.predict(image, verbose = 0) # the prediction is a vector with 2048 components
    return features_2

def word_from_id(integer, tokenizer):
    """Convert integer (value) to corresponding vocabulary word (key) using tokenizer.word_index dictionary"""
    for word, index in tokenizer.word_index.items():
        if index == integer:            
            return word
    return None

def generate_caption(model, photo, tokenizer, max_length):
    """Given a photo feature vector, generate a caption word by word, recursively"""
    # caption begins with "startseq"
    in_text = 'startseq'
    # iterate over maximum potential length of caption
    for i in range(max_length):
        # encode in_text using tokenizer.word_index
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad this sequence so that its length is max_length = 34
        sequence = pad_sequences([sequence], maxlen = max_length)
        # predict next word in the sequence; y_vec is vector of probabilities with 7579 components
        y_vec = model.predict([photo,sequence], verbose = 0)
        # backend.clear_session()
        # pick out the position of the word with greatest probability
        y_int = np.argmax(y_vec)
        # convert this position into English word by means of the function we just wrote
        word = word_from_id(y_int, tokenizer)
        if word is None:
            break
        # recursion: append word as input for generating the next word
        in_text += ' ' + word
        if word == 'endseq':
            break
    in_text = in_text.split()
    in_text = ' '.join(in_text[1:-1])
    return in_text