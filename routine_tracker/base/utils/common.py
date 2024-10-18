BOOTSTRAP_ICONS = [
    'bi-alarm',
    'bi-bag',
    'bi-bell',
    'bi-bicycle',
    'bi-book',
    'bi-camera',
    'bi-cloud',
    'bi-cup',
    'bi-envelope',
    'bi-flag',
    'bi-house',
    'bi-music-note',
    'bi-star',
    'bi-sun',
    'bi-wifi',
]


def icon_choices():
    return [(icon, icon[3:].replace('-', ' ').capitalize()) for icon in BOOTSTRAP_ICONS]
