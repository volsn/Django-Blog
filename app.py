import sys
import logging
from miloblog import app

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

if __name__ == '__main__':
    app.run(debug=True)
