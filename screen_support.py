import os
import tools
import shlex
import struct
import preset
import platform
import subprocess


def get_terminal_width():
    return (get_terminal_size()[0])-1


def get_terminal_size():
    current_os = platform.system()
    tuple_xy = None
    if current_os == preset.SYSTEM_WINDOWS:
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
    if current_os in [preset.SYSTEM_LINUX, preset.SYSTEM_DARWIN] or current_os.startswith(preset.SYSTEM_CYGWIN):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        tools.print_display(preset.DEFAULT_L)
        tuple_xy = (80, 25)
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        standard_handle = windll.kernel32.GetStdHandle(-12)
        string_buffer = create_string_buffer(22)
        if windll.kernel32.GetConsoleScreenBufferInfo(standard_handle, string_buffer):
            (buffer_x, buffer_y, current_x, current_y, wattr, left, top, right, bottom, max_x, max_y) = struct.unpack("hhhhHhhhhhh", string_buffer.raw)
            size_x = right - left + 1
            size_y = bottom - top + 1
            return size_x, size_y
    except Exception:
        pass


def _get_terminal_size_tput():
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return cols, rows
    except Exception:
        pass


def _get_terminal_size_linux():
    def ioctl_GWINSZ(local_file_descriptor):
        try:
            import fcntl
            import termios
            return struct.unpack('hh', fcntl.ioctl(local_file_descriptor, termios.TIOCGWINSZ, '1234'))
        except Exception:
            pass
    coordinates = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not coordinates:
        try:
            file_descriptor = os.open(os.ctermid(), os.O_RDONLY)
            coordinates = ioctl_GWINSZ(file_descriptor)
            os.close(file_descriptor)
        except Exception:
            pass
    if not coordinates:
        try:
            coordinates = (os.environ[preset.LINES], os.environ[preset.COLUMNS])
        except Exception:
            return None
    return int(coordinates[1]), int(coordinates[0])
