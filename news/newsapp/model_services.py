from time import time
from pytils.translit import slugify


def gen_slug(s):
    new_slug = slugify(s)
    return new_slug + "-" + str(int(time()))


def gen_user_slug(s):
    return slugify(s)