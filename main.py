import os
from requests import Request, Session, packages
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ContentDecodingError, RequestException, HTTPError, ConnectionError, Timeout
from datetime import datetime
from logging import basicConfig, info, error, INFO

packages.urllib3.disable_warnings(InsecureRequestWarning)


def send_image():
    try:
        request = Request(
            'POST',
            endpoint,
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
            print(json_response)
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


if __name__ == '__main__':
    basicConfig(filename='log.txt',
                filemode='a',
                format='%(asctime)s %(message)s',
                datefmt='%H:%M:%S',
                level=INFO)
    info("---start log---")

    file_path = 'C:\\Users\\LENOVO\\PycharmProjects\\facedetection\\laki.jpg'
    file_name = os.path.basename(file_path)
    endpoint = 'http://localhost:8080/api/upload/'

    send_image()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
