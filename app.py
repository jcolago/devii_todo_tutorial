from flask import Flask, render_template, request, redirect, url_for
import graphql_helper
import json

app = Flask (__name__)