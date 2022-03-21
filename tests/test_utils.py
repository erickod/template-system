import asyncio
from unittest import mock

from template_system.utils import remove_file


def test_remove_file_calls_remover_as_callable() -> None:
    remover = mock.Mock()
    asyncio.run(
        remove_file(
            "",
            time_in_seconds=0,
            remover=remover,
        )
    )
    remover.assert_called()
