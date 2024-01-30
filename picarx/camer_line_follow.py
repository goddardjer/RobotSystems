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

        # Define range for value channel
        lower_val = np.array([0, 0, 0])
        upper_val = np.array([180, 255, 100])

        # Threshold the HSV image to get only desired colors
        mask = cv2.inRange(hsv, lower_val, upper_val)

        # Bitwise-AND mask and original image
        frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Preprocess the frame (e.g., convert to grayscale, apply filters)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # Apply image processing techniques to detect the line
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
        # cv2.imshow('Frame', frame)
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
    control_picarx(car)