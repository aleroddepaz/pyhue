pyhue
=====

Python library for the Philips Hue personal lighting system

**Basic usage:**

```python
import pyhue

bridge = pyhue.Bridge('my_ip_address', 'my_username')
for light in bridge.lights:
	light.on = True
    light.hue = 0
```

See the complete documentation of the Philips Hue personal lighting system on <http://developers.meethue.com/>.