import os, datetime, requests
from dotenv import load_dotenv

load_dotenv()

from flask import Blueprint

games = Blueprint("games", "games")

base_url = "https://api.rawg.io/api/"
key = os.environ.get("API_KEY")


def get_current_month():
    """returns the current month from (1 to 12)"""
    month = datetime.datetime.now().month
    if month < 10:
        return f"0{month}"
    else:
        return month


def get_current_day():
    """returns the current day of the month from (1 to 31)"""
    day = datetime.datetime.now().day
    if day < 10:
        return f"0{day}"
    else:
        return day


def get_current_year():
    """returns the current year with four digits"""
    year = datetime.datetime.now().year
    return year


current_year = get_current_year()
current_month = get_current_month()
current_day = get_current_day()
current_date = f"{current_year}-{current_month}-{current_day}"
last_year = f"{current_year - 1}-{current_month}-{current_day}"
next_year = f"{current_year + 1}-{current_month}-{current_day}"

# POPULAR GAMES
popular_games = (
    f"games?key={key}&dates={last_year},{current_date}&ordering=-rating&page_size=10"
)

# UPCOMING GAMES
upcoming_games = (
    f"games?key={key}&dates={current_date},{next_year}&ordering=-added&page_size=10"
)

# RECENT GAMES
new_games = (
    f"games?key={key}&dates={last_year},{current_date}&ordering=-released&page_size=10"
)

# SEARCH GAMES
query_games = f"games?key={key}&search="

# BY GENRE, PLATFORM, PUBLISHER
genre_games = f"games?key={key}&genres="
platform_games = f"games?key={key}&platforms="
publisher_games = f"games?key={key}&publishers="

# GAME DETAILS, SCREENSHOTS, GENRES, PLATFORMS, PUBLISHERS
game_details = "games/"
game_screenshots = "/screenshots"
game_genres = "genres"
game_platforms = "platforms"
game_publishers_page = "publishers"

# PUBLISHERS VIEW 2
game_publishers = f"publishers?key={key}&page_size=50"


@games.route("/popular", methods=["GET"])
def get_popular_games():
    """returns popular games from API"""
    response = requests.get(
        "https://api.rawg.io/api/games?dates=2021-11-12%2C2022-11-12&key=da5a129d1222463594fe9081ecaac80a&ordering=-rating&page=2&page_size=10"
    ).json()
    return response


@games.route("/upcoming", methods=["GET"])
def get_upcoming_games():
    """return upcoming games from the API"""
    response = requests.get(
        "https://api.rawg.io/api/games?dates=2022-11-12%2C2023-11-12&key=da5a129d1222463594fe9081ecaac80a&ordering=-added&page=2&page_size=10"
    ).json()
    return response


@games.route("/new", methods=["GET"])
def get_new_games():
    """returns new games from the API"""
    response = requests.get(
        "https://api.rawg.io/api/games?dates=2021-11-12%2C2022-11-12&key=da5a129d1222463594fe9081ecaac80a&ordering=-released&page=2&page_size=10"
    ).json()
    return response


@games.route("/<searched>", methods=["GET"])
def search_games(searched):
    """returns games from API based off users' input"""
    searched = searched
    response = requests.get(
        "https://api.rawg.io/api/games?key=da5a129d1222463594fe9081ecaac80a&page_size=21&search=" + searched
    ).json()
    return response


def get_game_details(game_id):
    """returns details for a selected game"""
    details = f"{base_url}{game_details}{game_id}?key={key}"
    return details


def get_game_screenshots(game_id):
    """returns screenshots for a selected game"""
    screenshots = f"{base_url}{game_details}{game_id}{game_screenshots}?key={key}"
    return screenshots


def get_game_genres():
    """returns the genres of games"""
    genres = f"{base_url}{game_genres}?key={key}"
    return genres


def get_specific_genre(genre_id):
    """returns info from a specific genre"""
    a_genre = f"{base_url}{game_genres}/{genre_id}?key={key}"
    return a_genre


def get_specific_games_genre(genre_id):
    """returns games from a specific genre"""
    specific_genre = f"{base_url}{genre_games}{genre_id}&page-size=21"
    return specific_genre


def get_game_platforms():
    """returns platforms for games"""
    platforms = f"{base_url}{game_platforms}?key={key}"
    return platforms


def get_specific_platform(platform_id):
    """returns a specific gaming platform"""
    a_platform = f"{base_url}{game_platforms}/{platform_id}?key={key}"
    return a_platform


def get_specific_games_platform(platform_id):
    # uses digits, like 4, to mean 'PC'
    """returns games from a specific platform"""
    specific_platform = f"{base_url}{platform_games}{platform_id}&page_size=21"
    return specific_platform


def get_game_publishers():
    """returns publishers for games"""
    publishers = f"{base_url}{game_publishers}"
    return publishers


def get_specific_publisher(publisher_id):
    """returns a specific publisher"""
    a_publisher = f"{base_url}{game_publishers_page}/{publisher_id}?key={key}"
    return a_publisher


def get_specific_games_publisher(publisher_id):
    """returns specific games from a publisher"""
    specific_publisher = f"{base_url}{publisher_games}{publisher_id}&page_size=21"
    return specific_publisher


# headers = {
#     "x-rapidapi-key": "da5a129d1222463594fe9081ecaac80a",
#     "x-rapidapi-host": "rawg-video-games-database.p.rapidapi.com",
# }

# response = requests.request("GET", get_popular_games())

# print(response.text)
