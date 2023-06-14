# SrealityScraper

### Task:
> Use scrapy framework to scrape the first 500 items (title, image url) from sreality.cz (flats, sell) and save it in the Postgresql database. Implement a simple HTTP server in python and show these 500 items on a simple page (title and image) and put everything to single docker-compose command so that I can just run "docker-compose up" in the Github repository and see the scraped ads on http://127.0.0.1:8080 page.


### Idea:

0. Download and setup selenium chrome browser

1. Start the DB server
docker run --name some-postgres -e POSTGRES_PASSWORD=my_super_strong_password -d postgres

2. Run crawler to populate DB
cd sreality_scraper
scrapy crawl sreality

3. Run the server
cd ..
python3 web_server.py

### HOW TO:
Simply run `docker-compose up --build`
Visit 127.0.0.1:8080
(If nothing shows up, wait for the crawler to end)

------------------------------------

### SEE FILES INSIDE DOCKER CONTAINER:
`docker run --rm -it --entrypoint /bin/bash --volumes-from your-container-name your-image-name`


### HOW TO BUILD/MAKE AND RUN DOCKER:
`docker build -t your-image-name .`
`docker rm -f your-container-name # stop and remove old docker container`
`docker run -p 8080:8080 --name your-container-name your-image-name`


### DELETE OLD IMGS
`docker images # find ID`
`docker rmi IMG_ID_OR_NAME # force with -f`
`docker image prune  #(remove dangling (~ghosts) imgs)`


### How to run POSTGRESQL in docker
`docker run --name some-postgres -e POSTGRES_PASSWORD=my_super_strong_password -d postgres`
`psql -U postgres -h 127.0.0.1 password=my_super_strong_password`
`psql -U postgres -h 127.0.0.1 -c "ALTER USER postgres WITH PASSWORD 'my_super_strong_password';"`
`su -c "psql -h 127.0.0.1 -c \"ALTER ROLE postgres WITH LOGIN PASSWORD 'my_super_strong_password' \"" postgres`

TODO:
Add tests, change a bit docker-compose so it uses variables/environment such as DB connections, selenium directory, number of pages to scrape, running one shell file instead of two CMDs, etc., add a button to regenerate listings, generate a listing in browser (framework/js), not the server.
