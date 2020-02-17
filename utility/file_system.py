import os
from os import path
from typing import List


class FileSystem:

    @staticmethod
    def get_all_python_modules(p_subdir: str) -> List[str]:
        output = []
        sub_path = path.join(os.getcwd(), p_subdir)
        files = [f for f in os.listdir(sub_path)]
        for f in files:
            if f[:2] != "__" and f[:8] != "abstract" and f[:7] != "factory":
                file_name = os.path.splitext(f)[0]
                module_name = p_subdir + "." + file_name
                output.append(module_name)
        return output
