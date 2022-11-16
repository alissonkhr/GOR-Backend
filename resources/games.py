import os, datetime, requests
from dotenv import load_dotenv

load_dotenv()

from flask import Blueprint

games = Blueprint("games", "games")


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


base_url = "https://api.rawg.io/api/"
key = os.environ.get("API_KEY")
current_year = get_current_year()
current_month = get_current_month()
current_day = get_current_day()
current_date = f"{current_year}-{current_month}-{current_day}"
last_year = f"{current_year - 1}-{current_month}-{current_day}"
next_year = f"{current_year + 1}-{current_month}-{current_day}"


@games.route("/popular", methods=["GET"])
def get_popular_games():
    """returns popular games from API"""
    response = requests.get(
        base_url
        + "games?dates="
        + last_year
        + ","
        + current_date
        + "&key="
        + key
        + "&ordering=-rating&page=2&page_size=10"
    ).json()
    return response


@games.route("/upcoming", methods=["GET"])
def get_upcoming_games():
    """return upcoming games from the API"""
    response = requests.get(
        base_url
        + "games?dates="
        + current_date
        + ","
        + next_year
        + "&key="
        + key
        + "&ordering=-added&page=2&page_size=10"
    ).json()
    return response


@games.route("/new", methods=["GET"])
def get_new_games():
    """returns new games from the API"""
    response = requests.get(
        base_url
        + "games?dates="
        + last_year
        + ","
        + current_date
        + "&key="
        + key
        + "&ordering=-released&page=2&page_size=10"
    ).json()
    return response


@games.route("/<searched>", methods=["GET"])
def search_games(searched):
    """returns games from API based off users' input"""
    response = requests.get(
        base_url + "games?key=" + key + "&page_size=21&search=" + searched
    ).json()
    return response


@games.route("/details/<game_id>", methods=["GET"])
def get_game_details(game_id):
    """returns details for a selected game"""
    response = requests.get(base_url + "games/" + game_id + "?key=" + key).json()
    return response


@games.route("/screenshots/<game_id>", methods=["GET"])
def get_game_screenshots(game_id):
    """returns screenshots for a selected game"""
    response = requests.get(
        base_url + "games/" + game_id + "/screenshots?key=" + key
    ).json()
    return response


@games.route("/genres", methods=["GET"])
def get_game_genres():
    """returns the genres of games"""
    response = requests.get(base_url + "genres?key=" + key).json()
    return response


@games.route("/genres/<genre_id>", methods=["GET"])
def get_specific_genre(genre_id):
    """returns info from a specific genre"""
    response = requests.get(base_url + "genres/" + genre_id + "?key=" + key).json()
    return response


@games.route("/genres/details/<genre_id>", methods=["GET"])
def get_specific_games_genre(genre_id):
    """returns games from a specific genre"""
    response = requests.get(
        base_url + "games?key=" + key + "&genres=" + genre_id + "&page-size=21"
    ).json()
    return response


@games.route("/platforms", methods=["GET"])
def get_game_platforms():
    """returns platforms for games"""
    response = requests.get(base_url + "platforms?key=" + key).json()
    return response


@games.route("/platforms/<platform_id>", methods=["GET"])
def get_specific_platform(platform_id):
    """returns a specific gaming platform"""
    response = requests.get(
        base_url + "platforms/" + platform_id + "?key=" + key
    ).json()
    return response


@games.route("/platforms/details/<platform_id>", methods=["GET"])
def get_specific_games_platform(platform_id):
    # uses digits, like 4, to mean 'PC'
    """returns games from a specific platform"""
    response = requests.get(
        base_url + "games?key=" + key + "&platforms=" + platform_id + "&page_size=21"
    ).json()
    return response


@games.route("/publishers", methods=["GET"])
def get_game_publishers():
    """returns publishers for games"""
    response = requests.get(base_url + "publishers?key=" + key + "&page_size=50").json()
    return response


@games.route("/publishers/<publisher_id>", methods=["GET"])
def get_specific_publisher(publisher_id):
    """returns a specific publisher"""
    response = requests.get(
        base_url + "publishers/" + publisher_id + "?key=" + key
    ).json()
    return response


@games.route("/publishers/details/<publisher_id>", methods=["GET"])
def get_specific_games_publisher(publisher_id):
    """returns specific games from a publisher"""
    response = requests.get(
        base_url + "games?key=" + key + "&publishers=" + publisher_id + "&page_size=21"
    ).json()
    return response
