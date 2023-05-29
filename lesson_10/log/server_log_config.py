from pathlib import Path
import logging.handlers
import logging
import sys

home_path = Path().cwd()
log_path = home_path / "lesson_10" / "log" / "server.log"

hand = logging.StreamHandler(sys.stderr)
hand.setLevel(logging.ERROR)
format = logging.Formatter("%(asctime)s %(levelname)s %(filename)-10s %(message)s")
hand.setFormatter(format)
# For file
client_log_hand = logging.handlers.TimedRotatingFileHandler(
    log_path, when="midnight", encoding="utf-8"
)
client_log_hand.setFormatter(format)
# For parenting all loggers
client_log = logging.getLogger("server")
client_log.setLevel(logging.DEBUG)
client_log.addHandler(client_log_hand)
client_log.addHandler(hand)
