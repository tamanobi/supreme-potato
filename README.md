# prepare static server

```
$ python -m http.server  8088 --directory ./static/
```

```
$ uvicorn backend.main:app --host 0.0.0.0
```
