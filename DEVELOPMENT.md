# Developing Docker images

## Setting up for development

After cloning the repository you will need to clone the submodule:

```
git submodule update --init --force --recursive
```

You should also add the local githooks, which include checks for the generated
Bitbucket Pipelines configuration. This can be done with:

```
git config core.hooksPath .githooks
```

## Testing

The repository contains a smoke-test suite run on branch/PR builds and as part
of the release process. It uses `docker-compose` to run the image in production
mode with predefined database, and then run a suite of basic tests. *NOTE*: The
tests are not intended to test every aspect of the product, but to ensure basic
functionality works to a degree that we can be confident that there are no
regressions. See [func-tests/smoketests/src/](func-tests/smoketests/src/) for the actual tests run.

The default database was generated with the default sample project, but has had
the license elided for security reasons. See below for how to inject it.

### Pre-requisites

To run the functional testing, you are required to define several variables.

```
# String with full Jira DC license, don't forget the quotes as the license 
can contain special characters that would render the license unusable
JIRA_TEST_LICENSE='license_string' 

# The passwords used to access the product. These are stored in lastpass.
JIRA_USER_PWD='xxx'
JIRA_ADMIN_PWD='xxx'
```

### Run the smoke test functional suite

This will build a local image based on the latest Jira version and run the
func-tests against it:

```
export JIRA_VERSION=`curl -s https://marketplace.atlassian.com/rest/2/products/key/jira/versions/latest | jq -r .name`
docker build --build-arg JIRA_VERSION=${JIRA_VERSION} -t jira-test-image .
docker-compose build --build-arg TEST_TARGET_IMAGE=jira-test-image ./func-tests/docker-compose.yaml
./func-tests/run-functests jira-test-image
```

### Develop tests

Install packages

```
cd func-tests/smoketests
pipenv install
```

Run the smoke tests

```
cd func-tests
docker-compose up
export JIRA_ADMIN_PWD="passwordInLastpass"
export JIRA_BASEURL="http://localhost:2990/jira"
pipenv run pytest -v
```

### Release process

Releases occur automatically; see [bitbucket-pipelines.yml](bitbucket-pipelines.yml).
Due to the large amount of images that are built and tested the pipelines file
is generated from a template that parallelises the builds.  It includes a
self-check for out-of-date pipelines config. To avoid committing stale config it
is recommended you add the supplied pre-commit hook; see the setup section above.

It should be noted that a change to this repository will result in all published
images being regenerated with the latest version of the
[Dockerfile](Dockerfile). As part of the release process the following happens:

* A [Snyk](https://snyk.io) scan is run against the generated container image.
* The image dependencies are registered with Snyk for periodic scanning.
* The above func-test suite is run against the image.

This is all performed by the
[docker-release-maker](https://bitbucket.org/atlassian-docker/docker-release-maker/)
tool/image. See the
[README](https://bitbucket.org/atlassian-docker/docker-release-maker/src/master/README.md)
in that repository for more information.
