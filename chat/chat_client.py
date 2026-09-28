from re import match
import socket
import threading
import time
import os
import json


def find_local_ip():
    try: 
        temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        temp_socket.connect(("8.8.8.8", 80))
        local_ip = temp_socket.getsockname()[0]
        temp_socket.close()
        return local_ip
    except Exception as error:
        print("Error:", error)
        return None

CLIENT_IP = find_local_ip()  # Enter your IP address here
SERVER_IP = '10.100.50.35'  # Put your server's IP address here
PORT = 56789
name = "Guest"
color = ""
CONFIG_FILE = "config.json"



# Makes .json for user settings
def load_config():
    global name, color
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                name = data.get("name", name)
                color = data.get("color", color)
        except Exception as e:
            print(f"Error loading config: {e}")

def save_config():
    """Save current name and color to a JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"name": name, "color": color}, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

# Load saved shit
load_config()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def clear_terminal_ansi():
    # \x1b[2J clears the screen, \x1b[H moves the cursor to the top-left
    print("\x1b[2J\x1b[H", end="")


def welcome_message():
    global name
    global color
    global SERVER_IP
    global PORT
    clear_terminal_ansi()
    print("+-------------------------------------------------------------------------------+")
    print("\nWelcome to the server. You have started the clientside. \nIf you are having any troubles, please write it down on the shared spreadsheet.\n Please look at the README doc in the folder, and read the ToS\n \n Your current version is 0.2.7")
    print("+-------------------------------------------------------------------------------+")
    print(f"\nCurrent Profile: {color}{name}\033[00m")
    print(" ")
    print("Options:")
    print("1) Continue to server")
    print("2) Set display name")
    print("3) Set name color")
    print("4) Set server IP and port")

    start = int(input("Enter number associated: "))
    match start:
        case 1:
            return
        case 2:
            clear_terminal_ansi()
            print("=== SET DISPLAY NAME ===")
            new_name = input("Enter your new display name: ").strip()
            if new_name:
                name = new_name
                save_config()
                print(f"Name updated to: {color}{name}\033[00m")
            else:
                print("Name cannot be empty.")
                time.sleep(1.5)
                welcome_message()
        case 3:
           
            print("Choose what color you would like:")
            print("1) \033[91mRed\033[00m")
            print("2) \033[92mGreen\033[00m")
            print("3) \033[93mYellow\033[00m")
            print("4) \033[94mLight Purple\033[00m")
            print("5) \033[95mPurple\033[00m")
            print("6) \033[96mCyan\033[00m")
            print("7) \033[97mLight Gray\033[00m")
            print("")
            try:
                choice = int(input("Enter the corresponding number to your choice: "))
            except ValueError:
                choice = 0

            match choice:
                case 1:
                    color = "\033[91m"
                case 2:
                    color = "\033[92m"
                case 3:
                    color = "\033[93m"
                case 4:
                    color = "\033[94m"
                case 5:
                    color = "\033[95m"
                case 6:
                    color = "\033[96m"
                case 7:
                    color = "\033[97m"
                case 8:
                    color = "\033[3;4m\033[92m"
                case _:
                    print("Invalid color. Set to white")
                    color = "\033[00m"

            save_config()
            welcome_message()
        case 4:
            print("Set a new IP to connect to:")
            SERVER_IP = str(input())
            print("Set a new port to connect to:")
            PORT = int(input())
            print(f"\nServer set to {SERVER_IP}:{PORT}\n")
            welcome_message()

        case _:
            print("\nInvalid input. Please relaunch the program.")
            time.sleep(3)
            welcome_message()


welcome_message()

#attempt connection with server
try:
    print(f"Initiating server connect on {SERVER_IP}:{PORT}")
    client.connect((SERVER_IP, PORT))
    client.send(f"NAME:{color}{name}\033[00m".encode('utf-8'))
    print(f"\n[+] SUCCESS: Successfully connected to server at {SERVER_IP} on port {PORT}!\n")

#fail handiling
except Exception as e:
        print(f"[-] Unable to connect to the server at {SERVER_IP}:{PORT}. Error: {e}")
        client.close()
        quit()




def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("An error occurred!")
            client.close()
            break




def write():
    while True:
        message = input('Me: ')
        full_message = f"{color}{name}\033[00m: {message}"
        client.send(full_message.encode('utf-8'))




receive_thread = threading.Thread(target=receive)
receive_thread.start()




write_thread = threading.Thread(target=write)
write_thread.start()


