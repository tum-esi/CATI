import os
import argparse
import yolo_output_handling as yoh
from ultralytics import YOLO



    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input-Path")
    parser.add_argument("--output", required=True, help="Output-Path")
    parser.add_argument("--conf", type=float, default=0.5, help="Confidence Score Threshold")
    parser.add_argument("--save_images", action="store_true", help="Save annotated images?")
    parser.add_argument("--cuda", action="store_true", help="Use cuda?")
    
    
    args = parser.parse_args()

    model = YOLO(r"training_results/yolov10_traffic_map_1280_correct_labels_full_final/weights/best_modified.pt") 
    input_path = args.input
    output_path = args.output
    conf_threshold = args.conf
    save_images = args.save_images
    cuda = args.cuda

    output_directory_path = os.path.join(output_path, os.path.splitext(os.path.basename(input_path))[0])

    prediction = model.predict(source=input_path, save=save_images, conf=conf_threshold, project=output_directory_path, name="traffic_sign_detection", device = "cuda:0" if cuda else "cpu")

    yoh.save_results_to_json(prediction, input_path, output_directory_path, save_images, detection_type="yolov10_traffic_sign_detection")



if __name__ == "__main__":
    main()