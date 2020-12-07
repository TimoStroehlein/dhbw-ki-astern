import logging
import os


class FileController:

    @classmethod
    def is_path_valid(cls, path):
        """
        Checks if the passed path is valid
        :param path: The path to check
        :return: Boolean: True on valid, false on invalid
        """
        # If path is empty, it is not a valid path
        if path is None:
            return False

        # Check if the file exists and that it is accessible
        try:
            if os.path.exists(path):
                file = open(path, 'r')  # Opening with write deletes the file contents!
                file.close()
                return True
            else:
                return False
        except OSError:
            # Cannot open the file
            print('[ERROR] The path \'', path, '\' is not a valid path or the file does not exist.')
            return False
        except TypeError:
            # Path is not of type string or os.path, should never happen
            print("[FATAL] Path is in an invalid type!")
            return False
