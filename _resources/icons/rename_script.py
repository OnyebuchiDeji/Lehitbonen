import os

def work():
    target_dir = os.path.join(os.getcwd(), "_resources", "icons")
    for file in os.scandir(target_dir):
        if file.is_file():
            if file.name.endswith(".png"):
                split = file.name.split(".")
                name = split[0]
                ext = split[1]
                name_split = name.split("_")
                if len(name_split) > 2:
                    print("Former Name: ", name_split)
                    mstr = "br"
                    new_name = "_".join([name_split[0].lower(), name_split[1].lower()])
                    new_name = ".".join([new_name, ext])
                    print("New Name: ", new_name)
                    former_path = os.path.join(target_dir, file.name)
                    new_path = os.path.join(target_dir, new_name)
                    os.rename(former_path, new_path)
    

if __name__ == "__main__":
    work()