import subprocess
import os

def run_script(script_name):
    script_path = script_name
    if os.path.exists(script_path):
        subprocess.run(['python', script_path], check=True)
        print(f"Executed {script_name} successfully.")
    else:
        print(f"{script_name} not found in the current directory.")

def main():
    # Run the first script
    run_script('1_create_regexp_txt.py')

    # Run the second script
    run_script('2_create_mapper.py')

if __name__ == "__main__":
    main()
