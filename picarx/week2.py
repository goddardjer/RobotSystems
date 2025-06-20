import picarx_improved
import time

def main():
    car = picarx_improved.Picarx()

    while True:
        user_input = input("Please enter a command (F,B,PL,PR,K,E): ")

        if user_input == 'F':
            # do something for 'F' command
            speed = int(input("Enter speed: "))
            duration = int(input("Enter time: "))
            angle = int(input("Enter angle: "))
            car.Manuevering_fwd_at_angle(speed, duration, angle)
            # car.set_dir_servo_angle(angle)
            # car.forward(speed)
            # time.sleep(duration)
            # car.stop()
            print("Forward command executed.")

        elif user_input == 'B':
            # do something for 'B' command
            speed = int(input("Enter speed: "))
            duration = int(input("Enter time: "))
            angle = int(input("Enter angle: "))
            car.Manuevering_back_at_angle(speed, duration, angle)
            print("Backward command executed.")

        elif user_input == 'PL':
            # do something for 'PL' command
            car.Manuevering_back_at_angle(100,.75,-30)
            car.Manuevering_back_at_angle(100,1,30)
            car.Manuevering_fwd_at_angle(70,0.5,0)
            print("Parallel left command executed.")

        elif user_input == 'PR':
            # do something for 'PR' command
            car.Manuevering_back_at_angle(100,.75,30)
            car.Manuevering_back_at_angle(100,1,-30)
            car.Manuevering_fwd_at_angle(70,0.5,0)
            print("Parallel right command executed.")

        elif user_input == 'K':
            # do something for 'K' command
            car.Manuevering_fwd_at_angle(100,1,20)
            car.Manuevering_back_at_angle(100,1,-15)
            car.Manuevering_fwd_at_angle(100,2,20)
            print("K turn command executed.")

        elif user_input == 'E':
            break

        else:
            print("Invalid command. Please enter a valid command.")


if __name__ == "__main__":
    main()