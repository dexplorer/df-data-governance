# df-data-governance

This repository contains configuration to spin up the data governance or management services using docker containers. The cluster will have the following containers.

* Data Lineage Service
* Data Profile Service
* Data Quality Service
* Data Quality ML Service
* Data Reconciliation Service

Note: If the datasets are in spark/datalake then spin up the spark standalone cluster first.
[Spark Standalone Cluster](https://github.com/dexplorer/df-spark)

Also, start the data management services in the same docker network where the spark cluster nodes are running (i.e. df-spark_dfnet).

Data management services can be found here.

[Data Quality Service](https://github.com/dexplorer/df-data-quality)

[Data Quality ML Service](https://github.com/dexplorer/df-data-quality-ml)

[Data Profiling Service](https://github.com/dexplorer/df-data-profile)

[Data Reconciliation Service](https://github.com/dexplorer/df-data-recon)

[Data Lineage Service](https://github.com/dexplorer/df-data-lineage)


### Spin up Data Management Services using Docker Containers
```sh
docker-compose --project-name=df-spark up
```
