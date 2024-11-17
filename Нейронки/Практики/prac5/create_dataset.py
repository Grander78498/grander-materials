import os
import shutil

def find_flac_files(directory, dest_directory):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
        
    flac_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.flac'):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(dest_directory, file)
                
                # Перемещаем файл
                shutil.copy2(source_file_path, destination_file_path)
                print(f'Скопирован: {source_file_path} -> {destination_file_path}')

root_directory = 'D:/Music/complete'
dest_dir = 'D:/Music/dataset'

find_flac_files(root_directory, dest_dir)