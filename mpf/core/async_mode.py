"""Base class for asyncio modes."""
import abc
import asyncio
from typing import TYPE_CHECKING, Generator

from mpf.core.mode import Mode

if TYPE_CHECKING:   # pragma: no cover
    from mpf.core.machine import MachineController


class AsyncMode(Mode, metaclass=abc.ABCMeta):

    """Base class for asyncio modes."""

    def __init__(self, machine: "MachineController", config: dict, name: str, path: str) -> None:
        """Initialise async mode."""
        super().__init__(machine, config, name, path)

        self._task = None   # type: asyncio.Task

    def _started(self) -> None:
        """Start main task."""
        super()._started()

        self._task = self.machine.clock.loop.create_task(self._run())
        self._task.add_done_callback(self._done)

    def _done(self, future: asyncio.Future) -> None:
        """Evaluate result of task.

        Will raise exceptions from within task.
        """
        try:
            future.result()
        except asyncio.CancelledError:
            pass

        # stop mode
        self.stop()

    def _stopped(self) -> None:
        """Cancel task."""
        super()._stopped()

        self._task.cancel()

    @abc.abstractmethod
    @asyncio.coroutine
    def _run(self) -> Generator[int, None, None]:
        """Main task which runs as long as the mode is active.

        Overwrite this function in your mode.

        Its automatically canceled when the mode stops. You can catch CancelError to handle mode stop.
        """
        pass
