import picarx_improved

def main():
    car.Picarx()
    user_input = input("Please enter a command (F,B,PL,PR,K): ")
    
    if user_input == 'F':
        # do something for 'F' command
        speed = float(input("Enter speed: "))
        time = float(input("Enter time: "))
        angle = float(input("Enter angle: "))
        car.Manuevering_fwd_at_angle(speed, time, angle)
        print("Forward command executed.")
    
    elif user_input == 'B':
        # do something for 'B' command
        speed = float(input("Enter speed: "))
        time = float(input("Enter time: "))
        angle = float(input("Enter angle: "))
        car.Manuevering_back_at_angle(speed, time, angle)
        print("Backward command executed.")
    
    elif user_input == 'PL':
        # do something for 'PL' command
        print("Parallel left command executed.")
    
    elif user_input == 'PR':
        # do something for 'PR' command
        print("Parallel right command executed.")
    
    elif user_input == 'K':
        # do something for 'K' command
        print("K turn command executed.")
    
    else:
        print("Invalid command. Please enter a valid command.")


if __name__ == "__main__":
    main()