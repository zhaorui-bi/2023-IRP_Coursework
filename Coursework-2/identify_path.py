from typing import Tuple

import cv2
import numpy as np

# Define image dimensions and blue color range
image_width = 640
image_height = 480
lower_blue = np.array([100, 35, 45])
upper_blue = np.array([125, 255, 255])
center_x = image_width // 2
center_y = image_height
h_mean_x = 320
h_mean_y = 240
angle = 0
left = False
right = False
up = False
stop = False
kind = " "


def calculate_angle(v1) -> int:
    """ This function takes in one vector,
        it returns the angle in degree.
    """
    # set vector
    v = np.array([0, 1])

    # Calculate dot product
    dot_product = np.dot(v1, v)

    # Calculate vector lengths
    length_v1 = np.linalg.norm(v1)
    length_v = np.linalg.norm(v)

    # Calculate angle between vectors
    angle_rad = np.arccos(dot_product / (length_v1 * length_v))
    if v1[1] < 0:
        angle_deg = abs(180 - np.rad2deg(angle_rad))
    else:
        angle_deg = -np.rad2deg(angle_rad)

    return angle_deg


def find_intersection(x1, y1, a, x2, y2, b, epsilon=1e-9) -> (int, int):
    """ This function takes in two lines' variables,
        it returns the (x_intersection, y_intersection).
    """
    # Check if the lines are parallel
    if abs(a - b) < epsilon:
        # or any other value indicating no intersection
        return None

    # Calculate the intersection point
    c1 = y1 - a * x1
    c2 = y2 - b * x2
    x_intersection = (c2 - c1) / (a - b)
    y_intersection = a * x_intersection + c1

    return x_intersection, y_intersection


def calculate_x(x1, y1, a, y2) -> int:
    """ This function takes one line and y point,
        it returns x point.
    """
    if a == 0:
        return x1
    elif a > 999999:
        return x1
    else:
        return int((y2 - y1) / a + x1)


def calculate_y(x1, y1, a, x2) -> int:
    """ This function takes in one line and x point,
        it returns y point.
    """
    if a == 0:
        return y1
    elif a > 999999:
        return y1
    else:
        return int(a * (x2 - x1) + y1)


def get_lines(frame, lines) -> (int, int):
    """ This function takes in a frame and existing lines,
        it returns updated lines and the length of lines.
    """
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for blue color range
    mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)

    # Erode the mask
    mask = cv2.erode(mask, None, iterations= 2)

    # Dilate the mask
    mask = cv2.dilate(mask, None,  iterations= 2)

    # Apply the mask to the frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert the result to grayscale
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur and bilateral filter to reduce noise
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Detect edges using Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Apply Hough line transform to detect lines
    edge = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=10)

    # If any lines are detected, add them to the existing lines
    if edge is not None:
        for eg in edge:
            lines.append(eg)

    # Return the updated lines and the length of lines
    return lines, len(lines)


