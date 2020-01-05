from enums.SizeUnit import SizeUnit
import os

def convert_unit(size_in_bytes, unit):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SizeUnit.KB:
        return size_in_bytes/1024
    elif unit == SizeUnit.MB:
        return size_in_bytes/(1024*1024)
    elif unit == SizeUnit.GB:
        return size_in_bytes/(1024*1024*1024)
    else:
        return size_in_bytes


def get_file_size(file_name, size_type = SizeUnit.BYTES):
    """ Get file in size in given unit like KB, MB or GB"""
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)

