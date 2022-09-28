# Documentation

<p align="center">
    <img src="https://user-images.githubusercontent.com/5860071/61949755-7dbca580-afb4-11e9-87b6-1187933cccfb.png" width="200" border="0" alt="rasa-model-server">
    <br/>
    <a href="https://github.com/vrachieru/rasa-model-server/releases/latest">
        <img src="https://img.shields.io/badge/version-1.2.0-brightgreen.svg?style=flat-square" alt="Version">
    </a>
    <br/>
    Simple webserver for externalizing RASA models.
</p>

## About

You can [configure RASA to fetch models](https://rasa.com/docs/rasa/user-guide/running-the-server/#fetching-models-from-a-server) from this server in two ways.

### Get a specific model

Pointing to a specific model (`.tar.gz`) and overriding said file when you want the model to change.
`http://localhost:8080/models/model.tar.gz`  

### Get the latest model

Pointing to a folder (suffixing the url with `@latest`) containing multiple models (`.tar.gz`) and getting the latest model sorted by modified date.
`http://localhost:8080/models/@latest`

### Upload a model

You can upload models via POST requests that you send during a CI/CD RASA model training job.
If you choose a model name that exists on the server, the new one overwrites the old one.

## Quick start

Build a Docker image from this repository.

```bash
docker build -t rasa-model-server .
```

Specify your desired configuration and run the container:

```bash
docker run -<d|i> --rm \
    -v /host/path/to/models:/app/models \
    -p <host_port>:8080 \
    rasa-model-server
```

You can stop the container using:

```bash
docker stop rasa-model-server
```

## Configuration

You can configure the service via the following environment variables.

| Environment Variable  | Default Value | Description                                             |
| --------------------- | ------------- | ------------------------------------------------------- |
| PORT                  | 8080          | Port on which to run the webserver.                     |
| MODELS_DIR            | models        | The absolute or relative location of the models folder. |

## Examples

### Get model

Fetch a model without specifying a `If-None-Match` header.

``` Bash
curl -s -I 'http://localhost:8080/models/model.tar.gz'

HTTP/1.0 200 OK
Content-Disposition: attachment; filename=model.tar.gz
Content-Length: 6478848
Content-Type: application/x-tar
Last-Modified: Tue, 23 Apr 2019 12:28:43 GMT
Cache-Control: public, max-age=43200
Expires: Fri, 26 Jul 2019 23:42:05 GMT
ETag: "1556022523.364716-6478848-1948524791"
Date: Fri, 26 Jul 2019 11:42:05 GMT
Accept-Ranges: bytes
Server: Werkzeug/0.14.1 Python/3.6.3
```

Once the model is loaded by RASA, subsequent requests will use the received ETAG to check if the model has been updated.

``` Bash
curl -s -I 'http://localhost:8080/models/model.tar.gz' -H 'If-None-Match: 1556022523.364716-6478848-1948524791'

HTTP/1.0 304 NOT MODIFIED
Content-Disposition: attachment; filename=model.tar.gz
Cache-Control: public, max-age=43200
Expires: Fri, 26 Jul 2019 23:42:48 GMT
ETag: "1556022523.364716-6478848-1948524791"
Date: Fri, 26 Jul 2019 11:42:48 GMT
Accept-Ranges: bytes
Server: Werkzeug/0.14.1 Python/3.6.3
```

Update the model on the server an the next request will pull the new model upon ETag mismatch.

``` Bash
curl -s -I 'http://localhost:8080/models/model.tar.gz' -H 'If-None-Match: 1556022523.364716-6478848-1948524791'

HTTP/1.0 200 OK
Content-Disposition: attachment; filename=model.tar.gz
Content-Length: 900
Content-Type: application/x-tar
Last-Modified: Sat, 29 Dec 2018 23:17:54 GMT
Cache-Control: public, max-age=43200
Expires: Fri, 26 Jul 2019 23:43:32 GMT
ETag: "1546125474.453404-900-1948524791"
Date: Fri, 26 Jul 2019 11:43:32 GMT
Accept-Ranges: bytes
Server: Werkzeug/0.14.1 Python/3.6.3
```

### Upload model

Upload a model to the server using a POST request.

``` Bash

curl -X POST -F "model=@model.tar.gz" -H "Content-Type: multipart/form-data" "http://localhost:8080/models/model.tar.gz"

```

## Roadmap

* Add security token to access the server's endpoints.
* Add a front end that supports all features in app.py
* Add tests for different requests to check if abort clauses trigger correctly.

## Change history

### 1.2.0

* Added model upload via POST request Stefan Wellsandt, BIBA - Bremer Institut für Produktion und Logistik GmbH
* Extended config.py file
* Updated deprecated parts related to Flask 2.1.0
* Adding some detailed comments
* Updated the readme file (e.g. added change history)

### 1.1.0

* Several updates by Guilherme Guy
* Added '..' path check to improve security by Daniel Gabardo

### 1.0.0

Initial version provided by Victor Rachieru with model download and model index (list)

## License

MIT
