import logging


logger = logging.getLogger("mainApp")
logger.setLevel(logging.INFO)


logger_handler = logging.FileHandler('logfile.log')
logger_handler.setLevel(logging.INFO)


formatter = logging.Formatter(
	"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
	)

logger_handler.setFormatter(formatter)

logger.addHandler(logger_handler)