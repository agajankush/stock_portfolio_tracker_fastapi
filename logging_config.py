import logging
import sys
import structlog

def setup_logging():
    """
    Correctly configures structured logging for the application.
    """
    # This is the shared processor chain for both standard and structlog loggers.
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=shared_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # --- This is the new, more robust setup for the standard logger ---
    
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Create a handler to output to the console
    handler = logging.StreamHandler(sys.stdout)
    
    # The ProcessorFormatter is the magic bridge that tells the standard
    # logger to use the structlog processors.
    formatter = structlog.stdlib.ProcessorFormatter(
        # These processors are run first by the standard logger
        foreign_pre_chain=[structlog.stdlib.ExtraAdder()],
        # These are the shared processors that render the final log
        processors=shared_processors,
    )
    
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)