from pyspark.sql import functions as F


# ---------------------------------------------------------
# 1. Destinations: Bronze → Silver
# ---------------------------------------------------------

destinations_bronze = spark.table(
    "trip_planner.bronze.destinations_raw"
)

destinations_silver = (
    destinations_bronze
    .select(
        F.trim(F.col("name")).alias("destination_name"),
        F.trim(F.col("country")).alias("country"),
        F.upper(F.trim(F.col("country_code"))).alias("country_code"),
        F.col("latitude").cast("double").alias("latitude"),
        F.col("longitude").cast("double").alias("longitude"),
        F.trim(F.col("timezone")).alias("timezone"),
    )
    .filter(
        F.col("destination_name").isNotNull()
        & F.col("latitude").isNotNull()
        & F.col("longitude").isNotNull()
    )
    .dropDuplicates(["destination_name", "country_code"])
)


# Write Silver table
(
    destinations_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("trip_planner.silver.destinations")
)


print("Silver destinations table created successfully.")

destinations_silver.show(truncate=False)

# ---------------------------------------------------------
# 2. Weather: Bronze → Silver
# ---------------------------------------------------------

weather_bronze = spark.table(
    "trip_planner.bronze.weather_raw"
)

weather_silver = (
    weather_bronze
    .select(
        F.to_timestamp("forecast_time").alias("forecast_time"),
        F.col("temperature_2m").cast("double").alias("temperature_2m"),
        F.col("precipitation_probability")
         .cast("double")
         .alias("precipitation_probability"),
        F.col("precipitation").cast("double").alias("precipitation"),
        F.col("weather_code").cast("double").alias("weather_code"),
        F.col("wind_speed_10m").cast("double").alias("wind_speed_10m"),
    )
    .filter(
        F.col("forecast_time").isNotNull()
    )
    .dropDuplicates(["forecast_time"])
)


(
    weather_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("trip_planner.silver.weather")
)


print("Silver weather table created successfully.")

weather_silver.show(10, truncate=False)

# ---------------------------------------------------------
# 3. Air Quality: Bronze → Silver
# ---------------------------------------------------------

air_quality_bronze = spark.table(
    "trip_planner.bronze.air_quality_raw"
)

air_quality_silver = (
    air_quality_bronze
    .select(
        F.to_timestamp("forecast_time").alias("forecast_time"),
        F.col("pm10").cast("double").alias("pm10"),
        F.col("pm2_5").cast("double").alias("pm2_5"),
        F.col("uv_index").cast("double").alias("uv_index"),
    )
    .filter(
        F.col("forecast_time").isNotNull()
    )
    .dropDuplicates(["forecast_time"])
)


(
    air_quality_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("trip_planner.silver.air_quality")
)


print("Silver air quality table created successfully.")

air_quality_silver.show(10, truncate=False)

# ---------------------------------------------------------
# 4. Wikimedia Descriptions: Bronze → Silver
# ---------------------------------------------------------

wikimedia_descriptions_bronze = spark.table(
    "trip_planner.bronze.wikimedia_descriptions_raw"
)

wikimedia_descriptions_silver = (
    wikimedia_descriptions_bronze
    .select(
        F.col("page_id").cast("long").alias("page_id"),
        F.trim(F.col("page_title")).alias("page_title"),
        F.trim(F.col("description")).alias("description")
    )
    .filter(
        F.col("page_id").isNotNull()
        & F.col("description").isNotNull()
        & (F.length(F.col("description")) > 0)
    )
    .dropDuplicates(["page_id"])
)


(
    wikimedia_descriptions_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("trip_planner.silver.wikimedia_descriptions")
)


print("Silver Wikimedia descriptions table created successfully.")

wikimedia_descriptions_silver.show(
    10,
    truncate=False
)

# ---------------------------------------------------------
# 5. Wikimedia Attractions: Bronze → Silver
# ---------------------------------------------------------

wikimedia_attractions_bronze = spark.table(
    "trip_planner.bronze.wikimedia_attractions_raw"
)

wikimedia_attractions_silver = (
    wikimedia_attractions_bronze
    .select(
        F.col("pageid").cast("long").alias("page_id"),
        F.trim(F.col("title")).alias("title"),
        F.col("lat").cast("double").alias("latitude"),
        F.col("lon").cast("double").alias("longitude"),
        F.col("dist").cast("double").alias("distance_meters"),
        F.trim(F.col("primary")).alias("primary")
    )
    .filter(
        F.col("page_id").isNotNull()
        & F.col("title").isNotNull()
        & F.col("latitude").isNotNull()
        & F.col("longitude").isNotNull()
    )
    .dropDuplicates(["page_id"])
)


(
    wikimedia_attractions_silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("trip_planner.silver.wikimedia_attractions")
)


print("Silver Wikimedia attractions table created successfully.")

wikimedia_attractions_silver.show(
    10,
    truncate=False
)