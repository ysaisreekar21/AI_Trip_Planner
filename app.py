import os
from datetime import date, timedelta

import psycopg
import streamlit as st
from databricks.sdk import WorkspaceClient


# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ AI Trip Planner")
st.write("Plan a personalized trip with Databricks Genie and save it to Lakebase.")


USER_ID = 3


# =========================================================
# LAKEBASE
# =========================================================

def get_lakebase_connection():
    endpoint_name = os.getenv("ENDPOINT_NAME")
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT", "5432")
    database = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    sslmode = os.getenv("PGSSLMODE", "require")

    missing = []
    if not endpoint_name:
        missing.append("ENDPOINT_NAME")
    if not host:
        missing.append("PGHOST")
    if not database:
        missing.append("PGDATABASE")
    if not user:
        missing.append("PGUSER")

    if missing:
        raise RuntimeError(
            "Missing Lakebase configuration: " + ", ".join(missing)
        )

    workspace = WorkspaceClient()

    credential = workspace.postgres.generate_database_credential(
        endpoint=endpoint_name
    )

    return psycopg.connect(
        host=host,
        port=port,
        dbname=database,
        user=user,
        password=credential.token,
        sslmode=sslmode,
    )


def get_activities():
    conn = get_lakebase_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT activity_id, name, category, description
                FROM public.activities
                ORDER BY activity_id
                """
            )
            return cur.fetchall()
    finally:
        conn.close()


def create_trip(destination, days):
    start_date = date.today()
    end_date = start_date + timedelta(days=int(days) - 1)

    conn = get_lakebase_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO public.trips
                    (user_id, trip_name, start_date, end_date, status)
                VALUES
                    (%s, %s, %s, %s, %s)
                RETURNING trip_id
                """,
                (
                    USER_ID,
                    f"{destination.strip()} Trip",
                    start_date,
                    end_date,
                    "planned",
                ),
            )

            trip_id = cur.fetchone()[0]

        conn.commit()
        return trip_id

    finally:
        conn.close()


