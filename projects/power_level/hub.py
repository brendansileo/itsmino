import sys
sys.path.insert(0, '../api')
import mtg_api
import speed_of_setup

link = sys.argv[1]
deck = mtg_api.get_deck(link)

print("""
Deck: {name}
Commander: {commander}
""".format(name=deck.get_name(),
           commander='/'.join(deck.get_commander())))

setup_speed = speed_of_setup.get_speed(deck)
print(setup_speed)