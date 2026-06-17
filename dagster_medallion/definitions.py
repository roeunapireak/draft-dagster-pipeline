from dagster import Definitions

from dagster_medallion.assets.BRONZE.tablename01 import tablename01


defs = Definitions(
    assets=[
        tablename01
    ]
    
)


