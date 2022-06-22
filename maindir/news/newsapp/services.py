from newsapp.models import Article


def create_pagination_list():
    pag_list = []
    for i in range(51):
        if i % 10 == 0 and i >= 10 or i == 5:
            pag_list.append(str(i))
    return pag_list


class TimeInterval:
    name = str
    interval_desc = str
    interval_asc = str

    def __init__(self, name, interval):
        self.name = name
        self.interval_desc = f'-time_create__{interval}'
        self.interval_asc = f'time_create__{interval}'


def create_time_interval_list():
    return [TimeInterval('For hour', 'hour'),
            TimeInterval('For day', 'day'),
            TimeInterval('For week', 'week'),
            TimeInterval('For month', 'month'),
            TimeInterval('For year', 'year')]


def get_article_related_objects(kwargs):
    return Article.objects.select_related('user', 'cat', 'user__userprofile') \
        .prefetch_related('comments', 'comments__parent', 'comments__user__userprofile') \
        .get(slug=kwargs['article_slug'])
