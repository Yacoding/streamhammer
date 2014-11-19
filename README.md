streamhammer
============

Hammer on a video streaming service.  Intended to be used as a load/stress test tool.


Usage
-----

`start 10` clients `every 1000` milliseconds (1 second) capping out at `max 100` clients.

```bash
./bin/streamhammer --start 10 --every 1000 --max 100 --metadata http://domain.com/metadata.json
```
