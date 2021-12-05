import requests, json
from . import readConfig
from rich.table import Table, Column
from rich.console import Console
import rich

console = Console()

config = readConfig.config_read()

url = 'https://graphql.anilist.co'

ANIME_SEARCH_QUERY = """
query($id: Int, $page: Int, $per_page: Int, $search: String) {
    Page(page: $page, perPage: $per_page) {
        media(id: $id, search: $search, type: ANIME, sort: POPULARITY_DESC) {
            id
            title {
                romaji
                english
                native
            }
            episodes
            studios {
                nodes {
                    name
                }
            }
            season
            status
            seasonYear
            format
            genres
        }
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
    }
}
"""

CHARACTER_SEARCH_QUERY = """
query($per_page: Int, $page: Int, $search: String) {
    Page(page: $page, perPage: $per_page) {
        characters(search: $search) {
            id
            name {
                first
                full
                native
                last
            }
            age
            gender
            dateOfBirth {
                year
                month
                day
            }
        }
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
    }
}
"""

MANGA_SEARCH_QUERY = """
query($id: Int, $page: Int, $per_page: Int, $search: String) {
    Page(page: $page, perPage: $per_page) {
        media(id: $id, search: $search, type: MANGA, sort: POPULARITY_DESC) {
            id
            title {
                romaji
                english
                native
            }
            chapters
            status
            genres
            characters(sort: FAVOURITES_DESC) {
                edges {
                    node {
                        name {
                            first
                            full
                            native
                            last
                        }
                        id
                    }
                    role
                }
            }
            volumes
        }
        pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
        }
    }
}
"""

def search_anime(name, page=1, perPage=config['per_page']):

    variables = {
            'search': name,
            'page': page,
            'per_page': perPage
            }

    response = json.loads(requests.post(url, json={'query': ANIME_SEARCH_QUERY, 'variables': variables}).text)

    media = response['data']['Page']['media']

    table = Table(show_header=True, header_style='bold cyan')
    table.add_column("Title", style='dim', justify='left')

    if config['anime_show_season'] : 
        table.add_column("Season", style='dim', width=11)
    if config['anime_show_episode'] : 
        table.add_column("EP", style='dim', width=3)
    if config['anime_show_status'] : 
        table.add_column("Status", style='dim', width=9)
    if config['anime_show_format'] : 
        table.add_column("Format", style='dim', width=6)
    if config['anime_show_studio'] : 
        table.add_column("Studio", style='dim')
    if config['anime_show_genres'] : 
        table.add_column("Genre", style='dim')

    for i in range(perPage):
        if i == len(media):
            break

        anime = media[i]

        data = {
                'Name'         : anime['title'][config['title_language']],
                'episodeCount' : str(anime['episodes']),
                'genre'        : ', '.join(anime['genres']),
                'format'       : anime['format'],
                'season'       : 'No data'  if anime['season']                == None else anime['season'].lower() + ' ' + str(anime['seasonYear']),
                'status'       : 'Finished' if anime['status']                == 'FINISHED' else '[italic red]Ongoing[/italic red]',
                'studio'       : 'No data'  if not len(anime['studios']['nodes']) else anime['studios']['nodes'][0]['name'],
                } 

        table_data = (
                data['Name'],
                )
        if config['anime_show_season']: 
            table_data += data['season'],
        if config['anime_show_episode']: 
            table_data += data['episodeCount'],
        if config['anime_show_status']: 
            table_data += data['status'],
        if config['anime_show_format']: 
            table_data += data['format'],
        if config['anime_show_studio']: 
            table_data += data['studio'],
        if config['anime_show_genres']: 
            table_data += data['genre'],

        table.add_row(*table_data)  #adding data to row

    console.print(table)
    print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")

def search_manga(name, page=1, perPage=config['per_page']):
    variables = {
            'search': name,
            'page': page,
            'per_page': perPage
            }
    response = json.loads(requests.post(url, json={'query': MANGA_SEARCH_QUERY, 'variables': variables}).text)
    media = response['data']['Page']['media']
    table = Table(show_header=True, header_style='bold cyan')
    table.add_column("Title", style='dim', justify='left')

    if config['manga_show_chapter'] : 
        table.add_column("Chapters", style='dim', width=3)
    if config['manga_show_volume'] : 
        table.add_column("Volumes", style='dim', width=3)
    if config['manga_show_status'] : 
        table.add_column("Status", style='dim', width=9)
    if config['manga_show_genres'] : 
        table.add_column("Genres", style='dim', justify='right')

    for i in range(perPage):
        if i == len(media):
            break

        manga = media[i]

        data = {
                'Name'         : manga['title'][config['title_language']],
                'chapterCount' : str(manga['chapters']),
                'genre'        : ', '.join(manga['genres']),
                'status'       : 'Finished' if manga['status'] == 'FINISHED' else '[italic red]Ongoing[/italic red]',
                'volume'       : str(manga['volumes'])
                } 

        table_data = (
                data['Name'],
                )
        if config['manga_show_chapter']: 
            table_data += data['chapterCount'],
        if config['manga_show_volume'] : 
            table_data += data['volume'],
        if config['manga_show_status'] : 
            table_data += data['status'],
        if config['manga_show_genres'] : 
            table_data += data['genre'],

        table.add_row(*table_data)

    console.print(table)
    print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")

def search_char(name, page=1, perPage=config['per_page']):
    variables = {
            'search': name,
            'page': page,
            'per_page': perPage
            }
    response = json.loads(requests.post(url, json={'query': CHARACTER_SEARCH_QUERY, 'variables': variables}).text)
    charList = response['data']['Page']['characters']
    table = Table(show_header=True, header_style='bold cyan')
    table.add_column("Name", style='dim', justify='left')
    if config['char_show_age'] : 
        table.add_column("Age", style='dim', width=6)   
    if config['char_show_gender'] : 
        table.add_column("Gender", style='dim', width=6)
    if config['char_show_birthdate'] : 
        table.add_column("Birthdate", style='dim', width=11)

    for i in range(perPage):
        if i == len(charList):
            break
        char = charList[i]

        data = {
                'Name'      : char['name'][config['char_name_format']],
                'age'       : char['age'],
                'gender'    : char['gender'],
                'birthdate' : f"{char['dateOfBirth']['day']}/{char['dateOfBirth']['month']}/{char['dateOfBirth']['year']}" if char['dateOfBirth']['day'] != None else 'No data'
                } 

        table_data = (data['Name'],)

        if config['char_show_age']: 
            table_data += data['age'],
        if config['char_show_gender'] : 
            table_data += data['gender'],
        if config['char_show_birthdate'] : 
            table_data += data['birthdate'],

        table.add_row(*table_data)

    console.print(table)
    print(f"page {response['data']['Page']['pageInfo']['currentPage']} of {response['data']['Page']['pageInfo']['lastPage']}")
