import os
import zipfile


def unzip_mission(source_miz, dest_folder):
    with zipfile.ZipFile(source_miz, 'r') as zip:
        zip.extractall(dest_folder)
        zip.close()


def zip_mission(source_folder, dest_miz_path):
    zipf = zipfile.ZipFile(dest_miz_path, mode='w')
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, file_path[len(source_folder):])
    zipf.close()

    # zipf = zipfile.ZipFile(dest_miz_path, 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in os.walk(source_folder):
    #     for file in files:
    #         # zipf.write(os.path.join(root, file))
    #         zipf.write(file)
    # zipf.close()
