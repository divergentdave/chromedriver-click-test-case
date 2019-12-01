This repository reproduces a suspected bug causing issues with some Selenium
tests. This test will sporadically succeed or fail, because a click on a link
with a JS event handler is not triggering the script. Use the commands below to
download dependencies, build everything, and run the test.

```bash
docker-compose build && docker-compose up
until docker exec -it test-case-web python test.py; do echo retry; done
```
