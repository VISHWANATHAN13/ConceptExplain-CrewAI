from pathlib import Path
import yaml

FILE_DIR = Path(__file__).parent.parent
# debug
# print(FILE_DIR)
FILE_PATH = FILE_DIR / "agents" 
# debug
# print(FILE_PATH)
def load_yaml_file(file_name):

    file_path = FILE_PATH / file_name
    # debug
    # print(file_path)
    with open(file_path,"r") as f:
        # debug
        # print(f)
        return yaml.safe_load(f)


# debug
# if __name__ == "__main__":
    # load_yaml_file("agents_configuration.yaml")
