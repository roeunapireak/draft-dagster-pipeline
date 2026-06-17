import dagster as dg
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType

@dg.asset( group_name="bronze_streaming" )

def kafka_to_bronze():

    spark_session = (
        SparkSession.builder
        .remote("sc://spark-master-host:15002")
        .appName("kafka_to_bronze")
        .getOrCreate()
    )

    # 2. Read Kafka
    kafka_df = (
        spark_session.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka-host:9092")
        .option("subscribe", "kafka_topic")
        .option("startingOffsets", "latest")
        .load()
    )

    # 3. Mapping Field Types and JSON Parsing from kafka payload
    schema = StructType([
        StructField("column_01", StringType()),
        StructField("column_02", StringType()),
        StructField("column_03", LongType()),
        StructField("column_04", TimestampType()),
        StructField("column_05", StringType())
    ])

    parsed_df = (
        kafka_df
        .selectExpr("CAST(value AS STRING) as json_str")
        .select(from_json(col("json_str"), schema).alias("data"))
        .select("data.*")
    )


    # 3. Write to Iceberg Table (Nessie + Minio)
    start_streaming = (
        parsed_df.writeStream
        .format("iceberg")
        .outputMode("append")
        .option(
            "checkpointLocation",
            "file:///opt/dagster/checkpoints/BRONZE/tablename01"
        )
        .trigger(processingTime="1 seconds")
        .toTable("nessie.BRONZE.tablename01")
    )

    start_streaming.awaitTermination()


