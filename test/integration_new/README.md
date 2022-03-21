#Integration tests

To run integration tests locally you have to use a Box account with all possible scopes enabled.
For integration tests we use JWT authentication method. To use it download jwt settings file from
Developer Console and provide path to your config file in `integration_tests.cfg`.

To launch all integration tests locally run:
`pytest test/integration_new/object/*`
