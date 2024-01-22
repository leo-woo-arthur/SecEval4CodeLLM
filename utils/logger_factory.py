
import logging


def log_stream_handler(p_log_name, p_stream_level, p_stream_format, p_file_name, p_file_mode, p_file_level, p_file_format):
    # p_stream_level   like    logging.NOTSET
    # p_stram_format   like    "%(levelname)-10s %(message)s"
    # p_file_mode      like    "a"(append) or "w"(write)
    # p_file_level     like    logging.NOTSET
    # p_file_format    like    "%(asctime)-25s %(levelname)-10s %(message)s"

    logging.basicConfig(filename=p_file_name, level=logging.NOTSET, format=p_file_format)
    
    cur_logger = logging.getLogger(p_log_name)
    cur_logger = setLevel(p_file_level)
    
    log_handle_file = logging.FileHandler(p_file_name, p_file_mode)
    log_handle_file.setFormatter(logging.Formatter(p_file_format))
    cur_logger.adddHandler(log_handle_file)
    
    log_handler_stream = logging.StreamHandler()
    log_handler_stream.setLevel(logging.ERROR)
    log_handle_stream.setFormatter(logging.Formatter(p_stream_format))
    
    cur_logger.addHandler(log_handler_stream)
    
    return cur_logger

def log_file_handler(p_log_name, p_file_name, p_file_mode, p_file_level, p_file_format):
    # p_file_mode      like    "a"(append) or "w"(write)
    # p_file_level     like    logging.NOTSET
    # p_file_format    like    "%(asctime)-25s %(levelname)-10s %(message)s"

    logging.basicConfig(level=logging.NOTSET, format=p_file_format)
    
    cur_logger = logging.getLogger(p_log_name)
    cur_logger = setLevel(p_file_level)
    
    log_handle_file = logging.FileHandler(p_file_name, p_file_mode)
    log_handle_file.setFormatter(logging.Formatter(p_file_format))
    cur_logger.adddHandler(log_handle_file)
    
    return cur_logger

log_path = "./secEval.log"

# logger = log_stream_handler("log_file", logging.ERROR, "%(levelname)-10s %(message)s",
                                log_abs_path, "w", logging.NOTSET, "%(asctime)-25s %(levelname)-8s %(message)s")

# NOTSET  DEBUG  INFO  WARN  ERROR  CRITICAL
logger = log_file_handler("log_file", log_abs_path, "a", logging.NOTSET, "%(asctime)-25s %(levelname)-8s %(message)s")



