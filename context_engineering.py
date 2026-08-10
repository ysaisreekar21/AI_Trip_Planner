from pyspark.sql import functions as F


# --------------------------------------------------
# 1. Destination descriptions
# --------------------------------------------------

descriptions = (
    spark.table("trip_planner.silver.wikimedia_descriptions")
    .select(
        F.col("page_id").cast("long").alias("page_id"),
        F.trim(F.col("page_title")).alias("title"),
        F.trim(F.col("description")).alias("description")
    )
    .filter(
        F.col("description").isNotNull() &
        (F.length(F.col("description")) > 0)
    )
)


# --------------------------------------------------
# 2. Nearby attractions
# --------------------------------------------------

attractions = (
    spark.table("trip_planner.silver.wikimedia_attractions")
    .select(
        F.col("page_id").cast("long").alias("page_id"),
        F.trim(F.col("title")).alias("title"),
        F.col("latitude").cast("double").alias("latitude"),
        F.col("longitude").cast("double").alias("longitude"),
        F.col("distance_meters").cast("double").alias("distance_meters")
    )
    .filter(
        F.col("title").isNotNull() &
        (F.length(F.col("title")) > 0)
    )
)


# --------------------------------------------------
# 3. Create searchable attraction context
# --------------------------------------------------

attraction_context = attractions.select(
    F.col("page_id"),
    F.col("title"),
    F.lit("attraction").alias("content_type"),
    F.concat(
        F.lit("Attraction: "),
        F.col("title"),
        F.lit(". Location: latitude "),
        F.col("latitude").cast("string"),
        F.lit(", longitude "),
        F.col("longitude").cast("string"),
        F.lit(". Distance from destination: "),
        F.round(F.col("distance_meters"), 1).cast("string"),
        F.lit(" meters.")
    ).alias("content")
)


# --------------------------------------------------
# 4. Create searchable destination context
# --------------------------------------------------

destination_context = descriptions.select(
    F.col("page_id"),
    F.col("title"),
    F.lit("destination").alias("content_type"),
    F.concat(
        F.lit("Destination: "),
        F.col("title"),
        F.lit(". "),
        F.col("description")
    ).alias("content")
)


# --------------------------------------------------
# 5. Combine both context types
# --------------------------------------------------

ai_context = destination_context.unionByName(attraction_context)


# --------------------------------------------------
# 6. Save AI-ready context table
# --------------------------------------------------

(
    ai_context
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("trip_planner.silver.ai_trip_context")
)


# --------------------------------------------------
# 7. Verify
# --------------------------------------------------

print("AI context table created successfully.")

spark.table("trip_planner.silver.ai_trip_context").show(
    truncate=False
)