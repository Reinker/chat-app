from flask import Flask
app = Flask(__name__)

import chatapp.main
import chatapp.db.db
