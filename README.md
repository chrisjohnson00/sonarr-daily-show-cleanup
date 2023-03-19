# sonarr-daily-show-cleanup
A script which keeps up the last N of any 'daily' episode shows in your library

## PyPi Dependencies

``` 
docker run -it --rm -v ${PWD}:/repo -w /repo python:3.11.2-slim bash
pip install --upgrade pip
pip install --upgrade pygogo requests
pip freeze > requirements.txt
sed -i '/pkg_resources/d' requirements.txt
```

## Running

```commandline
docker build . -t chrisjohnson00/sonarr-daily-show-cleanup

docker run --rm -e SONARR_HOST=http://192.168.1.131:8989 \
    -e SONARR_APIKEY=xxxx \
    -v /mnt/video/Television:/tv \
    --user 1000:1000 \
    chrisjohnson00/sonarr-daily-show-cleanup
```