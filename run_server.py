"""Start a animation of the Duckmodel in the webbrowser."""
from server import server
server.port = 8521
server.verbose = False #dont print every message
server.launch()
