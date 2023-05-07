import os

from flask import Flask, send_from_directory, request, Response, jsonify
from fer import FER
#from fer import Video
import matplotlib.pyplot as plt
import cv2
import numpy as np
import base64


# def process_video(videofile):
#     # Face detection
#     detector = FER(mtcnn=True)
#     # Video predictions
#     video = Video(videofile)
#     # Output list of dictionaries
#     raw_data = video.analyze(detector, display=False)


app = Flask(__name__, static_folder='/build')
app.debug=True

# Crea el detector de emociones.
emo_detector = FER(mtcnn=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    print("Serving app")
    if path != "" and os.path.exists("build/" + path):
        return send_from_directory('build', path)
    else:
        return send_from_directory('build', 'index.html')

@app.route('/detect_emotions', methods=['POST'])
def detect_emotions():
    print("Running emotion detection")
    # Obtiene el archivo de imagen del objeto de solicitud.
    file = request.files['image']
    # Lee la imagen del archivo.
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Detecta las emociones en la imagen.
    result = emo_detector.detect_emotions(img)
    # Dibuja los cuadros de las caras y las emociones detectadas en la imagen.
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    for faceid in range(len(result)):
        bounding_box = result[faceid]["box"]
        emotions = result[faceid]["emotions"]
        cv2.rectangle(img, (
            bounding_box[0], bounding_box[1]), (
                          bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                      (0, 155, 255), 2, )

        for index, (emotion_name, score) in enumerate(emotions.items()):
            color = (211, 211, 211) if score < 0.01 else (255, 0, 0)
            emotion_score = "{}: {}".format(emotion_name, "{:.2f}".format(score))

            cv2.putText(img, emotion_score,
                    (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + index * 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA, )

    # Convierte la imagen de vuelta a RGB.
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Convierte la imagen en bytes para enviarla como respuesta.
    _, img_encoded = cv2.imencode('.jpeg', img)

   #_, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #image_base64 = base64.b64encode(buffer).decode('utf-8')
    #return Response(image_base64, mimetype='image/jpeg')



    response = img_encoded.tobytes()

    # Codificar los bytes en formato base64
    encoded_data = base64.b64encode(response)

    # Convertir el resultado a una cadena str
    encoded_str = encoded_data.decode('utf-8')
    # Devuelve la imagen en la respuesta.
    return response
    #return jsonify({'image': encoded_str})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

""" if __name__ == '__main__':
    #process_video("images/video1.mp4")
    #exit(0)
    img = plt.imread("images/farmacia1.jpeg")
    emo_detector = FER(mtcnn=True)
    # Capture all the emotions on the image
    result = emo_detector.detect_emotions(img)
    # Print all captured emotions with the image
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    for faceid in range(len(result)):
        bounding_box = result[faceid]["box"]
        emotions = result[faceid]["emotions"]
        cv2.rectangle(img, (
            bounding_box[0], bounding_box[1]), (
                          bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                      (0, 155, 255), 2, )

        for index, (emotion_name, score) in enumerate(emotions.items()):
            color = (211, 211, 211) if score < 0.01 else (255, 0, 0)
            emotion_score = "{}: {}".format(emotion_name, "{:.2f}".format(score))

            cv2.putText(img, emotion_score,
                    (bounding_box[0], bounding_box[1] + bounding_box[3] + 30 + index * 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA, )

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgplot = plt.imshow(img)
    # Display Output Image
    plt.show()
    print(result[faceid]["emotions"]) """

