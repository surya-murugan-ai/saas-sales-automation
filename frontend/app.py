import streamlit as st
import requests
from config import settings

st.title("Sales Automation SaaS")

try:
    # Scraping Form
    with st.form("scrape_form"):
        linkedin_url = st.text_input("LinkedIn Sales Navigator URL")
        session_cookie = st.text_input("Session Cookie (li_at)", type="password")
        lead_count = st.number_input("Number of Leads", min_value=1, max_value=100, value=10)
        notification_email = st.text_input("Scraping Notification Email")
        submitted = st.form_submit_button("Start Scraping")

        if submitted:
            if not all([linkedin_url, session_cookie, notification_email]):
                st.error("Please fill in all required fields for scraping.")
            elif "@" not in notification_email:
                st.error("Please enter a valid email address for scraping.")
            else:
                try:
                    response = requests.post(
                        f"{settings.API_URL}/api/scrape",
                        json={
                            "linkedin_url": linkedin_url,
                            "session_cookie": session_cookie,
                            "lead_count": lead_count,
                            "notification_email": notification_email
                        },
                        timeout=10
                    )
                    response.raise_for_status()
                    data = response.json()
                    task_id = data.get("task_id")
                    if task_id:
                        st.success(f"Scraping started! Task ID: {task_id}")
                    else:
                        st.error("Scraping started, but no task ID returned.")
                except requests.ConnectionError:
                    st.error("Failed to connect to the backend. Ensure it's running at http://localhost:8000.")
                except requests.Timeout:
                    st.error("Request timed out. Try again later.")
                except requests.HTTPError as e:
                    st.error(f"Backend error: {e.response.status_code} - {e.response.reason}")
                except (requests.JSONDecodeError, KeyError):
                    st.error("Invalid response from backend. Contact support.")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

    # Campaign Form
    with st.form("campaign_form"):
        campaign_email = st.text_input("Campaign Notification Email")
        campaign_submitted = st.form_submit_button("Start LinkedIn Campaign")

        if campaign_submitted:
            if not campaign_email:
                st.error("Please enter a campaign notification email.")
            elif "@" not in campaign_email:
                st.error("Please enter a valid email address for campaign.")
            else:
                try:
                    response = requests.post(
                        f"{settings.API_URL}/api/campaign",
                        json={"notification_email": campaign_email},
                        timeout=10
                    )
                    response.raise_for_status()
                    data = response.json()
                    task_id = data.get("task_id")
                    if task_id:
                        st.success(f"Campaign started! Task ID: {task_id}")
                    else:
                        st.error("Campaign started, but no task ID returned.")
                except requests.ConnectionError:
                    st.error("Failed to connect to the backend. Ensure it's running at http://localhost:8000.")
                except requests.Timeout:
                    st.error("Request timed out. Try again later.")
                except requests.HTTPError as e:
                    st.error(f"Backend error: {e.response.status_code} - {e.response.reason}")
                except (requests.JSONDecodeError, KeyError):
                    st.error("Invalid response from backend. Contact support.")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

except AttributeError:
    st.error("Configuration error: API_URL is not set. Check frontend/.env.")
except Exception as e:
    st.error(f"Failed to initialize app: {str(e)}")