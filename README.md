Mission Pinball Framework (MPF)
===============================

<img align="center" height="146" src="https://missionpinball.org/latest/images/mpf-logo-full.png"/>

<em>...Let's build a pinball machine!</em>

What is special here ?
----------------------

This was forked mainly for my Fast Draw / Quick Draw EM project. A few modifications were directly merged on the original project, 
some others were refused, and some may not be useful (or considered too dirty) to be included in mainstream.

Score reel management:

- add an overflow light when score exceeds reel group capacity
- mute the chime when resetting scores.

OPP / DMD support:

- Few changes to allow a DMD with OPP platform

For details, see `git log --author="Marc Rechté"`.


On this same account, one will find the forked mpf-mc required to implement DMD.

One will also require the following components on my gitlab account:

- [DMD server](https://gitlab.com/mrechte/dmd-server2) to drive the DMD
- [OPP](https://gitlab.com/mrechte/open-pinball-project) the platform hardware and firmware

Finaly the Fastdraw / Quickdraw projects may be found on:

- [Fastdraw MPF config](https://gitlab.com/mrechte/fastdraw_mpf)
- [Fastdraw OPP config](https://gitlab.com/mrechte/fastdraw_opp)
- [Quickdraw MPF config](https://gitlab.com/mrechte/quickdraw_mpf)
- [Quickdraw OPP config](https://gitlab.com/mrechte/quickdraw_opp)

What is Mission Pinball Framework?
----------------------------------

Mission Pinball Framework (MPF) is open source, cross-platform software for powering real pinball
machines. MPF is a community-developed project released under the MIT license. It's supported by volunteers in their spare time.

[![Coverage Status](https://coveralls.io/repos/missionpinball/mpf/badge.svg?branch=dev&service=github)](https://coveralls.io/github/missionpinball/mpf?branch=dev)
[![Test Status](https://github.com/missionpinball/mpf/actions/workflows/run_tests.yml/badge.svg)](https://github.com/missionpinball/mpf/actions/workflows/run_tests.yml)
[![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/1687/badge)](https://bestpractices.coreinfrastructure.org/projects/1687)

Visit the MPF project homepage at https://missionpinball.org. Additional related projects exist as part of the MPF ecosystem, including the "MPF Monitor" which is a graphical application that lets you simulate pinball hardware, and "MPF-MC" which is a media controller which provides graphics and sounds for pinball machines.

Documentation
-------------

* User Docs (installation, tutorials, & reference): https://missionpinball.org

Support
-------

MPF is an open source community project which has no official support. Some MPF users participate in the MPF-Users Google group or GitHub Discussion. Links [here](https://missionpinball.org/latest/community/).

Individual pinball hardware companies may provide additional support for users of their hardware, often via their own Slack, Discord, or other chat groups. If you get stuck, you can ask for help in the MPF-users group, or you reach out to your hardware provider.

Maintenance, Pull Requests, & Bug Fixes
---------------------------------------

As a community project, we welcome pull requests and bug fixes. However, we do not have the resources to provide support for MPF. If you are interested in becoming a maintainer, please contact us at brian@missionpinball.org.

Bugs or other issues related to MPF itself can be posted to the [MPF Discussions page on GitHub](https://missionpinball.org/latest/community/).

Contributing
------------

Individual pinball hardware makers are responsible for their own platform interface maintenance and contributions.

MPF is a passion project created and maintained by volunteers. If you're a Python coder, documentation writer, or pinball maker, feel free to make a change and submit a pull request. For more information about contributing see the [Contributing Code](https://missionpinball.org/latest/about/contributing_to_mpf/)
and [Contributing Documentation](https://missionpinball.org/latest/about/help_docs/) pages.

License
-------

MPF and related projects are released under the MIT License. Refer to the LICENSE file for details. Docs are released under Creative Commons CC BY 4.0.
