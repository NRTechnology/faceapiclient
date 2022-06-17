import os
from requests import Request, Session, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ContentDecodingError, RequestException, HTTPError, ConnectionError, Timeout
from datetime import datetime
from logging import basicConfig, info, error, INFO
import cv2
import cvlib as cv
import time


packages.urllib3.disable_warnings(InsecureRequestWarning)


def send_image(endpoint_url, file_path):
    # file_path = 'C:\\Users\\LENOVO\\PycharmProjects\\facedetection\\laki.jpg'
    file_name = os.path.basename(file_path)

    try:
        request = Request(
            'POST',
            endpoint_url,
            files={
                'ImageFile': (file_name, open(file_path, 'rb'), 'image/jpeg', {'Expires': '0'}),
            }
        ).prepare()
    except Exception as err:
        error(err)

    json_response = None
    with Session() as s:
        try:
            response = s.send(request, verify=False)
            if response.status_code == 200 or response.status_code == 500:
                json_response = response.json()
            else:
                error('server response code not found')
            # print(json_response)
        except HTTPError as err:
            error(str(err))
        except ConnectionError as err:
            error(str(err))
        except Timeout as err:
            error(str(err))
        except ContentDecodingError as err:
            error(str(err))
        except RequestException as err:
            error(str(err))
        except TypeError as err:
            error(str(err))

        return json_response


if __name__ == '__main__':
    basicConfig(filename='log.txt',
                filemode='a',
                format='%(asctime)s %(message)s',
                datefmt='%H:%M:%S',
                level=INFO)
    info("---start log---")

    endpoint = 'http://localhost:8080/api/upload/'

    vid = cv2.VideoCapture(0)
    while (True):
        # time.sleep(1)
        # Capture the video frame
        # by frame
        ret, frame = vid.read()

        # Display the resulting frame
        face, confidence = cv.detect_face(frame)

        for idx, f in enumerate(face):
            # get corner points of face rectangle
            cv2.imwrite("face.jpg", frame)
            response = send_image(endpoint_url=endpoint, file_path='face.jpg')['message']
            if response is not None:
                label = "{}: {:.2f}%".format(response['label'], response['confidence'])

                (startX, startY) = f[0], f[1]
                (endX, endY) = f[2], f[3]

                # draw rectangle over face
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(frame, label, (startX, startY-5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 0), 2)

        cv2.imshow('frame', frame)
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

    # send_image(endpoint_url=endpoint)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
