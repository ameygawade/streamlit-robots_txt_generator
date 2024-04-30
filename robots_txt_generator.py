import streamlit as st

def get_user_agents():
    """Get a list of commonly used User-Agents."""
    return [
        "baiduspider", "baiduspider-image", "baiduspider-mobile", "baiduspider-news",
        "baiduspider-video", "bingbot", "msnbot", "msnbot-media", "adidxbot",
        "Googlebot", "Googlebot-Image", "Googlebot-Mobile", "Googlebot-News",
        "Googlebot-Video", "Storebot-Google", "Mediapartners-Google", "AdsBot-Google",
        "slurp", "yandex"
    ]

def robots_txt_generator():
    """Generate and customize a robots.txt file using a Streamlit app.

    This Streamlit app allows users to customize a robots.txt file by selecting
    User-Agents, specifying disallowed paths, enabling crawler delay, and providing
    a sitemap URL.

    Returns:
        None
    """
    st.title("Robots.txt Generator")
    st.write("Kindly select specific options for robots.txt creation")

    user_agents = get_user_agents()

    user_agent_option = st.radio("Select User-Agent Option:", ("All User-Agents", "Specific User-Agent"))

    if user_agent_option == "Specific User-Agent":
        user_agent = st.multiselect("Select User-Agent(s):", user_agents)
    else:
        user_agent = "*"

    disallow = st.text_area("Disallow (one path per line):", "/path/to/disallow1\n/path/to/disallow2")

    on_crawler_delay = st.checkbox("Mention Crawler Delay")

    if on_crawler_delay:
        user_agent_option_crawler_delay = st.radio("User-agent:", ("All User-Agents", "Specific User-Agent"))

        if user_agent_option_crawler_delay == "Specific User-Agent":
            user_agent_crawler_delay = st.multiselect("Select User-Agent for Crawler:", user_agents)
        else:
            user_agent_crawler_delay = "*"

        page_delays = st.slider("Select the page delay value", 1, 20, 10)

    sitemap = st.text_input("Sitemap URL:", "https://example.com/sitemap.xml")

    if st.button("Generate robots.txt"):
        robots_txt_content = "User-agent: * \nAllow: / \n\n"

        if isinstance(user_agent, list):
            for agent in user_agent:
                # Add User-Agent line only once for all paths
                robots_txt_content += f"User-agent: {agent}\n"
                # Iterate over each line in disallow and add the appropriate Disallow lines
                for line in disallow.strip().split('\n'):
                    robots_txt_content += f"Disallow: {line}\n"
                # Add an additional line break after each User-Agent block
                robots_txt_content += '\n'
        else:
            # Add User-Agent line only once for all paths
            robots_txt_content += f"User-agent: {user_agent}\n"
            # Iterate over each line in disallow and add the appropriate Disallow lines
            for line in disallow.strip().split('\n'):
                robots_txt_content += f"Disallow: {line}\n"

        if on_crawler_delay:
            for agent in (user_agent_crawler_delay if isinstance(user_agent_crawler_delay, list) else [user_agent_crawler_delay]):
                robots_txt_content += f"User-agent: {agent}\nCrawl-delay: {page_delays}\n\n"

        if sitemap:
            robots_txt_content += f"\nSitemap: {sitemap}"

        st.write("Generated robots.txt content:")
        st.code(robots_txt_content)

        st.download_button("Download robots.txt", robots_txt_content, "robots.txt")
        st.success("robots.txt file has been generated and saved as robots.txt")

if __name__ == "__main__":
    robots_txt_generator()
