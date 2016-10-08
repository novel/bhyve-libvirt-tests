import os.path

FIXTURE_PREFIX = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "static")


def get(name, format=None):
    fixture_path = os.path.join(FIXTURE_PREFIX, name)
    with open(fixture_path, 'r') as f:
        data = f.read()

    if format:
        for var, value in format.items():
            data = data.replace("%%" + var + "%%", value)

    return data
