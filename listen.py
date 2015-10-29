import time

from flask import Flask, request, url_for, render_template, json

import scrape

webapp = Flask(
    __name__
)
light_vals = []
last_scrape_attempt = None


@webapp.route("/seamless/send_light/<val>", methods=["GET"])
def get_light(val):
    intval = int(val)
    light_vals.append(intval)
    do_food_check()
    print "got a val of %s" % intval
    return "ok, got it, thanks"


def do_food_check():
    if len(light_vals) > 4:
        average_last_2 = sum(light_vals[-2:]) / 2
        average_before_that = sum(light_vals[-4:-2]) / 2
        print "Avg went from %s to %s" % (average_before_that, average_last_2)
        if average_last_2 - average_before_that > 150:
            print "LIGHT CHANGE!"
            order_food()


def order_food():
    global last_scrape_attempt
    if last_scrape_attempt:
        time_since = int(time.time()) - last_scrape_attempt
        # Make sure we wait a long time between orders
        # Don't want it to go haywire
        if time_since < 300 * 60:
            print "TOO SOON! ABORTING!"
            return False
    last_scrape_attempt = int(time.time())
    scrape.reorder_most_recent()
    

if __name__ == "__main__":
    webapp.config["DEBUG"] = True
    webapp.run("0.0.0.0", port=6789)


