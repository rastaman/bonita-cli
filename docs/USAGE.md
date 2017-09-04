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
$ bonita process deploy tmp_9184139940101600952.bar
{
 "actorinitiatorid": "1", 
 "displayDescription": "", 
 "displayName": "xxx process", 
 "description": "", 
 "configurationState": "UNRESOLVED", 
 "deployedBy": "-1", 
 "version": "1.0.6", 
 "last_update_date": "1970-01-01 00:00:00.000", 
 "activationState": "DISABLED", 
 "deploymentDate": "2017-09-04 09:46:40.321", 
 "id": "5627990631861392806", 
 "name": "xxxx"
}
$ bonita process get 5627990631861392806
$ bonita process enable 5627990631861392806
```
