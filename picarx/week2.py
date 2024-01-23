import picarx_improved

def main():
    car = picarx_improved.Picarx()

    while True:
        user_input = input("Please enter a command (F,B,PL,PR,K,E): ")

        if user_input == 'F':
            # do something for 'F' command
            speed = int(input("Enter speed: "))
            durration = int(input("Enter time: "))
            angle = int(input("Enter angle: "))
            car.Manuevering_fwd_at_angle(speed, durration, angle)
            print("Forward command executed.")

        elif user_input == 'B':
            # do something for 'B' command
            speed = int(input("Enter speed: "))
            durration = int(input("Enter time: "))
            angle = int(input("Enter angle: "))
            car.Manuevering_back_at_angle(speed, durration, angle)
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

        elif user_input == 'E':
            break

        else:
            print("Invalid command. Please enter a valid command.")


if __name__ == "__main__":
    main()