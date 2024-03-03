import random
from string import hexdigits

from .models import Code


class CodeManager:
    @staticmethod
    def generate(user):
        code = ''.join(random.sample(hexdigits, 5))
        if Code.objects.filter(user=user).exists():
            Code.objects.filter(user=user).update(code=code)
        else:
            Code.objects.create(user=user, code=code)
        return code
