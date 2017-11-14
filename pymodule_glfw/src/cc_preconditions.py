def file_exists(absolute_path):
    """Fails if file does not exist."""
    if not open(absolute_path):
        raise FileNotFoundError('File not found at %s' % absolute_path)