# Usage

## Installation of the tool

```sh
$ pip install -e .[test]
```

## Installation of an application

### Login as platform admin

```sh
$ bonita platform login http://${BONITA_HOST}:8080/bonita platformAdmin platform
```

### Stop the platform

```sh
$ bonita platform stop
```

### Upload process

```sh
$ bonita upload process toto.bar
```

## Sample sessions

```sh
$ bonita session login http://$BONITA_HOST:8080/bonita install install
$ bonita session get
$ bonita system tenant get
$ bonita system tenant pause
$ bonita system tenant get
$ bonita system tenant resume
$ bonita session logout
$ bonita upload process ../release/process-1.0.6.bar 
$ bonita platform login http://$BONITA_HOST:8080/bonita platformAdmin platform
$ bonita platform get
$ bonita platform start
$ bonita platform stop
$ bonita platform logout
```

  