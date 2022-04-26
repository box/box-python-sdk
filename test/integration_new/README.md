# Integration Tests

## Running integration tests locally

### Create Custom Application
To run integration tests locally you will need a `Custom App` created at https://cloud.app.box.com/developers/console
with `Server Authentication (with JWT)` selected as authentication method.
Once created you can edit properties of the application:
- In section `App Access Level` select `App + Enterprise Access`. You can enable all `Application Scopes`.
- In section `Advanced Features` enable `Make API calls using the as-user header` and `Generate user access tokens`.

Now select `Authorization` and submit application to be reviewed by account admin.


### Export configuration

There are two ways to set up JWT configuration:
1. First method:
- Select `Configuration` tab and in the bottom in the section `App Settings`
   download your app configuration settings as JSON.
- Specify the path to the JWT config file in `integration_tests.cfg`, e.g. `ConfigFilePath = /Users/me/jwt-config.json`
2. Alternatively:
- Select `Configuration` tab and in the bottom in the section `App Settings`
  download your app configuration settings as JSON.
- Encode configuration file to Base64, e.g. using command: `base64 -i path_to_json_file`
- Set environment variable: `JWT_CONFIG_BASE_64` with base64 encoded jwt configuration file

### Running Tests

You can run all tests (unit in all supported python environments and integration) using command:
```bash
tox
```

To run only integration tests, you can run:
```bash
tox -e integration-tests
```
