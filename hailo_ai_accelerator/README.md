# CATI on Edge Devices

This folder provides a prototype of the CATI object detection model (based on YOLOv10m) for the Raspberry Pi 5 with [Hailo-8L](https://www.raspberrypi.com/products/ai-kit/). The model is available in the Hailo-specific HEF format. It is a quantized version of the [CATI object detection model](../training_results/yolov10_objects_coco_pat_25_full/weights/last.pt).

## Requirements

* **Hardare**
    * [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/)
    * [Raspberry Pi AI Kit](https://www.raspberrypi.com/documentation/accessories/ai-kit.html)
    * Raspberry Pi Camera (e.g., [Camera Module 3](https://www.raspberrypi.com/products/camera-module-3/))

* **Software**
    * We assume a fully functional Raspberry Pi AI Kit. Please follow the procedure from the Raspberry Pi homepage to [install the AI Kit](https://www.raspberrypi.com/documentation/accessories/ai-kit.html#ai-kit-installation) and [Hailo drivers for Raspberry Pi](https://www.raspberrypi.com/documentation/computers/ai.html#getting-started). Additionally:
    * [Camera software by Raspberry Pi](https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-apps)

## Getting started
1. Adapt the file path to the HEF file:
    * Open [`hailo_catiObjectDetection_inference.json`](hailo_catiObjectDetection_inference.json)
    * Navigate to line 14 and change `"hef_file": "/home/hailo_catiObjectDetection_inference_full_last.hef",` to the **absolute file path** of [`hailo_catiObjectDetection_inference_full_last.hef`](hailo_catiObjectDetection_inference_full_last.hef).
2. Make the shell script executable: `chmod +x hailo_catiObjectDetection_inference.sh`
3. Start image aquisition by executing [`./hailo_catiObjectDetection_inference.sh`](./hailo_catiObjectDetection_inference.sh)

An window with the camera image will appear and bounding boxes of detected objects are drawn. If objects are not detected immediately, please be patient, as the model might take a few seconds to be available on the Hailo accelerator.

## Further use
The HEF file ([`hailo_catiObjectDetection_inference_full_last.hef`](hailo_catiObjectDetection_inference_full_last.hef)) is compatible to other  [`rpicam-apps`](https://www.raspberrypi.com/documentation/computers/camera_software.html#rpicam-apps) to store images, videos, etc. Please use the parameter `--post-process-file` with [`hailo_catiObjectDetection_inference.json`](hailo_catiObjectDetection_inference.json) to use our model. Please refer to the official [Raspberry Pi documentation](https://www.raspberrypi.com/documentation/computers/camera_software.html#post-processing-with-rpicam-apps) for further help on post-processing files.

**Please Note:** This version of the CATI model is _not_ part of our [original work](http://dx.doi.org/10.1109/DSD67783.2025.00078). The performance will differ from the [full model](../training_results/yolov10_objects_coco_pat_25_full/weights/last.pt). It is intended as a supporting work for researchers and developers to use the features of the CATI model on an embedded edge device.

Model was originally adapted for the Hailo accelerator by Shashank Simha Mysore Ramesh.