import os


class cleaner:
    def __init__(self):
        tmp_folder = 'src/tmp/'
        self.__clean_tmp(tmp_folder)

    def __clean_tmp(self, folder_path: str):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith(('.mp3', '.txt')):
                    os.remove(file_path)
                    print(f"Deleted: {filename}")


cleaner()
