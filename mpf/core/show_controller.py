"""Contains the ShowController base class."""
from mpf.assets.show import Show, ShowConfig, ShowPool
from mpf.core.mpf_controller import MpfController


class ShowController(MpfController):

    """Manages all the shows in a pinball machine.

    The ShowController handles priorities, restores, running and stopping
    shows, etc.

    """

    __slots__ = ["show_players", "_next_show_id"]

    config_name = "show_controller"

    def __init__(self, machine):
        """initialize show controller.

        Args:
        ----
            machine: Parent machine object.
        """
        super().__init__(machine)

        self.show_players = {}
        self._next_show_id = 0

        self.machine.events.add_handler('init_phase_1', self._initialize, priority=10)
        self.machine.events.add_handler('init_phase_3', self._load_shows)
        self.machine.shows = dict()

    def _initialize(self, **kwargs):
        del kwargs
        show_names = self.machine.mpf_config.get_shows()
        for show_name in show_names:
            self.register_show(show_name)

        self._create_show_pool(config=self.machine.config)

        # Create the mode assets
        for mode in self.machine.modes.values():
            self._create_show_pool(config=mode.config)

    def _load_shows(self, **kwargs):
        del kwargs
        show_names = self.machine.mpf_config.get_shows()
        for show_name in show_names:
            self.log.debug("Loading show: %s", show_name)
            show_config = self.machine.mpf_config.get_show_config(show_name)
            self.machine.shows[show_name].load(show_config)

    def _create_show_pool(self, config):
        for show_pool_name, show_pool_config in config.get("show_pools", {}).items():
            self.machine.shows[show_pool_name] = ShowPool(self.machine, show_pool_name, show_pool_config, Show)

    def get_next_show_id(self):
        """Return the next show id."""
        self._next_show_id += 1
        return self._next_show_id

    def register_show(self, name):
        """Register a named show."""
        if name in self.machine.shows:
            raise ValueError("Show named '{}' was just registered, but "
                             "there's already a show with that name. Shows are"
                             " shared machine-wide".format(name))

        self.debug_log("Registering show: {}".format(name))
        self.machine.shows[name] = Show(self.machine,
                                        name=name)

    # pylint: disable-msg=too-many-arguments
    # pylint: disable-msg=too-many-locals
    def create_show_config(self, name, priority=0, speed=1.0,
                           loops=-1, sync_ms=None, manual_advance=False, show_tokens=None,
                           events_when_played=None, events_when_stopped=None,
                           events_when_looped=None, events_when_paused=None,
                           events_when_resumed=None, events_when_advanced=None,
                           events_when_stepped_back=None, events_when_updated=None,
                           events_when_completed=None):
        """Create a show config."""
        if sync_ms is None:
            sync_ms = self.machine.config['mpf']['default_show_sync_ms']
        return ShowConfig(name, int(priority), float(speed), int(loops), int(sync_ms), bool(manual_advance),
                          show_tokens, events_when_played, events_when_stopped, events_when_looped,
                          events_when_paused, events_when_resumed, events_when_advanced,
                          events_when_stepped_back, events_when_updated, events_when_completed)

    # pylint: disable-msg=too-many-arguments
    def replace_or_advance_show(self, old_instance, config: ShowConfig, start_step, start_time=None,
                                start_running=True, stop_callback=None):
        """Replace or advance show.

        Compare a given show (may be empty) to a show config and ensure that the new config becomes effective.
        If the old show runs a config which is equal to the new config nothing will be done.
        If the old_instance is set to manual_advance and one step behind the target step it will advance the show.
        Otherwise, the old show is stopped and the new show is stopped in sync.
        """
        start_callback = None
        if old_instance and not old_instance.stopped:
            if stop_callback or config.events_when_played or config.events_when_stopped:
                # would break things which rely on this. could be implemented here
                pass
            elif old_instance.show_config != config:
                # show_config changed so show needs to be replaced
                pass
            elif start_step is None and not config.manual_advance:
                return old_instance
            # this is an optimization for the case where we only advance a show or do not change it at all
            elif old_instance.current_step_index is not None and \
                    old_instance.current_step_index + 1 == start_step:
                # the show already is at the target step
                return old_instance
            elif old_instance.current_step_index is not None and \
                    old_instance.current_step_index + 2 == start_step:
                # advance show to target step
                old_instance.advance()
                return old_instance
            # in all other cases stop the current show
            if config.sync_ms:
                # stop current show in sync with new show
                start_callback = old_instance.stop
            else:
                # stop the current show instantly
                old_instance.stop()
        try:
            show_obj = self.machine.shows[config.name]
        except KeyError:
            raise KeyError("Cannot play show '{}'. No show with that "
                           "name.".format(config.name))

        return show_obj.play_with_config(
            show_config=config,
            start_time=start_time,
            start_step=start_step if start_step else 1,
            start_running=start_running,
            stop_callback=stop_callback,
            start_callback=start_callback
        )

    def play_show_with_config(self, config, mode=None, start_time=None):
        """Play and return a show from config.

        Will add the mode priority if a mode is passed.
        """
        show = self.machine.shows[config['show']]
        priority = config['priority'] + mode.priority if mode else config['priority']
        running_show = show.play(priority=priority, speed=config['speed'],
                                 start_step=config['start_step'], loops=config['loops'],
                                 sync_ms=config['sync_ms'], manual_advance=config['manual_advance'],
                                 show_tokens=config['show_tokens'], start_time=start_time)

        return running_show