def display_image(frame, lines) -> (bool, bool, bool, bool):
    """ This function takes in frame and lines,
        it shows the image.
    """
    global h_mean_x
    global h_mean_y
    global left
    global right
    global up
    global stop
    global angle
    paths_info = []

    if lines is not None:
        v_beg = True
        h_beg = True
        v_count = 0
        h_count = 0
        count = 0
        last_x = h_mean_x
        last_y = h_mean_y
        left_point_x = 640
        right_point_x = 0
        up_point_y = 480
        v_mean_x, v_mean_y, v_slope, h_mean_x, h_mean_y, h_slope, mean_v_angle, mean_h_angle, main = 0, 0, 0, 0, 0, 0, 0, 0, 0

        for line in lines:
            count += 1
            x1, y1, x2, y2 = line[0]
            slope = (y2 - y1) / (x2 - x1)

            # Calculate angle from line coordinates
            v1 = np.array([(x2 - x1), (y2 - y1)])
            angle = calculate_angle(v1)

            # Check if it's the first vertical line and angle meets a condition
            if v_beg and abs(angle) < 42:
                mean_v_angle = angle
                main = angle
                v_slope = slope
                v_mean_x = (x1 + x2) // 2
                v_mean_y = (y1 + y2) // 2
                up_point_y = min(y1, y2)
                v_beg = False

            # Check if it's the first horizontal line and angle meets a condition
            if h_beg and abs(angle) > 42:
                mean_h_angle = angle
                h_slope = slope
                h_mean_x = (x1 + x2) // 2
                h_mean_y = (y1 + y2) // 2
                left_point_x = min(x1, x2)
                h_beg = False

            # Update variables if angle is close to main angle and not the first vertical line
            if abs(main - angle) < 10 and ~v_beg:
                if up_point_y > min(y1, y2):
                    up_point_y = min(y1, y2)
                mean_v_angle = (mean_v_angle + angle) // 2
                v_slope = 0.5 * (slope + v_slope)
                v_mean_x = (v_mean_x + (x1 + x2) // 2) // 2
                v_mean_y = (v_mean_y + (y1 + y2) // 2) // 2
                v_count += 1

            # Update variables if angle is significantly different from main angle or not the first horizontal line
            elif abs(main - angle) > 50 or ~h_beg:
                # print(min(x1, x2))
                if left_point_x > min(x1, x2):
                    left_point_x = min(x1, x2)
                if right_point_x < max(x1, x2):
                    right_point_x = max(x1, x2)
                mean_h_angle = (mean_h_angle + angle) // 2
                h_slope = 0.5 * (slope + h_slope)
                h_mean_x = (h_mean_x + (x1 + x2) // 2) // 2
                h_mean_y = (h_mean_y + (y1 + y2) // 2) // 2
                h_count += 1

        # print("count: " + str(count))
        # print("v_count: "+str(v_count))
        # print("h_count: "+str(h_count))

        joint = True
        # Check if the intersection of two lines exists
        if find_intersection(v_mean_x, v_mean_y, v_slope, h_mean_x, h_mean_y, h_slope) is not None:
            # If intersection exists, get the coordinates
            cross_x, cross_y = find_intersection(v_mean_x, v_mean_y, v_slope, h_mean_x, h_mean_y, h_slope)
            # Check if the intersection point is within the frame boundaries
            if 0 < cross_x < 640 and 0 < cross_y < 480:
                # Draw a circle at the intersection point
                cross_x, cross_y = int(cross_x), int(cross_y)
                cv2.circle(frame, (cross_x, cross_y), 5, (0, 255, 0),
                           -1)  # 5 is the radius, (0, 255, 0) is the color, -1 fills the whole circle
        else:
            cross_x, cross_y = last_x, last_y
            joint = False

        left = False
        right = False
        up = False
        stop = False
        straight = True
        # Initialize path information dictionary
        path_info = {"path": "", "angle": mean_v_angle, "offset": 480 - cross_y}

        # Check for different movement options based on the intersection and line positions
        if joint and (cross_x - left_point_x > 150):
            path_info["path"] = "Turn left"
            # print("turn left")
            straight = False
            # Draw a line and display text for turning left
            if 0 < cross_x < 640 and 0 < cross_y < 480:
                cross_x, cross_y = int(cross_x), int(cross_y)
                cv2.line(frame, (left_point_x, calculate_y(cross_x, cross_y, h_slope, left_point_x)),
                         (cross_x, cross_y), (255, 0, 255), 2)
            cv2.putText(frame, "turn left", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(frame, f"Left: {mean_v_angle - 90:.2f}", (60, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255),
                        2)
            left = True
        if joint and (right_point_x - cross_x > 150):
            # Check for turning right
            path_info["path"] = "Turn right"
            # print("turn right")
            straight = False
            # Draw a line and display text for turning right
            if 0 < cross_x < 640 and 0 < cross_y < 480:
                cross_x, cross_y = int(cross_x), int(cross_y)
                cv2.line(frame, (right_point_x, calculate_y(cross_x, cross_y, h_slope, right_point_x)),
                         (cross_x, cross_y), (0, 255, 255), 2)
            cv2.putText(frame, "turn right", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, f"Right: {mean_v_angle + 90:.2f}", (500, 240), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            right = True
        if joint and (cross_y - up_point_y > 150) and 480 - up_point_y > 150:
            # Check for going straight
            path_info["path"] = "Go straight"
            print("go straight")
            # Draw a line and display text for going straight
            if 0 < cross_x < 640 and 0 < cross_y < 480:
                cross_x, cross_y = int(cross_x), int(cross_y)
                cv2.line(frame, (calculate_x(cross_x, cross_y, v_slope, up_point_y), up_point_y), (cross_x, cross_y),
                         (80, 100, 255), 2)
            cv2.putText(frame, "go straight", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            up = True
        elif ~joint and straight and (480 - up_point_y > 150):
            # Check for going straight if there is no intersection
            path_info["path"] = "Go straight"
            # print("go straight")
            path_info["offset"] = 480 - up_point_y
            cv2.circle(frame, (calculate_x(v_mean_x, v_mean_y, v_slope, up_point_y), up_point_y), 5, (0, 255, 0), -1)
            cv2.putText(frame, "go straight", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        elif ~joint and (480 - up_point_y < 150):
            # Consider stopping if there is no intersection and the offset is less than 150
            path_info["offset"] = 480 - up_point_y
            cv2.circle(frame, (calculate_x(v_mean_x, v_mean_y, v_slope, up_point_y), up_point_y), 5, (0, 255, 0), -1)
            cv2.putText(frame, "Stop", (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            stop = True

        # Append path information to the list
        paths_info.append(path_info)

        # Display distance and vertical angle information on the frame
        if len(paths_info) > 0:
            distance_text = f"Distance: {paths_info[0]['offset']}"
            vertical_angle_text = f"Vertical Angle: {paths_info[0]['angle']:.2f}"
            cv2.putText(frame, distance_text, (frame.shape[1] - 150, image_height - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, vertical_angle_text, (frame.shape[1], image_height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame,f"Line angle: {angle:.2f}", (10, image_height - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # cv2.line(frame, (320, 0), (320, 480), (0, 0, 255), 2)
        # Return movement flags and information
        return left, right, up, stop


def process_video():
    """ This function takes in name(String) and image,
        it shows the image.
    """
    global left
    global right
    global up
    global stop
    global kind

    # Create a VideoCapture object to capture video from the camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height)

    # Variables to count the number of consecutive frames with certain path directions
    left_cnt, right_cnt, up_cnt, stop_cnt, cnt = 0, 0, 0, 0, 0

    while True:
        # Read a frame from the video stream
        ret, frame = cap.read()

        if not ret:
            break

        count = 0
        lines = []

        # Collect lines from multiple frames for better accuracy
        while count < 20:
            lines, _ = get_lines(frame, lines)
            count += 1

        # Display the processed image and retrieve path information
        l, r, u, s = display_image(frame, lines)

        # Reset path direction flags
        left, right, up, stop = False, False, False, False

        # Count consecutive frames with certain path directions to determine the final path
        if l:
            left_cnt += 1
            if left_cnt > 3:
                left = True
        if r:
            right_cnt += 1
            if right_cnt > 3:
                right = True
        if u:
            up_cnt += 1
            if up_cnt > 5:
                up = True
        if s:
            stop_cnt += 1
            if stop_cnt > 5:
                stop = True

        if cnt >= 10:
            cnt = 0
            if left and right and up:
                kind = "Crossroads"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif left and right:
                kind = "Terminating T-junction"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif up and right:
                kind = "Right T-junction"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif left and up:
                kind = "Left T-junction"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif left:
                kind = "Left Corner"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif right:
                kind = "Right Corner"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            elif stop:
                kind = " "
                left_cnt, right_cnt, up_cnt = 0, 0, 0
            else:
                kind = "Straight Line"
                left_cnt, right_cnt, up_cnt = 0, 0, 0
        cnt += 1

        # Display the path information on the frame
        cv2.putText(frame, kind, (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (240, 0, 200), 2)

        # Show the frame with path information
        cv2.imshow('Path Detection', frame)

        # Check for key press to exit the loop
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
