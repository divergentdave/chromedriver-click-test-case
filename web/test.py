#!/usr/bin/env python3
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SELENIUM_TIMEOUT = 30


def main():
    options = webdriver.ChromeOptions()
    capabilities = options.to_capabilities()
    capabilities["loggingPrefs"] = {"browser": "INFO"}
    capabilities["goog:loggingPrefs"] = {"browser": "INFO"}
    driver = webdriver.Remote(
        "http://test-case-selenium:4444/wd/hub",
        desired_capabilities=capabilities
    )

    try:
        old_page = driver.find_element_by_tag_name("html")
        driver.get("http://test-case-web:8000/?page=1")
        WebDriverWait(driver, SELENIUM_TIMEOUT).until(
            EC.staleness_of(old_page)
        )

        profile_dropdown = driver.find_element_by_css_selector(
            "a.dropdown-toggle"
        )
        dropdown_menu = driver.find_element_by_css_selector("ul.dropdown-menu")
        profile_dropdown.click()
        WebDriverWait(driver, SELENIUM_TIMEOUT).until(
            EC.visibility_of(dropdown_menu)
        )
        favorites = driver.find_element_by_link_text("Favorites")
        old_page = driver.find_element_by_tag_name("html")
        favorites.click()
        WebDriverWait(driver, SELENIUM_TIMEOUT).until(
            EC.staleness_of(old_page)
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
        print("onclick attribute: {}".format(div.get_attribute("onclick")))
        edit_link.click()
        time.sleep(1)
        log_entries = driver.get_log("browser")
        for entry in log_entries:
            message = entry["message"]
            if "touch-icon-192x192.png" not in message:
                print("console.log message: {}".format(message))
        if not log_entries:
            print("no console.log messages")

        modal = driver.find_element_by_id("modal-save-favorite")
        WebDriverWait(driver, SELENIUM_TIMEOUT).until(
            EC.visibility_of(modal)
        )

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
