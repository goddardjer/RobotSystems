# Import necessary libraries
import cv2
import numpy as np
import picarx_improved as pixi

def control_picarx(car): 
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # Use the appropriate camera index
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    wait = input("Press enter to start")
    car.forward(35)

    # Main loop
    while True:
        # Capture frame from the camera
        ret, frame = camera.read()

        # Convert the frame to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for blue color
        lower_blue = np.array([110, 50, 50])
        upper_blue = np.array([130, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)

        # Split the image into B, G, R channels
        b, g, r = cv2.split(res)

        # Apply Gaussian blur and thresholding to each channel
        blur_b = cv2.GaussianBlur(b, (5, 5), 0)
        _, threshold_b = cv2.threshold(blur_b, 60, 255, cv2.THRESH_BINARY_INV)

        blur_g = cv2.GaussianBlur(g, (5, 5), 0)
        _, threshold_g = cv2.threshold(blur_g, 60, 255, cv2.THRESH_BINARY_INV)

        blur_r = cv2.GaussianBlur(r, (5, 5), 0)
        _, threshold_r = cv2.threshold(blur_r, 60, 255, cv2.THRESH_BINARY_INV)

        # Combine the thresholds
        threshold = cv2.merge([threshold_b, threshold_g, threshold_r])

        # Convert the merged threshold to grayscale
        threshold_gray = cv2.cvtColor(threshold, cv2.COLOR_BGR2GRAY)

        # Apply image processing techniques to detect the line
        contours, _ = cv2.findContours(threshold_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
        
        # Draw contours on the frame
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

        # Calculate the error (e.g., distance from the center of the line)
        if contours:
            M = cv2.moments(contours[0])
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                error = cx - frame.shape[1]//2

                # Control the picarx based on the error (e.g., adjust steering angle)
                steering_angles = [-30, -15, 0, 15, 30]
                if error < -512 * 0.4:
                    steering_angle = steering_angles[0]  # Left
                elif -512 * 0.4 <= error < -512 * 0.1:
                    steering_angle = steering_angles[1]  # Kinda left
                elif -512 * 0.1 <= error <= 512 * 0.1:
                    steering_angle = steering_angles[2]  # Center
                elif 512 * 0.1 < error <= 512 * 0.4:
                    steering_angle = steering_angles[3]  # Kinda right
                else:
                    steering_angle = steering_angles[4]  # Right
                
                car.set_dir_servo_angle(steering_angle)

        # Display the processed frame (optional)
        cv2.imshow('Threshold', threshold)

        # Check for exit condition (e.g., press 'q' to quit)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and clean up
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    car = pixi.Picarx()
    car.set_cam_tilt_angle(-50)
    car.set_cam_pan_angle(0)
    control_picarx(car)