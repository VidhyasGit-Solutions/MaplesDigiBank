from datetime import datetime

from flask import Blueprint, abort, redirect, render_template, request
from flask_login import current_user
from loguru import logger

applications = Blueprint("applications", __name__)


@applications.route("/home")
def home():
    logger.debug("Home")
    return render_template("home.html")


@applications.route("/applications", methods=["GET", "POST"])
def application():

    return render_template("applications.html")


@applications.route("/create_application", methods=["GET", "POST"])
def create_application():
    return render_template("create_application.html")
