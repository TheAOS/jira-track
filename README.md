# jira-track
tracks wip limit in jira

# usage
set up a config file based on `config.example.json` and then
init Tracker with the path to your config file and a pass and fail callback and call run

```python
track = Tracker('config.json', pass_callback, fail_callback)
track.run()
```