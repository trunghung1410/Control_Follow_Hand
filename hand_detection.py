import time

import cv2
import datetime
import argparse
import imutils
from imutils.video import VideoStream

from utils import detector_utils as detector_utils

ap = argparse.ArgumentParser()
ap.add_argument('-d', '--display', dest='display', type=int,
                        default=1, help='Display the detected images using OpenCV. This reduces FPS')
args = vars(ap.parse_args())

detection_graph, sess = detector_utils.load_inference_graph()

if __name__ == '__main__':
    c1 = 0
    c2 = 0
    # Detection confidence threshold to draw bounding box
    score_thresh = 0.60

    # Get stream from webcam and set parameters)
    vs = VideoStream().start()

    # max number of hands we want to detect/track
    num_hands_detect = 1

    # Used to calculate fps
    start_time = datetime.datetime.now()
    num_frames = 0

    im_height, im_width = (None, None)

    try:
        while True:
            # Read Frame and process
            frame = vs.read()
            frame = cv2.resize(frame, (400, 300))

            if im_height == None:
                im_height, im_width = frame.shape[:2]

            # Convert image to rgb since opencv loads images in bgr, if not accuracy will decrease
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                print("Error converting to RGB")

            # Run image through tensorflow graph
            boxes, scores, classes = detector_utils.detect_objects(
                frame, detection_graph, sess)

            # Draw bounding boxeses and text
            detector_utils.draw_box_on_image(
                num_hands_detect, score_thresh, scores, boxes, classes, im_width, im_height, frame)

            # Calculate Frames per second (FPS)
            num_frames += 1
            elapsed_time = (datetime.datetime.now() -
                            start_time).total_seconds()
            fps = num_frames / elapsed_time

            if args['display']:
                # Display FPS on frame
                detector_utils.draw_text_on_image("FPS : " + str("{0:.2f}".format(fps)), frame)
                cv2.imshow('Detection', cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    vs.stop()
                    break


            # Cách 3:
            # Quay trái phải trước rồi mới tiến lùi
            b1 = detector_utils.control_right_left(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)
            b2 = detector_utils.control_up_back(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)

            #Khởi đầu:
            if b1 == 0 and c1 == 0:
                if b2 == 0:
                    print("Dừng")
                    c1 = 1
                if b2 == 1:
                    print("Tiến")
                    c1 = 2
                if b2 == 2:
                    print("Lùi")
                    c1 = 3
            if b1 == 1 and c1 == 0:
                print("Phải")
                c1 = 4
            if b1 == 2 and c1 == 0:
                print("Trái")
                c1 = 5

            # Từ giữa ra 2 bên
            if c1 == 1 and b1 == 0:
                if b2 == 1:
                    print("Tiến")
                    c1 = 2
                if b2 == 2:
                    print("Lùi")
                    c1 = 3
            if c1 == 2 and b1 == 0:
                if b2 == 0:
                    print("Dừng")
                    c1 = 1
                if b2 == 2:
                    print("Lùi")
                    c1 = 3
            if c1 == 3 and b1 == 0:
                if b2 == 0:
                    print("Dừng")
                    c1 = 1
                if b2 == 1:
                    print("Tiến")
                    c1 = 2

            if c1 == 1 and b1 == 1:
                print("Phải")
                c1 = 4
            if c1 == 1 and b1 == 2:
                print("Trái")
                c1 = 5

            if c1 == 2 and b1 == 1:
                print("Phải")
                c1 = 4
            if c1 == 2 and b1 == 2:
                print("Trái")
                c1 = 5

            if c1 == 3 and b1 == 1:
                print("Phải")
                c1 = 4
            if c1 == 3 and b1 == 2:
                print("Trái")
                c1 = 5

            #Từ Phải vào giữa

            if c1 == 4 and b1 == 0:
                if b2 == 0:
                    print("Dừng")
                    c1 = 1
                if b2 == 1:
                    print("Tiến")
                    c1 = 2
                if b2 == 2:
                    print("Lùi")
                    c1 = 3
            if c1 == 5 and b1 == 0:
                if b2 == 0:
                    print("Dừng")
                    c1 = 1
                if b2 == 1:
                    print("Tiến")
                    c1 = 2
                if b2 == 2:
                    print("Lùi")
                    c1 = 3


            # # Cách 2:
            # b1 = detector_utils.control_right_left(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)
            # b2 = detector_utils.control_up_back(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)
            # if b1 == 0:
            #     if b2 == 0:
            #         print("Giua")
            #     if b2 == 1:
            #         print("Tien")
            #     if b2 == 2:
            #         print("Lui")
            # if b1 == 1:
            #     if b2 == 0:
            #         print("Sang Phai")
            #     if b2 == 1:
            #         print("Tien - Phai")
            #     if b2 == 2:
            #         print("Lui - Phai")
            # if b1 == 2:
            #     if b2 == 0:
            #         print("Sang Trai")
            #     if b2 == 1:
            #         print("Tien - Trai")
            #     if b2 == 2:
            #         print("Lui - Trai")





            # Cách 1:
            # # Di chuyển trái phải
            # # Biến b1 để xét xem xe sang trái hay phải
            # b1 = detector_utils.control_right_left(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)
            #
            # if b1 == 0:
            #     if c1 != 0:
            #         print("Dung1")
            #         c1 = 0
            # else:
            #     if c1 == 0:
            #         if b1 == 2:
            #             print("Trai")
            #             c1 += 1
            #         if b1 == 1:
            #             print("Phai")
            #
            #             c1 += 1
            #
            # # Di chuyển tiến lùi
            # # Biến b2 để xét xem xe di chuyển tiến hay lùi
            # b2 = detector_utils.control_up_back(num_hands_detect, score_thresh, scores, boxes, im_width, im_height)
            # if b2 == 0:
            #     if c2 != 0:
            #         print("Dung2")
            #         c2 = 0
            # else:
            #     if c2 == 0:
            #         if b2 == 2:
            #             print("Lui")
            #             c2 += 1
            #         if b2 == 1:
            #             print("Tien")
            #             c2 += 1
        print("Average FPS: ", str("{0:.2f}".format(fps)))

    except KeyboardInterrupt:
        print("Average FPS: ", str("{0:.2f}".format(fps)))
