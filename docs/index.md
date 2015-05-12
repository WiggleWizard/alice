Alice
=====

![Runs on Python 2.7.x](https://img.shields.io/badge/Python-2.7.x-brightgreen.svg)

Alice is a powerful CoD4 addon. It is the love child of GSC and B3/Manu. Alice can do things like this with just 8 lines of code:

![Chat filtering](http://i.imgur.com/U4IjUAg.gif)

```python
from system.base_plugin import BasePlugin

import re

class Plugin(BasePlugin):

	name     = 'ip_filter'
	name     = 'IP Chat Filter'
	version  = '1.0'

	def on_player_chat(self, player, message):
		return re.sub(r'[0-9]+(?:\.[0-9]+){3}', "^1[do not advertise]^7", message)
```

The magic behind Alice is WonderlandX which itself
a plugin for CoD4X17/18 server. So if you run/moderate a CoD4X server, you can simply drop WonderlandX into your CoD4X plugins folder and run an Alice addon.

Features
--------

- Lightning fast.
- Easy to write plugins for.
- Open source (all tech involved is open source).
- Event based/Asyncronous.
- Can be configured to run remotely. (TCP or IPC)
- No log/file parsing involved.
- Utilizes and abuses WonderlandX.
- Super low overhead.