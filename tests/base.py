from datetime import datetime

import uuid

TIME_FORMAT = "%d%m%y_%H%M%S"


class BaseTestCase(object):

    def name_generate(self, obj):
        return "%s_%s" % (obj, datetime.now().strftime(TIME_FORMAT))

    def uuid(self):
        return str(uuid.uuid4())
