import random
from fake_useragent import UserAgent

useragent = UserAgent()

store = {'leagues': {

        },
        'leagues_clubs': set(),


        'clubs': {

        },
        'clubs_players': set(),


        'clubs_link': {

        },
        'stadiums': {

        },
        'stadium_clubs': set(),


        'players_link': {

        },
        'players_info': {

        },
        'positions': [],
        'positions_players': set(),

        'nation': [],
        'nations_players': set(),

        'national_team_players': set()


    }

leagues = []
list_url = []
stadium_list = []
position_list = []
nation_list = []
headers = {'User-Agent': useragent.chrome}