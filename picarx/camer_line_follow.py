# Import necessary libraries
import cv2
import picarx_improved as pixi

def control_picarx(car): 
    # Initialize the camera
    camera = cv2.VideoCapture(0)  # Use the appropriate camera index

    # Main loop
    while True:
        # Capture frame from the camera
        ret, frame = camera.read()

        # Define the region of interest (ROI)
        # This is an example, adjust the values according to your needs
        y_start = 100
        y_end = 300
        x_start = 200
        x_end = 800

        # Crop the frame
        cropped_frame = frame[y_start:y_end, x_start:x_end]

        # Preprocess the frame (e.g., convert to grayscale, apply filters)
        gray = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

        # Apply image processing techniques to detect the line
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        # Calculate the error (e.g., distance from the center of the line)
        if contours:
            M = cv2.moments(contours[0])
            if M['m00'] != 0:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                error = cx - cropped_frame.shape[1]//2

                # Control the picarx based on the error (e.g., adjust steering angle)
                steering_angles = [30, 15, 0, -15, -30]
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
        cv2.imshow('Frame', cropped_frame)
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
    wait = input("Press enter to start")
    car.forward(35)
    control_picarx(car)