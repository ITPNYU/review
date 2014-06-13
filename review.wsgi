import sys

activate_this = '/var/www/dev/review/venv/review-v1/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/dev/review/review')

from review import app as application
