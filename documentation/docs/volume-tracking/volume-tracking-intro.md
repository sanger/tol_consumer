# Process and Introduction

When samples are used up by runs through libraries and pools, a proper tracking process in terms of volume is required in order to assert the possibility of re-sequencing. Therefore, library and pool volumes used by runs needs be tracked and published to an accessible data store to be later accessed for _volume checks_.

!!! question "Volume Check"

    A _volume check_ is a comparison between the remaining volume and the volume required.

    $$
    V_{required} < V_{original} - V_{used}
    $$

    Above equation describes the concept of volume check, where $V_{original}$ represents the original volume in a library/pool, and $V_{used}$ represents the volume of the library/pool already used. If the condition displayed in the above equation is satisfied, the volume check returns `true`.

## Types of aliquots

This process is assisted by a model that contains the following type of aliquots.

1. `primary` aliquots.
2. `derived` aliquots.

`primary` aliquot records contain ^^initial^^ (i.e., original) volume of a library or a pool. Each time a library or a pool is used (e.g., in a sequencing run) a derived aliquot is created with the used volume and other details such as which type of an entity that used it (e.g, a run). Aliquot schema is as follows.

<center>

| **Attribue**      | **Type**        | **Description**                                          | **Values**            |
|-------------------|-----------------|----------------------------------------------------------|-----------------------|
| `id_lims`         | `varchar(255)`  | The LIMS system that the aliquot was created in          | `Traction`            |
| `aliquot_uuid`    | `varchar(255)`  | The UUID of the aliquot in the LIMS system               |                       |
| `aliquot_type`    | `varchar(255)`  | The type of the aliquot                                  | `primary`, `derived`  |
| `source_type`     | `varchar(255)`  | The type of the source of the aliquot                    | `library`, `pool`     |
| `source_barcode`  | `varchar(255)`  | The barcode of the source of the aliquot                 |                       |
| `sample_name`     | `varchar(255)`  | The name of the sample that the aliquot was created from |                       |
| `used_by_type`    | `varchar(255)`  | The type of the entity that the aliquot is used by       | `none`, `run`, `pool` |
| `used_by_barcode` | `varchar(255)`  | The barcode of the entity that the aliquot is used by    |                       |
| `volume`          | `decimal(10,2)` | The volume of the aliquot ($\mu L$)                      |                       |
| `concentration`   | `decimal(10,2)` | The concentration of the aliquot ($ng/\mu L$)            |                       |
| `insert_size`     | `int`           | The size of the insert in base pairs                     |                       |
| `last_updated`    | `datetime(6)`   | The date and time that the aliquot was last updated      |                       |
| `recorded_at`     | `datetime(6)`   | The date and time that the aliquot was recorded          |                       |
| `created_at`      | `datetime(6)`   | The date and time that the aliquot was created           |                       |

</center>

A sample table from MultiLIMS Warehouse is attached below.

{{ read_csv('aliquot-export.csv') }}

## Tracking volume through message publishing

To access the `primary` and `derived` aliquots created prior to sequencing operations, an asynchronous messaging process was set up so that this process would not block client threads. 
Each time an aliquot is created in Traction (`primary` or `derived`), Traction publishes a message containing details of the aliquots to a RabbitMQ instance that `tol-lab-share` listens to. 
`tol-lab-share` thereafter consumes it, validates it and pushes it to MultiLIMS Warehouse where the aliquots could be accessed.

<figure markdown="span">
  ![EMQ Integration](../img/emq-integration.png)
  <figcaption>Queue Bindings</figcaption>
</figure>
