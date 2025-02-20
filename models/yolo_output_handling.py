import os
import json


def save_results_to_json(predictions, input_path,  output_folder, save_images, detection_type):

    """
    Writes detections results to a JSON output file. If the file already exists the detections will be added. 

    Parameters:
    predictions (list): A list of predictions, where each prediction is an object (return type of yolo.predict()).
    input_path (str): Path to the input file.
    output_folder (str): Directory where the JSON file will be saved.
    save_images (bool): Flag to determine whether the images are saved aswell or only the JSON output.
    detection_type (str): Key indicating the type of detection (e.g., "object detection", "traffic sign detection").

    Returns:
    None
    """
    
    img_name = os.path.basename(input_path)

    if not save_images:
        os.makedirs(output_folder, exist_ok=True)
        

    json_path = os.path.join(output_folder, os.path.splitext(img_name)[0] + ".json")

    if os.path.exists(json_path):
        with open(json_path, "r") as json_file:
            detections = json.load(json_file)
    else:
        detections = {}


    for prediction in predictions:

        json_boxes = json.loads(prediction.to_json())

        detections[detection_type] = json_boxes
        

    with open(json_path, "w") as output_file:
        json.dump(detections, output_file, indent=4)
