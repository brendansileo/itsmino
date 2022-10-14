from get_groups import get_groups
from get_decks import get_decks

commander_name = "Krark, the Thumbless;Sakashima of a Thousand Faces"
groups = get_groups(commander_name)
for i, group in enumerate(groups):
    print('Build '+str(i+1))
    print(get_decks(group, commander_name))



