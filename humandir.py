from pathlib import Path
from typing import BinaryIO, Optional
from subprocess import CompletedProcess, run


class directory:
    """
    A more human-friendly way to interact with directories.
    """

    path: Path

    def __init__(self, path: Path):
        self.path = path

    @classmethod
    def from_str(self, path: str):
        self(Path(path))

    def parent(self):
        """
        Checks if this directory's parent directory exists, and returns it's
        directory object if it does.

        Returns None if the logical parent of this directory does not exist.
        """
        p = self.path.parent
        if not p.exists():
            return None
        return directory(p)

    def subpath(self, name: str) -> Path:
        """
        Returns a path within this directory, with no prior checks.

        `name`: the subpath
        """
        return self.path.joinpath(name)

    def dir(self, name: str):
        """
        Ensures that the given subdirectory exists and returns it if it exists.

        Returns None if the directory does not exists and/or could not be created.

        `name`: the name of the subdirectory
        """
        if not self.ensure_dir():
            return None
        return directory(self.subpath(name))

    def ensure_dir(self, name: str) -> bool:
        """
        Ensures that the given subdirectory exists within this directory,
        creating one if necessary.

        Returns true if the subdirectory exists or has been successfully
        created.

        `name`: the name of the subdirectory
        """
        dir_path = self.subpath(name)
        if dir_path.exists():
            return dir_path.is_dir()
        else:
            try:
                dir_path.mkdir()
                return True
            except:
                return False

    def ensure_all_dirs(self, *names: str) -> bool:
        for n in names:
            if not self.ensure_dir(n):
                return False

    def ensure_tree(self, *tree: str) -> bool:
        """
        Recursively ensures that a hierarchy of subdirectories exists,
        top-level first.

        Returns true if all directories were successfully created.

        `tree`: the list of directories, top-level first
        """
        if not self.ensure_dir(tree[0]):
            return False
        if len(tree) > 1:
            if not self.dir(tree[0]).ensure_tree(tree[1:]):
                return False

    def ensure_file(self, name: str) -> bool:
        """
        Ensures that the given file exists with this directory, creating one
        if necessary.

        Returns true if the directory exists or was successfully created.

        `name`: the name of the file
        """
        file_path = self.subpath(name)
        if file_path.exists():
            return file_path.is_file()
        else:
            try:
                with file_path.open("xt") as f:
                    f.write("")
                return True
            except:
                return False

    def file(self, name: str, mode: str) -> Optional[BinaryIO]:
        """
        Ensures that the given file exists, and then returns it's file
        descriptor opened with the given mode.

        Returns None if the file does not exist and/or could not be created.

        `name`: the name of the file
        `mode`: the mode to open the file with
        """
        if not self.ensure_file(name):
            return None
        return self.subpath(name).open(mode)

    def dump_file(self, name: str, data: bytes) -> bool:
        """
        Ensures the file exists, and then dumps the given data to it if it
        exists.

        Returns true if the file exists or was successfully created, but
        does not return false if the file creation was unsuccessful.

        `name`: the name of the file
        `data`: the data to be written
        """
        if self.ensure_file(name):
            with self.subpath(name).open("wb") as f:
                f.write(data)
            return True
        else:
            return False

    def dump_file_str(self, name: str, txt: str) -> bool:
        """
        Same as dump_file, but takes a string instead of a bytes object.

        `name`: the name of the file
        `txt`: the text to be written
        """
        return self.dump_file(name, bytes(txt))

    def cmd(self, *args: str, **kwargs) -> CompletedProcess:
        """
        Runs a command within this directory. All keyword arguments passed to
        this method will be passed to `subprocess.run`.

        Return the completed process from the executed command.
        """
        kwargs["cwd"] = self.path.absolute().resolve().as_posix()
        return run(args, **kwargs)
