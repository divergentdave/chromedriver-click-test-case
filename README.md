This repository reproduces a suspected bug causing issues with some Selenium
tests. This test will sporadically succeed or fail, because a click on a link
with a JS event handler is not triggering the script. Use the following
commands to download dependencies, build everything, and run the test.

```bash
docker build -t chrome-bisect-environment .
docker run --rm -it --name bisect chrome-bisect-environment /usr/bin/supervisord --configuration /etc/supervisord.conf &
docker exec -it bisect /opt/scripts/bisect-builds.py --archive=linux64 --use-local-cache --verify-range --good=681094 --bad=693954 '--command=/opt/scripts/harness.py'
TODO: add --not-interactive once the harness is working properly and I can reproduce the issue
```

This reduced test loads one page, navigates to another by clicking on a link,
waits for jQuery events to be registered, and clicks on a link with multiple
event handlers registered. Then, it fetches browser log entries, prints those,
and finally waits for a modal dialog to appear. When the test is successful,
three console.log messages should be seen from the various event handlers, the
wait for the modal dialog box will finish immediately, and the script will exit
successfully. When it is unsuccessful, no log messages will be seen, the wait
for the modal dialog box will time out, and the script will exit with an error.
The test tends to fail more often than it succeeds.

The browser can be monitored by forwarding port 5900 with `-p 5900:5900`,
running `/opt/bin/start-fluxbox.sh` and `/opt/bin/start-vnc.sh` inside the
container, and connecting a VNC client to localhost:5900. When the test fails,
it seems that the click from the Selenium script has at least caused the link
to be focused, as its underline is visible while the wait is running.
