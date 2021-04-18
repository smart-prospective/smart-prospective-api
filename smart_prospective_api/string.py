
def str_to_ascii(msg):
    """
    Convert a string to ascii encoding.

    :param string msg: The msg to convert.
    """
    return msg.encode('ascii', 'ignore').decode('ascii')
