import logging
from unittest.mock import patch

from ml.logger.logging_utils import get_logger


@patch("ml.logger.logging_utils.coloredlogs.install")
def test_get_logger(mocked_install):
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_logger"

    mocked_install.assert_called_once_with(
        level="INFO",
        logger=logger,
        fmt="%(asctime)s %(name)s %(levelname)s: %(message)s",
    )
