#!/usr/bin/env python3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SELENIUM_TIMEOUT = 120


def main():
    options = webdriver.ChromeOptions()
    capabilities = options.to_capabilities()
    capabilities["loggingPrefs"] = {"browser": "INFO"}
    capabilities["goog:loggingPrefs"] = {"browser": "INFO"}
    driver = webdriver.Remote(
            "http://test-case-selenium:4444/wd/hub",
        desired_capabilities=capabilities
    )

    driver.get("http://test-case-web:8000/profile/favorites/")
    WebDriverWait(driver, SELENIUM_TIMEOUT).until(
        EC.presence_of_element_located((By.TAG_NAME, "html"))
    )

    WebDriverWait(driver, SELENIUM_TIMEOUT).until(
        lambda driver: driver.execute_script(
            "return $._data("
            "document.querySelector(\".edit-favorite-trigger\"), "
            "\"events\").click.length"
        )
    )

    edit_link = driver.find_element_by_link_text("Edit / Delete")
    div = edit_link.find_element(By.XPATH, "./parent::div")
    print("onclick: {}".format(div.get_attribute("onclick")))
    edit_link.click()
    time.sleep(1)
    log_entries = driver.get_log("browser")
    for entry in log_entries:
        print("console.log message: {}".format(entry["message"]))
    if not log_entries:
        print("no console.log messages")

    modal = driver.find_element_by_id("modal-save-favorite")
    WebDriverWait(driver, SELENIUM_TIMEOUT).until(
        EC.visibility_of(modal)
    )


if __name__ == "__main__":
    main()
