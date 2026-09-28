import os
import json
import subprocess
import getpass
from pathlib import Path

# Configuration
USER_DATA_FILE = "user.json"

def load_users():
    """Load user database from JSON file."""
    if not os.path.exists(USER_DATA_FILE):
        return {}
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_users(users):
    """Save user database to JSON file."""
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

def run_program(folder, script_name):
    """Launch an external Python script and return when finished."""
    script_path = os.path.join(folder, script_name)
    
    if not os.path.exists(script_path):
        print(f"\n❌ Error: Could not find '{script_name}' inside the '{folder}' folder.")
        input("\nPress Enter to return to the menu...")
        return

    print(f"\n🚀 Launching {script_name.replace('.py', '').title()}... Close its window to return here.")
    try:
        # Runs the program and pauses 'main.py' until the app finishes execution
        subprocess.run(["python", script_path], check=True)
    except Exception as e:
        print(f"\n❌ Something went wrong while running the app: {e}")
        input("\nPress Enter to return to the menu...")

def auth_menu():
    """Initial login / registration gateway."""
    users = load_users()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print(" 🏰  WELCOME TO THE CITADEL  🏰 ")
        print("=" * 40)
        print("1. Login")
        print("2. Create New Account")
        print("3. Exit")
        print("=" * 40)
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            username = input("Username: ").strip()
            # getpass hides the password typing in standard terminals
            password = getpass.getpass("Password: ")
            
            if username in users and users[username]["password"] == password:
                print(f"\n✅ Access Granted. Welcome back, {username}!")
                input("Press Enter to enter the Citadel...")
                return username
            else:
                print("\n❌ Invalid username or password.")
                input("\nPress Enter to try again...")
                
        elif choice == "2":
            username = input("Choose a Username: ").strip()
            if not username:
                print("\n❌ Username cannot be blank.")
                input("\nPress Enter to try again...")
                continue
                
            if username in users:
                print("\n❌ That username is already taken.")
                input("\nPress Enter to try again...")
                continue
                
            password = getpass.getpass("Choose a Password: ")
            if len(password) < 4:
                print("\n❌ Password must be at least 4 characters long.")
                input("\nPress Enter to try again...")
                continue
                
            # Create user profile shell (you can add high scores, bio, etc., here later)
            users[username] = {
                "password": password,
                "high_scores": {"pong": 0, "snake": 0}
            }
            save_users(users)
            print("\n🎉 Account created successfully! You can now log in.")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            print("\nGoodbye!")
            exit()
        else:
            print("\n❌ Invalid choice.")
            input("\nPress Enter to try again...")

def main_hub(username):
    """The core navigation menu after authentication."""
    # Maps user choices to specific files inside your apps directory
    categories = {
        "1": {"name": "🎵  Music", "folder": "music"},
        "2": {"name": "🕹️  Games", "folder": "games"},
        "3": {"name": "⏱️  Timer", "folder": "timer"},
        "4": {"name": "💬 Chat Client", "folder": "chat"}
    }
    
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print(f" 🏰  THE CITADEL - Main Hub  [User: {username}]")
        print("=" * 40)
        print("Available Programs:")
        
        for key, app in categories.items():
            print(f"{key}. {app['name']}")
            
        print("5. Log Out")
        print("=" * 40)
        
        choice = input("Where would you like to go? (1-5): ").strip()
        
        if choice in categories:
            folder = categories[choice]["folder"]
            folder_path = Path(f"{folder}")
            for file in folder_path.iterdir():
                if file.is_file():
                    print(f"File Name: {file.name}")
            choice = str(input("Enter your choice: ")).lower().strip()
            run_program(folder_path, choice)

        elif choice == "5":
            print("\nLogging out...")
            break
        else:
            print("\n❌ Invalid choice.")
            input("\nPress Enter to try again...")

if __name__ == "__main__":
        
    while True:
        logged_in_user = auth_menu()
        main_hub(logged_in_user)
