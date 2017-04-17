# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import uuid

from django.db import models

class ImageField(models.ImageField):
    def generate_filename(self, instance, filename):
        identity = str(instance.id)
        model_field_name = str(self.name)
        filename, extension = os.path.splitext(filename)
        filename = str(uuid.uuid4()).replace("-", "")[:20] + str(extension).lower()
        return '{}/{}/{}/'.format(identity, model_field_name, filename)