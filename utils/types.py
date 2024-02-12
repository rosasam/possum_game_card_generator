def get_card_type(types):
    if types is None or types == '':
       return 'default'

    types_list = [t.strip() for t in types.split(",")]
    special_card_types = ['EGG', 'lock', 'trap']
    for card_type in special_card_types:
      if card_type in types_list:
        return card_type
    return 'default'