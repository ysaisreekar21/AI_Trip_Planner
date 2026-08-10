# ✈️ AI Trip Planner

An AI-powered trip planning application built with Databricks that creates personalized itineraries based on a user's destination, trip duration, preferences, weather conditions, air quality, and available activities.

The application uses Databricks Genie to generate the itinerary and Lakebase to persist the trip and selected activities.

---

## 📌 Project Overview

Planning an outdoor trip often requires checking multiple sources for destinations, activities, weather, and air quality.

The AI Trip Planner brings these pieces together into a single Databricks-based application.

A user provides:

- Destination
- Number of days
- Travel preferences

The application uses available travel, weather, air-quality, and activity data to generate a personalized itinerary.

The generated trip can then be saved to Lakebase.

---

## 🎯 Problem Statement

Travel planning can be time-consuming because users need to consider:

- Suitable destinations
- Available activities
- Weather conditions
- Air quality
- Outdoor suitability
- User preferences

The goal of this project is to build an AI-powered application that combines these factors and produces a practical trip itinerary.

---

## 💡 Solution

The AI Trip Planner uses Databricks technologies to create an end-to-end data and AI application.

The workflow is:

```text
User
 │
 ▼
Databricks App
 │
 ▼
Genie Agent
 │
 ├── Weather Data
 ├── Air Quality Data
 ├── Destination Data
 ├── Attraction Data
 └── Activity Data
 │
 ▼
Personalized Itinerary
 │
 ▼
Lakebase
 │
 ├── Trip
 └── Trip Activities

              External Data Sources
                     │
          ┌──────────┴──────────┐
          │                     │
      Weather              Air Quality
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
              Data Processing
                     │
                     ▼
                Silver Tables
                     │
        ┌────────────┼────────────┐
        │            │            │
   destinations   weather    air_quality
        │                         │
        ├── wikimedia_attractions │
        └── wikimedia_descriptions
                     │
                     ▼
              Databricks Genie
                     │
                     ▼
             AI Trip Planner Agent
                     │
                     ▼
              Databricks App
                     │
                     ▼
                 Lakebase
                     │
              ┌──────┴──────┐
              ▼             ▼
             Trips       Activities



             Technologies Used
Databricks
Databricks Workspace
Apache Spark
Delta Lake
Unity Catalog
Databricks Genie
Genie Agent
Databricks Apps
Lakebase
Application
Python
Streamlit
Databricks SDK
PostgreSQL connectivity through psycopg
📊 Data Sources

The project uses multiple datasets to support itinerary generation.

Weather

Weather information is used to understand conditions such as:

Temperature
Precipitation
Weather suitability
Air Quality

Air-quality information is used to consider outdoor suitability.

Examples include:

PM2.5
PM10
Air-quality conditions
Destination Data

Destination information provides locations that can be considered during trip planning.

Wikimedia Data

Wikimedia attraction and description data provides additional information about attractions and places.

Activity Data

Activity information stored in Lakebase is used by the application for activity selection and persistence.

🤖 Databricks Genie

Databricks Genie is used as the AI reasoning layer for the application.

The Genie Agent is configured with project data sources including:

air_quality
destinations
weather
wikimedia_attractions
wikimedia_descriptions
activities

The Agent can answer questions about the available data and generate personalized trip recommendations.

Example request:

Create a 2-day itinerary for Visakhapatnam
focusing on outdoor activities and good air quality.

The Agent uses the available data to generate an itinerary based on the requested preferences and environmental conditions.

🗄️ Lakebase Integration

Lakebase is used as the application's operational database.

The application saves:

Trip information
Generated itinerary information
Matching activity records

After a successful trip generation, the application displays the saved trip ID.

Example:

Trip saved successfully. Trip ID: 6
3 matching activity item(s) saved to Lakebase.

This demonstrates the integration between the Databricks App and Lakebase.

🖥️ Databricks App

The application is implemented using Streamlit and deployed as a Databricks App.

The user interface allows the user to enter:

Destination

Example:

Visakhapatnam
Number of Days

Example:

2
Preferences

Example:

Outdoor activities, good air quality

The user then selects:

🗺️ Plan My Trip

The application sends the request to the Genie Agent and displays the generated itinerary.

🔄 End-to-End Workflow
Step 1: User Input

The user enters the destination, number of days, and preferences.

Step 2: Application Request

The Streamlit application receives the request.

Step 3: Genie Agent

The request is sent to the Databricks Genie Agent.

Step 4: Data-Based Reasoning

The Agent uses the configured data sources to determine suitable activities and conditions.

Step 5: Itinerary Generation

The Agent generates a personalized itinerary.

Step 6: Lakebase Persistence

The application saves the trip and matching activities to Lakebase.

Step 7: User Output

The application displays the generated itinerary and confirms successful persistence.

🧪 Example
User Request
Destination: Visakhapatnam

Days: 2

Preferences:
Outdoor activities, good air quality
Generated Itinerary

The application can generate recommendations such as:

Day 1
- RK Beach
- Kailasagiri

Day 2
- INS Kurusura Submarine Museum
- RK Beach

The exact recommendations depend on the available data and environmental conditions at the time of the request.

✅ Successful End-to-End Test

A successful application test demonstrated:

Genie successfully generated your itinerary.

Trip saved successfully. Trip ID: 6

3 matching activity item(s) saved to Lakebase.

This confirms the complete application flow:

User Input
    ↓
Databricks App
    ↓
Genie Agent
    ↓
Itinerary Generation
    ↓
Lakebase
    ↓
Saved Trip + Activities