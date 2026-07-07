import json
import logging
import time

import numpy as np
import requests,cv2 as opencv
from sahi import AutoDetectionModel
from sahi.predict import get_sliced_prediction

detection_model = AutoDetectionModel.from_pretrained(
    model_type='yolov8',
    model_path='ships_v4.pt', 
    confidence_threshold=0.3,
    device="cpu" 
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S"
)
logger = logging.getLogger(__name__)

while True:
    try:
        response = requests.get("http://web:8000/api/images/queue/pending/")
        response.raise_for_status()
        photo_list = response.json()

        if not photo_list:
                time.sleep(5)
                continue

        photo_id = photo_list[0]['id']
        photo_image = photo_list[0]['image']
        response_image = requests.get(photo_image)

        image_array = np.frombuffer(response_image.content, np.uint8)
        opencv_photo = opencv.imdecode(image_array, opencv.IMREAD_COLOR)

        rgb_photo = opencv.cvtColor(opencv_photo, opencv.COLOR_BGR2RGB)

        result = get_sliced_prediction(
            rgb_photo,
            detection_model,
            slice_height=640,  
            slice_width=640,      
            overlap_height_ratio=0.2, 
            overlap_width_ratio=0.2
        )

        result_list = result.object_prediction_list

        obj_list = []
        obj_number = len(result_list)

        for obj in result_list:
            obj_minx = int(obj.bbox.minx)
            obj_miny = int(obj.bbox.miny)
            obj_maxx = int(obj.bbox.maxx)
            obj_maxy = int(obj.bbox.maxy)
            obj_score_value = float(obj.score.value)
            obj_name = str(obj.category.name)

            obj_list.append({'name' : obj_name, 
                            'score_value' : obj_score_value, 
                            'minx' : obj_minx,
                            'miny' : obj_miny,
                            'maxx' : obj_maxx,
                            'maxy' : obj_maxy,
                            })

        request_package = {
            "satellite_image_source": photo_id,
            "ship_number": obj_number,
            "raw_detections": obj_list
        }

        post_response = requests.post("http://web:8000/api/detections/", json=request_package)
        post_response.raise_for_status()
        logger.info(f"success {photo_id} saved and flagged.")

    except requests.exceptions.HTTPError as err:
        logger.error(f"Error while saving photo {photo_id}. Status: {err.response.status_code}")
        time.sleep(10)

    except requests.exceptions.ConnectionError:
        logger.warning("Django API unavailable. Waiting 5 seconds..")
        time.sleep(5)
        
    except Exception as e:
        logger.critical(f"Unexpected error: {e}. Try again in 5 seconds..")
        time.sleep(5)
        
    time.sleep(2)