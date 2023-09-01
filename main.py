import os
import time


class TerminalEmulator:
    def __init__(self):
        self.base_directory = os.path.abspath("pj")
        self.users = {
            "user": {"password": "qwerty123", "directory": "home/user"},
            "star_admin": {"password": "ILoveChickenS0up", "directory": "home"},
            "root": {"password": "Q9sM02ip(]_iaS@(YMa-<)&C", "directory": ""}
        }
        self.current_directory = self.base_directory
        self.user = None
        self.prompt = None

    def run(self):
        self.login()
        if self.user:
            print(f"Welcome, {self.user}!")
            while True:
                self.prompt = f"{self.get_formatted_prompt()}$ "
                user_input = input(self.prompt)
                if user_input.lower() == "exit":
                    break

                output = self.execute_command(user_input)
                print(output)

    def login(self):
        while not self.user:
            username = input("Username: ")
            password_attempts = 3
            while password_attempts > 0:
                password = input("Password: ")  # In a real scenario, you'd want to securely handle passwords
                if self.authenticate(username, password):
                    print("Login successful!")
                    self.user = username
                    self.current_directory = self.users[username]["directory"]
                    return
                else:
                    password_attempts -= 1
                    print("Wrong password. Please try again.")
                    if password_attempts == 0:
                        print("Login failed. Please try again.")
                        break

    def authenticate(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return True
        return False

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return ""

        base_command = parts[0].lower()

        if base_command == "pwd":
            return self.get_formatted_path()
        elif base_command == "ls":
            return "\n".join(os.listdir(self.get_current_directory()))
        elif base_command == "cd":
            return self.change_directory(parts[1] if len(parts) > 1 else "")
        elif base_command == "cat":
            if len(parts) > 1:
                return self.read_file(parts[1])
            else:
                return "cat: missing operand"
        elif base_command == "logout":
            return self.logout()
        elif base_command == "python3":
            if len(parts) > 1 and parts[1].endswith(".py"):
                return self.run_python_script(parts[1])
            else:
                return "Usage: python3 <script.py>"
        elif base_command == "ufw":
            if self.user == "star_admin" or self.user == "root":
                return self.execute_ufw_command(parts)
            elif self.user == "user":
                return "Access Denied"
        else:
            return f"Command not found: {command}"

    def change_directory(self, destination):
        if destination == "/":
            self.current_directory = self.users[self.user]["directory"]
        elif destination == "~":
            self.current_directory = self.users[self.user]["directory"]
        else:
            new_path = self.get_absolute_path(os.path.join(self.current_directory, destination))
            if self.user == "user" and not os.path.abspath(new_path).startswith(self.get_current_directory()):
                return f"cd: {destination}: Access denied"
            elif os.path.exists(new_path) and os.path.abspath(new_path).startswith(self.get_current_directory()):
                self.current_directory = self.get_relative_path(new_path)
            else:
                return f"cd: {destination}: No such directory"
        return ""

    def read_file(self, file_name):
        file_path = os.path.join(self.get_current_directory(), file_name)
        try:
            with open(file_path, "r") as file:
                content = file.read()
                return content
        except FileNotFoundError:
            return f"cat {file_name}: No such file or directory"
        except Exception as e:
            return f"Error reading file: {e}"

    def run_python_script(self, script_name):
        if script_name == "Run4w4Y.py":
            main_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(main_dir, "Tickets")
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    print(content)
                    print("Unwrapping ", end="")
                    for _ in range(5):
                        time.sleep(1.5)
                        print(".", end="")
                    print()
                    print("Scanning ", end="")
                    for _ in range(5):
                        time.sleep(1)
                        print(".", end="")
                    print()
                    print("Another user detected: star_admin")
                    time.sleep(2)
                    print("Vulnerability detected - StackRot (CVE-2023-3269)\nAssembling payload")
                    time.sleep(4)
                    print("Sending payload")
                    time.sleep(1.5)
                    print("Payload sent. Awaiting incoming information")
                    time.sleep(3)
                    if self.user == "user":
                        print("Gathered information:\n\n!!!\nLOGIN: star_admin\nPASSWORD: ILoveChickenS0up\n!!!\n")
                    elif self.user == "star_admin":
                        print("Gathered information:\n\n!!!\nLOGIN: user\nPASSWORD: qwerty123\n\nLOGIN: "
                              "root\nPASSWORD: Q9sM02ip(]_iaS@(YMa-<)&C\n!!!\n")
                    elif self.user == "root":
                        print("Gathered information:\n\n!!!\nLOGIN: user\nPASSWORD: qwerty123\n\nLOGIN: LOGIN: "
                              "star_admin\nPASSWORD: ILoveChickenS0up\n!!!\n")
                    print("Wrapping up and cleaning logs ", end="")
                    for _ in range(5):
                        time.sleep(0.8)
                        print(".", end="")
                    print("\nThank you for using RUNAWAY software:)\nLogging out")
                    return self.logout()
            except FileNotFoundError:
                return "File not found"

    def execute_ufw_command(self, command_parts):
        if len(command_parts) >= 3 and command_parts[1] == "allow" and "/" in command_parts[2]:
            port_str, protocol = command_parts[2].split("/")
            try:
                port = int(port_str)
                if protocol == "tcp" and port == 3020:
                    return "WOW!"
                elif protocol == "tcp":
                    return f"Allowing traffic on port {port} using ufw..."
                else:
                    return f"Unsupported protocol: {protocol}. Only 'tcp' protocol is supported."
            except ValueError:
                return f"Invalid port: {port_str}. Please provide a valid integer port number."
        else:
            return "Invalid ufw command format. Usage: ufw allow <port>/<protocol>"

    def logout(self):
        self.user = None
        self.current_directory = self.base_directory
        print("Logged out. Please log in.")
        return self.run()

    def get_formatted_path(self):
        return f"{self.get_formatted_prompt()} {self.get_relative_path(self.get_current_directory())}"

    def get_formatted_prompt(self):
        return f"{self.user if self.user else 'None'}@aicore:{self.get_relative_path(self.current_directory)}"

    def get_relative_path(self, absolute_path):
        target_path = self.get_current_directory()
        if absolute_path:
            return os.path.relpath(absolute_path, target_path).replace("\\", "/").lstrip("/")
        else:
            return ""

    def get_absolute_path(self, relative_path):
        return os.path.normpath(os.path.join(self.get_current_directory(), relative_path.lstrip("/")))

    def get_current_directory(self):
        return os.path.normpath(os.path.join(self.base_directory, self.current_directory))




if __name__ == "__main__":
    terminal = TerminalEmulator()
    terminal.run()
