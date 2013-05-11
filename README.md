pyhue
=====

Python library for the Philips Hue personal lighting system.

Installation:
-------------

You can install pyhue with `pip install pyhue` or [download `pyhue.py`](https://raw.github.com/alexrdp90/pyhue/master/src/pyhue.py) and place it in your project directory.

Example
-------

```python
import pyhue

bridge = pyhue.Bridge('my_ip_address', 'my_username')
for light in bridge.lights:
	light.on = True
    light.hue = 0
```

See the complete documentation of the Philips Hue personal lighting system on <http://developers.meethue.com/>.