def save_itinerary_items(trip_id, matched_activities, days):
    if not matched_activities:
        return 0

    conn = get_lakebase_connection()
    saved = 0

    try:
        with conn.cursor() as cur:
            for index, activity in enumerate(matched_activities):
                activity_id = activity[0]
                name = activity[1]

                day_number = (index % int(days)) + 1
                activity_date = date.today() + timedelta(days=day_number - 1)

                cur.execute(
                    """
                    INSERT INTO public.itinerary_items
                    (
                        trip_id,
                        activity_id,
                        activity_date,
                        status,
                        reason,
                        notes
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        trip_id,
                        activity_id,
                        activity_date,
                        "planned",
                        "Recommended by Databricks Genie.",
                        f"Selected activity: {name}",
                    ),
                )

                saved += 1

        conn.commit()
        return saved

    finally:
        conn.close()


# =========================================================
# TEXT / ACTIVITY MATCHING
# =========================================================

def normalize(text):
    if text is None:
        return ""

    return (
        str(text)
        .lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace(",", " ")
        .replace(".", " ")
        .replace("(", " ")
        .replace(")", " ")
        .replace(":", " ")
        .replace("'", "")
    )


def find_activity_names_in_itinerary(itinerary_text, activities):
    """
    Match Genie recommendations against the exact activity names
    available in Lakebase.

    The Genie prompt is also given the exact list of activity names,
    so the response and Lakebase use the same vocabulary.
    """

    text = normalize(itinerary_text)
    matches = []

    for activity in activities:
        activity_id, name, category, description = activity

        if not name:
            continue

        name_normalized = normalize(name)

        if name_normalized and name_normalized in text:
            if activity_id not in [x[0] for x in matches]:
                matches.append((activity_id, name, category, description))

    return matches


def get_genie_text(response):
    parts = []

    attachments = getattr(response, "attachments", None) or []

    for attachment in attachments:
        text_obj = getattr(attachment, "text", None)

        if text_obj is None:
            continue

        content = getattr(text_obj, "content", None)

        if content:
            parts.append(str(content))

    return "\n\n".join(parts).strip()


# =========================================================
# FALLBACK
# =========================================================

def build_fallback(destination, days, preferences, activities):
    if not activities:
        raise RuntimeError(
            "Genie was unavailable and the Lakebase activities table is empty."
        )

    lines = [
        f"Data-backed {int(days)}-day itinerary for {destination}.",
    ]

    if preferences.strip():
        lines.append(f"Preferences: {preferences.strip()}")

    lines.append("")

    for day_number in range(1, int(days) + 1):
        activity = activities[(day_number - 1) % len(activities)]

        name = activity[1]
        category = activity[2]
        description = activity[3]

        lines.append(f"Day {day_number}")
        lines.append(f"- {name} ({category})")

        if description:
            lines.append(f"  {description}")

        lines.append("")

    lines.append("This itinerary uses activities stored in Lakebase.")

    return "\n".join(lines)


# =========================================================
# GENIE
# =========================================================

def ask_genie(destination, days, preferences, activities):
    space_id = os.getenv("GENIE_SPACE_ID")

    if not space_id:
        raise RuntimeError(
            "GENIE_SPACE_ID is not configured in the Databricks App."
        )

    if not activities:
        raise RuntimeError(
            "The Lakebase activities table contains no activities."
        )

    activity_lines = []

    for activity_id, name, category, description in activities:
        activity_lines.append(
            f"- {name} | category: {category} | description: {description or 'No description'}"
        )

    available_activities = "\n".join(activity_lines)

    preference_text = preferences.strip()
    if not preference_text:
        preference_text = "general sightseeing"

    question = f"""
Create a practical {int(days)}-day itinerary for {destination}.

Traveler preferences:
{preference_text}

Use the connected weather and air-quality data when relevant.

IMPORTANT:
You MUST select activities ONLY from the following Lakebase activities.
Use the activity names EXACTLY as written below.
Do NOT invent, rename, paraphrase, or substitute activity names.

AVAILABLE LAKEBASE ACTIVITIES:
{available_activities}

Requirements:
1. Organize the response by Day 1, Day 2, etc.
2. Select suitable activities from the list above.
3. Consider weather, temperature, precipitation, and air quality.
4. Respect the traveler's preferences.
5. Avoid repeating an activity when other suitable activities are available.
6. For every selected activity, use its exact Lakebase name.
7. Give the category and a short description.
8. Give a short reason for the selection.
9. If weather is unsuitable for an outdoor activity, choose another suitable activity from the list.
10. Never create an activity that is not in the AVAILABLE LAKEBASE ACTIVITIES list.
"""

    workspace = WorkspaceClient()

    response = workspace.genie.start_conversation_and_wait(
        space_id=space_id,
        content=question,
    )

    text = get_genie_text(response)

    if not text:
        raise RuntimeError("Genie returned no readable itinerary text.")

    return text


# =========================================================
# USER INPUT
# =========================================================

destination = st.text_input(
    "Where do you want to travel?",
    placeholder="Example: Visakhapatnam",
)

days = st.number_input(
    "Number of days",
    min_value=1,
    max_value=14,
    value=2,
    step=1,
)

preferences = st.text_area(
    "What are your preferences?",
    placeholder="Example: outdoor activities, beaches, sightseeing, good air quality",
)

plan_clicked = st.button(
    "🗺️ Plan My Trip",
    type="primary",
)


# =========================================================
# RUN
# =========================================================

if plan_clicked:

    if not destination.strip():
        st.warning("Please enter a destination.")
        st.stop()

    try:
        # 1. Read activities first.
        activities = get_activities()

        # 2. Ask Genie using the exact Lakebase activity vocabulary.
        genie_used = True

        try:
            with st.spinner("🤖 Generating your itinerary with Databricks Genie..."):
                itinerary_text = ask_genie(
                    destination,
                    days,
                    preferences,
                    activities,
                )

        except Exception as genie_error:
            genie_used = False
            itinerary_text = build_fallback(
                destination,
                days,
                preferences,
                activities,
            )

            st.warning(
                "Genie was unavailable. The app used Lakebase activities as a fallback."
            )

        # 3. Display itinerary.
        st.subheader("🗺️ Your Itinerary")
        st.write(itinerary_text)

        if genie_used:
            st.success("Genie successfully generated your itinerary.")

        # 4. Save trip.
        with st.spinner("💾 Saving trip to Lakebase..."):
            trip_id = create_trip(destination, days)

        st.success(f"Trip saved successfully. Trip ID: {trip_id}")

        # 5. Match Genie activities against the SAME activity list
        #    that was supplied to Genie.
        matched_activities = find_activity_names_in_itinerary(
            itinerary_text,
            activities,
        )

        # 6. Save itinerary items.
        if matched_activities:
            saved_count = save_itinerary_items(
                trip_id,
                matched_activities,
                days,
            )

            st.info(
                f"{saved_count} matching activity item(s) saved to Lakebase."
            )
        else:
            st.warning(
                "Trip was saved, but no Lakebase activity names were found "
                "in the Genie response."
            )

    except Exception as error:
        st.error(f"Unable to complete the trip request: {error}")