import rumps
import requests
import threading
import subprocess
import os
import sys

import config


def setup():
    if not os.path.exists(config.model_folder):
        if input(f"Model folder {config.model_folder} does not exist. Create it? (y/n) ").lower() == 'y':
            os.makedirs(config.model_folder)
    
    for model in config.models:
        if model == 'default':
            continue
        if config.models[model]['type'] == 'local':
            # Extract the parts from the URL
            url_parts = config.models[model]['url'].split('/')
            # The structure is models/TheBloke/CodeLlama-34B-Instruct-GGUF/codellama-34b-instruct.Q4_K_M.gguf
            # So we take the relevant parts from the URL to form the path
            owner = url_parts[3]
            repo_name = url_parts[4]
            model_filename = url_parts[-1]

            # Construct the nested folder path
            nested_folder_path = os.path.join(config.model_folder, owner, repo_name)
            model_path = os.path.join(nested_folder_path, model_filename)

            # Check if the nested folder exists, if not, create it
            if not os.path.exists(nested_folder_path):
                os.makedirs(nested_folder_path)

            # Check if the model file exists within the nested folder
            if not os.path.isfile(model_path):
                if input(f'Model {model} not found in {nested_folder_path}. Would you like to download it? (y/n) ').lower() == 'y':
                    print(f"Downloading {model} from {config.models[model]['url']}...")
                    subprocess.run(['curl', '-L', config.models[model]['url'], '-o', model_path])
            else:
                print(f"Model {model} found in {nested_folder_path}.")



class ModelPickerApp(rumps.App):
    def __init__(self):
        super(ModelPickerApp, self).__init__("ModelPickerApp")

        # Dynamically create menu items from the MENUBAR_OPTIONS
        self.menu_items = {}
        for option in config.models:
            if option == 'default':
                continue
            self.menu_items[option] = rumps.MenuItem(
                title=option, callback=self.pick_model)

        self.menu = list(self.menu_items.values())
        self.menu_items[config.models['default']].state = True
        self.icon = "icon.png"

    def pick_model(self, sender):
        # Toggle the checked status of the clicked menu item
        sender.state = not sender.state

        # Send the choice to the local proxy app
        if sender.state:
            choice = sender.title
            try:
                response = requests.post(
                    "http://localhost:1730/set_target", json={"target": choice})
                if response.status_code == 200:
                    print(f"Successfully sent selection: {choice}.")
                else:
                    rumps.alert(
                        "Error", f"Failed to send selection. Server responded with: {response.status_code}.")
            except requests.RequestException as e:
                rumps.alert("Error", f"Failed to send selection. Error: {e}.")

        # If other options were previously selected, deselect them
        for item in self.menu:
            if item == 'Quit':
                continue
            if item != sender.title:
                self.menu_items[item].state = False

    def run_server(self):
        subprocess.run(['python', 'proxy.py'])

if __name__ == '__main__':
    if '--setup' in sys.argv:
        setup()
    app = ModelPickerApp()
    print("Running server...")
    server_thread = threading.Thread(target=app.run_server)
    server_thread.start()
    app.run()