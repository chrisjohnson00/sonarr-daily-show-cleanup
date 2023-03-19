import requests
import re
import os
import pygogo as gogo

# logging setup
kwargs = {}
formatter = gogo.formatters.structured_formatter
logger = gogo.Gogo('struct', low_formatter=formatter).get_logger(**kwargs)


def main():
    logger.info("Starting")
    # Set up variables for Sonarr API
    sonarr_url = get_config('SONARR_HOST')
    sonarr_api_key = get_config('SONARR_APIKEY')
    # headers = {'X-Api-Key': sonarr_api_key}

    # Get list of shows that are set to air daily
    sonarr_daily_shows = []
    response = requests.get(f'{sonarr_url}/api/series?apikey={sonarr_api_key}')
    json_data = response.json()

    for show in json_data:
        if show['seriesType'] == 'daily':
            sonarr_daily_shows.append(show)

    logger.debug('Found the following daily shows', extra={'shows': sonarr_daily_shows})

    # For each daily show, get list of episode directories and delete all but the last 7
    for show in sonarr_daily_shows:
        show_id = show['id']
        show_title = show['title']
        show_files = []
        url = f'{sonarr_url}/api/v3/episode?seriesId={show_id}&includeImages=false'
        logger.info(f'Getting episodes for seriesId {show_id}', extra={'url': url})
        response = requests.get(f'{url}&apikey={sonarr_api_key}')
        json_data = response.json()

        for episode in json_data:
            if episode['hasFile']:
                episode_id = episode['id']
                url = f'{sonarr_url}/api/v3/episode/{episode_id}'
                logger.info(f'Getting episode {episode_id}', extra={'url': url})
                response = requests.get(f'{url}?apikey={sonarr_api_key}')
                episode_data = response.json()
                show_files.append(episode_data['episodeFile']['path'])

        logger.debug(f'Found files for {episode_id}', extra={'files': show_files})
        files_to_delete = get_old_files(show_files, 5)

        logger.debug(f'Will delete the following files for {episode_id}', extra={'files_to_delete': files_to_delete})
        # Delete files
        for file_path in files_to_delete:
            if os.path.isfile(file_path):
                logger.info("Deleting file", extra={'file_path': file_path})
                os.remove(file_path)

        logger.info(f'{show_title}: {len(files_to_delete)} episodes deleted')


def get_config(key):
    if os.environ.get(key):
        return os.environ.get(key)


def get_old_files(file_list, older_than_x_days):
    # Define regular expression pattern to find date strings in file names
    date_pattern = r"\d{4}-\d{2}-\d{2}"

    # Sort files by date
    file_list.sort(key=lambda x: re.search(date_pattern, x).group(0))

    # Get all files except the latest older_than_x_days
    old_files = file_list[:-older_than_x_days]

    return old_files


if __name__ == '__main__':
    main()
