from flask import render_template, redirect, request, session
import secrets

def wrong_login(e):
    token = secrets.token_hex(16)
    session['csrf_token'] = token
