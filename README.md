This repository reproduces a suspected bug causing issues with some Selenium
tests. This test will sporadically succeed or fail, because a click on a link
with a JS event handler is not triggering the script. Use the commands below to
download dependencies, build everything, and run the test.

This reduced test loads one page, navigates to another by clicking on a link,
waits for jQuery events to be registered, and clicks on a link with multiple
event handlers registered. Then, it fetches browser log entries, prints those,
and finally waits for a modal dialog to appear. When the test is successful,
three console.log messages should be seen from the various event handlers, the
wait for the modal dialog box will finish immediately, and the script will exit
successfully. When it is unsuccessful, no log messages will be seen, the wait
for the modal dialog box will time out, and the script will exit with an error.
The test tends to fail more often than it succeeds.

The browser can be monitored by connecting a VNC client to localhost:5900. When
the test fails, it seems that the click from the Selenium script has at least
caused the link to be focused, as its underline is visible while the wait is
running.

```bash
docker-compose build && docker-compose up
until docker exec -it test-case-web python test.py; do echo retry; done
```
