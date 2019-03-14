"""
Module contains class to extract tar and gz files
"""

import re
import tarfile
import gzip
from pathlib import Path

#pylint: disable-msg=too-many-arguments
#pylint: disable-msg=invalid-name
#pylint: disable-msg=no-else-return

class Extract:
    """
    This class takes care of extracting files
    """

    file_extensions = ('.tar', '.tgz', '.tbz', '.tb2')

    @staticmethod
    def make_unique_directory_name(directorypath):
        """
        This make sure the directory path is always unique
        To avoid exceptions when creating a new directory

        Example:
            Directory 'test' is already unique
                Input   '/home/test'
                Output  '/home/test'

            Directory 'test' exists
                Input   '/home/test'
                Output  '/home/test 1'

            Directory 'test' and 'test1' exists
                Input   '/home/test'
                Output  '/home/test 2'
        Args:
            directorypath(str): Directory full path to make unique

        Returns:
            str: Unique directory full path
        """
        directorypath = Path(directorypath)
        if directorypath.exists():
            parent_path = directorypath.parent
            match = re.compile("(?P<name>.*)[ ](?P<num>\\d+).*$").match(directorypath.as_posix())

            if match:
                new_num = int(match.group('num')) + 1
                new_dir_name = "%s %d" % (match.group('name'), new_num)
                new_folder = (parent_path / new_dir_name).as_posix()
                return Extract.make_unique_directory_name(new_folder)

            else:
                new_dir_name = "%s %d" % (directorypath.stem, 1)
                new_folder = (parent_path / new_dir_name).as_posix()
                return Extract.make_unique_directory_name(new_folder)

        return directorypath.as_posix()

    @staticmethod
    def tar(filepath, extract_to=None, create_dir=True, delete=True):
        """
        Extracting tar file or files that have the same extension as file_extensions

        Args:
            filepath(str):      Filepath to compressed file
            extract_to(str):    Path to extract to, default is the folder where it is located
            create_dir(bool):   Creating directory with filename as directory name
            delete(bool):       Delete file after extracting

        Returns:
            str: Folder where files are extracted to
        """
        try:
            filepath = Path(filepath)

            if extract_to is None:
                extract_to = filepath.parent

            if create_dir:
                extract_to = (extract_to / filepath.stem).as_posix()
                extract_to = Extract.make_unique_directory_name(extract_to)
                print("Create directory '%s'" % extract_to)
                extract_to = Path(extract_to)
                extract_to.mkdir()

            filepath = filepath.as_posix()
            extract_to = extract_to.as_posix()
            print("Extracting '%s' to '%s'" % (filepath, extract_to))

            tar = tarfile.open(filepath)
            tar.extractall(extract_to)
            tar.close()
            print("Extracting done")

            if delete:
                Path(filepath).unlink()
                print("Deleted file '%s'" % filepath)

            return extract_to

        except OSError as exc:
            print("Error while extracting file '%s'" % filepath)
            print("Message '%s'" % str(exc))

    @staticmethod
    def gz(filepath, extract_to=None, create_dir=False, delete=True):
        """
        Extracting gz file

        Args:
            filepath(str):      Filepath to compressed file
            extract_to(str):    Path to extract to, default is the folder where it is located
            create_dir(bool):   Creating directory with filename as directory name
            delete(bool):       Delete file after extracting

        Returns:
            str: Folder where files are extracted to
        """
        try:
            filepath = Path(filepath)
            if extract_to is None:
                extract_to = filepath.parent
            if create_dir:
                extract_to = (extract_to / filepath.stem).as_posix()
                extract_to = Extract.make_unique_directory_name(extract_to)
                print("Create directory '%s'" % extract_to)
                extract_to = Path(extract_to)
                extract_to.mkdir()

            extract_to = (extract_to / filepath.stem).as_posix()
            filepath = filepath.as_posix()

            print("Extracting '%s' to '%s'" % (filepath, extract_to))
            gzfile = gzip.open(filepath)
            output = open(extract_to, "wb")
            output.write(gzfile.read())
            gzfile.close()
            output.close()
            print("Extracting done")
            if delete:
                Path(filepath).unlink()
                print("Deleted file '%s'" % filepath)
            return extract_to

        except OSError as exc:
            print("Error while extracting file '%s'" % filepath)
            print("Message '%s'" % str(exc))

    @staticmethod
    def walk_tree_and_extract(directory_path, delete=True, create_dir=True, gz_create_dir=False):
        """
        Recursively walk through tree and extract compressed files

        Args:
            directory_path(str): Directory to start in
            delete(bool): Delete files after extracting
            create_dir(bool): Create directories for tar files
            gz_create_dir(bool): Create directories for gz files
        """
        directory_path = Path(directory_path)
        files = list(x for x in directory_path.glob("**/*.*") if x.is_file())

        for filepath in files:
            extension = filepath.suffix
            filepath = filepath.as_posix()
            new_dir = None
            if extension.lower() in Extract.file_extensions:
                new_dir = Extract.tar(filepath, create_dir=create_dir, delete=delete)

            elif extension.lower() == '.gz':
                new_dir = Extract.gz(filepath, create_dir=gz_create_dir, delete=delete)

            if new_dir is not None:
                Extract.walk_tree_and_extract(new_dir)

    @staticmethod
    def extract(filepath, extract_to=None, recursive=True, delete=True,
                create_dir=True, gz_create_dir=False):
        """
        Extract single file or recursively through tree

        Args:
            filepath(str): Filepath of file to extract
            extract_to(str): Directory to extract files in
            recursive(bool): Run through tree and extract files
            delete(bool): Delete files after extracting (takes effect if recursive is true)
            create_dir(bool): Create directory for tar files (takes effect if recursive is true)
            gz_create_dir(bool): Create directory for gz files (takes effect if recursive is true)
        """
        ext = Path(filepath).suffix
        new_dir = None

        if ext in Extract.file_extensions:
            new_dir = Extract.tar(filepath, extract_to=extract_to,
                                  create_dir=True, delete=False)

        elif ext == '.gz':
            new_dir = Extract.gz(filepath, extract_to=extract_to,
                                 create_dir=True, delete=False)

        else:
            print("Not valid file extension '%s'" % ext)
            return

        if recursive and new_dir is not None:
            Extract.walk_tree_and_extract(new_dir, delete=delete,
                                          create_dir=create_dir, gz_create_dir=gz_create_dir)
