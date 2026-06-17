

# Spark Connect Configuration
### The Spark Connect server must already be started with Iceberg (Minio + Nessie Catalog) configurtion

#### For example:

pyspark --master spark://hadoop-master.wingmoney.com:7077 --deploy-mode client --total-executor-cores 6 --executor-memory 2G \
    --jars /opt/spark-3.5.6-bin-hadoop3/jars/iceberg-spark-runtime-3.5_2.12-1.9.2.jar,/opt/spark-3.5.6-bin-hadoop3/jars/hadoop-aws-3.3.1.jar,/opt/spark-3.5.6-bin-hadoop3/jars/aws-java-sdk-bundle-1.12.99.jar \
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
    --conf spark.sql.catalog.nessie_uat=org.apache.iceberg.spark.SparkCatalog \
    --conf spark.sql.catalog.nessie_uat.catalog-impl=org.apache.iceberg.nessie.NessieCatalog \
    --conf spark.sql.catalog.nessie_uat.uri=http://10.120.116.16:19120/api/v2 \
    --conf spark.sql.catalog.nessie_uat.ref=wingbank --conf spark.sql.catalog.nessie_uat.warehouse=s3a://customer360 \
    --conf spark.hadoop.fs.s3a.endpoint=http://hadoop-slave2.wingmoney.com:9000 \
    --conf spark.hadoop.fs.s3a.access.key=admin --conf spark.hadoop.fs.s3a.secret.key=Apire@k12345678 \
    --conf spark.hadoop.fs.s3a.path.style.access=true --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider \
    --conf spark.sql.catalogImplementation=in-memory




##### Explain Configuration

1). Loads extra libraries
    --jars 

2). Iceberg Runtime - [Apache Iceberg Maven Repository](https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.9.2/?utm_source=chatgpt.com)
    iceberg-spark-runtime-3.5_2.12-1.9.2.jar

3). Hadoop AWS - support s3a:// [Apache Hadoop AWS Maven Repository](https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.1/?utm_source=chatgpt.com)
    hadoop-aws-3.3.1.jar

4). AWS SDK - Required by Hadoop AWS - [AWS SDK Bundle Maven Repository](https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.99/?utm_source=chatgpt.com)
    aws-java-sdk-bundle-1.12.99.jar

    Used to talk to:
    - AWS S3
    - MinIO
    - Dell PowerStore S3
    - Other S3-compatible storage

5). Iceberg Extensions
    --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions

6). Catalog Name (Creates a Spark catalog named: nessie_uat)
    --conf spark.sql.catalog.nessie_uat=org.apache.iceberg.spark.SparkCatalog

7). Catalog Implementation - (Tells Iceberg to use nessie as metadata catalog)
    --conf spark.sql.catalog.nessie_uat.catalog-impl=org.apache.iceberg.nessie.NessieCatalog

8). Nessie Server
    --conf spark.sql.catalog.nessie_uat.uri=http://10.120.116.16:19120/api/v2

9). Nessie Branch - (Spark reads/writes tables from branch: wingbank)
    --conf spark.sql.catalog.nessie_uat.ref=wingbank

10). Warehouse Location 
    --conf spark.sql.catalog.nessie_uat.warehouse=s3a://customer360

11). S3 Endpoint
    --conf spark.hadoop.fs.s3a.endpoint=http://hadoop-slave2.wingmoney.com:9000

12). Access Key - (S3 username)
    --conf spark.hadoop.fs.s3a.access.key=admin

13). Secret Key - (S3 password)
    --conf spark.hadoop.fs.s3a.secret.key=**********

14). Path Style Access - (Required for MinIO and many S3-compatible systems)
    --conf spark.hadoop.fs.s3a.path.style.access=true

15). S3A Filesystem - (Use Hadoop S3A connector.)
    --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem

16). Credentials Provider - (Read credentials from access.key and secret.key)
    --conf spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider

17). Catalog Implementation - (Spark's default catalog is in-memory)
    --conf spark.sql.catalogImplementation=in-memory



