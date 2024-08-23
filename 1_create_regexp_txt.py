import os
from config import ENTITYS_en, INTENTS_en, INTENT_REGEXP_DIRECTORY, ENTITY_REGEXP_DIRECTORY

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory created: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def create_txt_files(file_names, directory):
    create_directory_if_not_exists(directory)
    
    for file_name in file_names:
        file_path = os.path.join(directory, f"{file_name}.txt")
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("")  # Create an empty file
            print(f"Created: {file_path}")
        else:
            print(f"File already exists: {file_path}")

def main():
    # Directories for entities and intents
    entity_directory = INTENT_REGEXP_DIRECTORY
    intent_directory = ENTITY_REGEXP_DIRECTORY
    
    # Create files for entities
    create_txt_files(ENTITYS_en, entity_directory)

    # Create files for intents
    create_txt_files(INTENTS_en, intent_directory)

if __name__ == "__main__":
    main()
