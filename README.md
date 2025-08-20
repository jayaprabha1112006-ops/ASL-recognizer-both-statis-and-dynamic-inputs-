American Sign Language recognition system with static image and real-time webcam input using deep learning.
To install the required modules : pip install tensorflow keras opencv-python streamlit numpy
[Download ASL Dataset from Kaggle](https://kaggle.com/your-dataset-link)

Files explanation:
Train.py-
Script to train the CNN/MobileNetV2 model on the ASL dataset.
Running this script generates the trained model file (sign.h5).

Sign_model.h5-
The trained model file created from train.py.
It is used for both static and dynamic sign recognition.

Predict_User_input.py-
Script for static image prediction.
Input: A single image of a hand gesture.
Output: The predicted ASL letter with confidence score.

Realtime_recognition.py-
Script for real-time sign recognition using webcam.
Input: Live hand gestures captured from camera.
Output: Dynamic recognition of ASL letters with interactive display.
