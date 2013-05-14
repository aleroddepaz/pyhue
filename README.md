pyhue
=====

Python library for the Philips Hue personal lighting system.

Installation:
-------------

You can install pyhue with `pip install pyhue` or [download `pyhue.py`][1] and place it in your project directory.

Example
-------

```python
import pyhue

bridge = pyhue.Bridge('my_ip_address', 'my_username')
for light in bridge.lights:
	light.on = True
    light.hue = 0
```

Features
--------

- Object-oriented mapping of the RESTful interface.
- Major support of the v1.0 of the API: [Lights][2], [Groups][3], [Schedules][4].
- Conversion of basic color models.


See the complete documentation of the Philips Hue personal lighting system on <http://developers.meethue.com/>.

 [1]: http://raw.github.com/alexrdp90/pyhue/master/src/pyhue.py
 [1]: http://developers.meethue.com/1_lightsapi.html
 [2]: http://developers.meethue.com/2_groupsapi.html
 [3]: http://developers.meethue.com/3_schedulesapi.html
