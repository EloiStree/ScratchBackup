import os
import requests
import pandas as pd



current_folder = os.getcwd()
print("Current execution folder:", current_folder)

def get_user_projects(username):
    url = f"https://api.scratch.mit.edu/users/{username}/projects"
    response = requests.get(url)
    
    if response.status_code == 200:
        projects = response.json()
        return projects
    else:
        print(f"Failed to fetch projects for user {username}. Status code: {response.status_code}")
        return None



def export_data_to_json(data, json_file_path):
    """
    Export data to a JSON file.

    Parameters:
    - data: The table data (dictionary or DataFrame).
    - json_file_path: The path to save the JSON file.
    """

    # If data is a dictionary, convert it to a DataFrame
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    try:
        # Export the DataFrame to a JSON file
        data.to_json(json_file_path, orient='records', lines=True)
        print(f"Data exported as JSON to {json_file_path}")
    except Exception as e:
        print(f"Error exporting data to JSON: {e}")
        
def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        with open(save_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Image downloaded successfully and saved at {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

def create_project_folder(project_id):
    folder_name = f"Projects/{project_id}"
    url_file_name = f"{project_id}.url"
    
    # Create folder
    os.makedirs(folder_name, exist_ok=True)
    
    # Create URL window file
    with open(os.path.join(folder_name, url_file_name), 'w') as file:
        file.write(f"[InternetShortcut]\nURL=https://scratch.mit.edu/projects/{project_id}\n")

def create_text_file(file_path, text_content):
    
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text_content)
        print(f"Text file created successfully at {file_path}")
    except Exception as e:
        print(f"Error creating text file: {e}")

# Example usage:

markdown="";
usernames = ["EloiStree", "jaimelesfrites2501", "eloiscratchstudents"]


markdown+="# Scratch project automatic portfolio  \n  \n"
markdown+="> Find here all the projects I have been working on until now.  \n"

heavytask=False
for username in usernames:
    projects = get_user_projects(username)
    if projects:
        print(f"Projects for user '{username}':")
        for project in projects:
            print(f"Project ID: {project['id']}")
            print(f"Title: {project['title']}")
            print(f"Description: {project['description']}")
            print(f"Thumbnail URL: {project['image']}")

            print(f"Views: {project['stats']['views']}")
            print(f"Loves: {project['stats']['loves']}")
            print(f"Favorites: {project['stats']['favorites']}")
            create_project_folder(project['id'])
            if heavytask:
                download_image(project['image'],f"Projects/{project['id']}.png")
                download_image(project['image'],f"Projects/{project['id']}/{project['id']}.png")
                export_data_to_json(project, f"Projects/{project['id']}/{project['id']}.json")
            print()
            markdown+=f"## {project['id']}: {project['title']}  \n  \n"
            markdown+=f"**Public:** {project['is_published']}  \n"
            markdown+=f"**Description:**  \n{project['description']}  \n"
            markdown+=f"**Instructions:**  \n{project['instructions']}  \n"
            markdown+= f"[![Projects/{project['id']}](Projects/{project['id']}/{project['id']}.png)](https://scratch.mit.edu/projects/{project['id']})  \nhttps://scratch.mit.edu/projects/{project['id']}  \n"

            
create_text_file("README.md", markdown)
