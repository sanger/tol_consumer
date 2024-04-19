# Modifying Schemas Managed By RedPanda

## Current Best Method Since April 2024

Each instance of RedPanda has a an admin web console which lets you take all actions on schemas in a visual editor.
The console can be accessed by appending `/console/` to the base URL of the RedPanda instance.
It will require authentication which can be found in the team password vault.
Only the Schema Registry section should be used in the console as we are not using the other parts of RedPanda.

## Legacy Methods

In order to perform create, update and delete actions on schemas via the API the restriction on HTTP methods will need to be lifted on the RedPanda instance.
This is a config option in nginx that restricts methods to just HEAD and GET when PUSH is needed to write schemas.
It is recommended the config is not changed, as this can cause security issues for the schemas.

### Create and Update Schemas

1. Ensure `jq` is installed:

    ```shell
    brew install jq
    ```

1. Run the command:

    ```shell
    push.sh <REDPANDA_URL>
    ```

    where:

    ```text
    <REDPANDA_URL>: URL to connect to RedPanda where the schemas will be uploaded
    ```

### Remove Schemas

Run the command:

```shell
remove_all.sh <REDPANDA_URL>
```

where:

```text
<REDPANDA_URL>: URL to connect to RedPanda where the schemas will be uploaded
```
