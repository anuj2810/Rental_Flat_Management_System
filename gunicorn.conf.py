# gunicorn.conf.py
import multiprocessing

# bind to all interfaces on port 8000 (Render uses this)
bind = "0.0.0.0:8000"

# workers: reasonable default using CPU count
workers = max(2, multiprocessing.cpu_count() * 2 + 1)

# request timeout (seconds)
timeout = 120

# send logs to stdout/stderr so Render captures them
errorlog = "-"
accesslog = "-"
loglevel = "info"

# don't write a pidfile (avoid 'logs doesn't exist' errors)
pidfile = None
