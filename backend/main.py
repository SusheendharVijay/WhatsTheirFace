import flask
import requests
from io import BytesIO
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch 
from torchvision import datasets 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from imageio import imread


def face_embedding(request):
   
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    if request.method=="GET":
        return "Hello!"



    if request.method=="POST":
        data = request.get_json()
        downloadURL = data["downloadURL"]

        
        image = imread(downloadURL)

        device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        mtcnn = MTCNN( 
                    image_size=160,margin=0,min_face_size=20,thresholds=[0.6,0.7,0.7],factor=0.709,post_process=True,device=device)
        resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)


        aligned_image, prob = mtcnn(image,return_prob=True)
        aligned_image = aligned_image.unsqueeze(0)
        aligned_image.to(device)

        embedding = str(resnet(aligned_image).detach().cpu())







        response = flask.jsonify("download url : " + downloadURL + "embedding : " + embedding + "probability: " + prob)
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST')
        return response