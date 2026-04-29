import os
import hashlib
import base64


class Hasher:
    def hash_file(self, file_path: str) -> str:
        with open(file_path, 'rb') as file:
            text = file.read()
            hash_obj = hashlib.md5(text).digest()
            base64_encoded_hash = base64.b64encode(hash_obj)
            encoded_string = base64_encoded_hash.decode('utf-8')
            return encoded_string

    def find_files(self, directory: str, extensions: tuple) -> list:
        file_list = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(extensions):
                    file_list.append(os.path.join(root, file))
        return file_list

    def hash_directory(self, directory: str, extensions: tuple) -> dict:
        file_list = self.find_files(directory, extensions)
        file_hashes = []
        for file in file_list:
            file_hash = self.hash_file(file)
            dir_name, file_name = os.path.split(file)
            _, last_dir_name = os.path.split(dir_name)
            result_path = os.path.join(last_dir_name, file_name)
            file_hashes.append({'hash': file_hash, 'file_path': result_path})

        return {'name': directory, 'file_hashes': file_hashes}
