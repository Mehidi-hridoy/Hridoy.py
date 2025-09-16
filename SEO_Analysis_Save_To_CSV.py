import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
from datetime import datetime

# URL of the page to analyze
url = "https://link3.net/"
company = "Link 3 "


# Send a GET request to fetch the page content and measure load time
start_time = time.time()
response = requests.get(url)  # Store the response object here
res = response.text  # Extract the content from the response
end_time = time.time()
page_load_time = round(end_time - start_time, 2)

# Parse the page with BeautifulSoup
soup = BeautifulSoup(res, 'html.parser')

# Lists to store SEO insights
seo_data = []

# Extract Title
title = soup.find('title')
if title:
    seo_data.append(["Title", "Good", f"Title Exists: {title.text.strip()}", url, ""])
else:
    seo_data.append(["Title", "Bad", "Title Does Not Exist", url, url])

# Extract Meta Description
description = soup.find('meta', attrs={'name': 'description'})
if description and description.get('content'):
    seo_data.append(["Meta Description", "Good", f"Description Exists: {description.get('content').strip()}", url, ""])
else:
    seo_data.append(["Meta Description", "Bad", "Description Does Not Exist", url, url])

# Extract Published and Modified Date
published_date = soup.find('meta', attrs={'name': 'published'})
modified_date = soup.find('meta', attrs={'name': 'last-modified'})

if published_date and published_date.get('content'):
    seo_data.append(["Published Date", "Good", f"Published Date: {published_date.get('content').strip()}", url, ""])
else:
    seo_data.append(["Published Date", "Bad", "Published Date Not Found", url, url])

if modified_date and modified_date.get('content'):
    seo_data.append(["Modified Date", "Good", f"Modified Date: {modified_date.get('content').strip()}", url, ""])
else:
    seo_data.append(["Modified Date", "Bad", "Modified Date Not Found", url, url])

# Extract Headings
headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
for heading in headings:
    seo_data.append([f"{heading.name.upper()}", "Good", f"Heading Text: {heading.text.strip()}", url, ""])

if not any(h.name == 'h1' for h in headings):
    seo_data.append(["H1", "Bad", "H1 Tag Not Found", url, url])

# Check for Images without Alt Tags
images = soup.find_all('img')
for img in images:
    if not img.get('alt'):
        seo_data.append(["Image", "Bad", f"Image Missing Alt Tag: {img.get('src')}", url, url])

# Check for Favicon
favicon = soup.find('link', rel='icon') or soup.find('link', rel='shortcut icon')
if favicon:
    seo_data.append(["Favicon", "Good", "Favicon Exists", url, ""])
else:
    seo_data.append(["Favicon", "Bad", "Favicon Not Found", url, url])

# Check for Mobile-Friendliness (Meta Viewport)
viewport = soup.find('meta', attrs={'name': 'viewport'})
if viewport:
    seo_data.append(["Mobile-Friendliness", "Good", "Viewport Meta Tag Found", url, ""])
else:
    seo_data.append(["Mobile-Friendliness", "Bad", "Viewport Meta Tag Not Found", url, url])

# Technical Extracts
# Extract HTTP Status Code
status_code = response.status_code  # Use the response object to get the status code
seo_data.append(["HTTP Status Code", "Good" if status_code == 200 else "Bad", f"Status Code: {status_code}", url, ""])

# Extract Canonical Tag
canonical = soup.find('link', rel='canonical')
if canonical:
    seo_data.append(["Canonical Tag", "Good", f"Canonical Tag: {canonical.get('href')}", url, ""])
else:
    seo_data.append(["Canonical Tag", "Bad", "Canonical Tag Not Found", url, url])

# Extract Structured Data (JSON-LD, Microdata, RDFa)
structured_data = soup.find_all('script', type='application/ld+json')
if structured_data:
    for data in structured_data:
        seo_data.append(["Structured Data (JSON-LD)", "Good", f"Structured Data Found", url, ""])
else:
    seo_data.append(["Structured Data (JSON-LD)", "Bad", "Structured Data Not Found", url, url])

# Check Robots.txt
robots_url = urljoin(url, 'robots.txt')
robots_response = requests.get(robots_url)
if robots_response.status_code == 200:
    seo_data.append(["Robots.txt", "Good", f"Robots.txt Found: {robots_url}", url, ""])
else:
    seo_data.append(["Robots.txt", "Bad", "Robots.txt Not Found", url, url])

# Check XML Sitemap
sitemap_url = urljoin(url, 'sitemap.xml')
sitemap_response = requests.get(sitemap_url)
if sitemap_response.status_code == 200:
    seo_data.append(["XML Sitemap", "Good", f"Sitemap Found: {sitemap_url}", url, ""])
else:
    seo_data.append(["XML Sitemap", "Bad", "Sitemap Not Found", url, url])

# Check for Broken Links
links = soup.find_all('a', href=True)
broken_links = []
for link in links:
    link_url = link['href']
    full_url = urljoin(url, link_url)
    try:
        link_res = requests.get(full_url, timeout=5)
        if link_res.status_code >= 400:
            broken_links.append(full_url)
    except requests.exceptions.RequestException:
        broken_links.append(full_url)

if broken_links:
    seo_data.append(["Broken Links", "Bad", f"Broken Links Found: {', '.join(broken_links)}", url, ""])
else:
    seo_data.append(["Broken Links", "Good", "No Broken Links Found", url, ""])

# International SEO: hreflang tags
hreflang_tags = soup.find_all('link', attrs={'rel': 'alternate', 'hreflang': True})
if hreflang_tags:
    seo_data.append(["hreflang Tags", "Good", "hreflang Tags Found", url, ""])
else:
    seo_data.append(["hreflang Tags", "Bad", "hreflang Tags Not Found", url, url])

# Indexability: Check for noindex or robots.txt blocking
meta_noindex = soup.find('meta', attrs={'name': 'robots', 'content': 'noindex'})
if meta_noindex:
    seo_data.append(["Indexability", "Bad", "Noindex Tag Found", url, ""])
else:
    seo_data.append(["Indexability", "Good", "Page is Indexable", url, ""])

# Analytics Integration: Check for Google Analytics or Tag Manager
google_analytics = soup.find('script', attrs={'src': lambda x: x and 'www.googletagmanager.com/gtag/js' in x})
if google_analytics:
    seo_data.append(["Analytics Integration", "Good", "Google Analytics Found", url, ""])
else:
    seo_data.append(["Analytics Integration", "Bad", "Google Analytics Not Found", url, url])

# Core Web Vitals: Check for performance-related metadata (LCP, FID, CLS)
# These checks typically require page speed tools, but we'll check for relevant metadata here.
core_web_vitals = soup.find_all('script', type='application/json')
if any('web-vitals' in str(data) for data in core_web_vitals):
    seo_data.append(["Core Web Vitals", "Good", "Core Web Vitals Data Found", url, ""])
else:
    seo_data.append(["Core Web Vitals", "Bad", "Core Web Vitals Data Not Found", url, url])

# Security: HTTPS Implementation
https_status = "HTTPS" if url.startswith("https://") else "HTTP"
if https_status == "HTTPS":
    seo_data.append(["HTTPS Implementation", "Good", "Site Uses HTTPS", url, ""])
else:
    seo_data.append(["HTTPS Implementation", "Bad", "Site Does Not Use HTTPS", url, url])

# Security Headers: Check for CSP, X-Content-Type-Options
headers = response.headers
csp = headers.get('Content-Security-Policy', None)
x_content_type_options = headers.get('X-Content-Type-Options', None)

if csp:
    seo_data.append(["Security Headers (CSP)", "Good", "Content-Security-Policy Found", url, ""])
else:
    seo_data.append(["Security Headers (CSP)", "Bad", "Content-Security-Policy Not Found", url, url])

if x_content_type_options:
    seo_data.append(["Security Headers (X-Content-Type-Options)", "Good", "X-Content-Type-Options Found", url, ""])
else:
    seo_data.append(["Security Headers (X-Content-Type-Options)", "Bad", "X-Content-Type-Options Not Found", url, url])

# Media Optimization: Image File Sizes
image_file_sizes = [img['src'] for img in images if img.get('src') and requests.head(urljoin(url, img['src'])).status_code == 200]
large_images = []

for img_url in image_file_sizes:
    img_res = requests.head(urljoin(url, img_url))
    img_size = int(img_res.headers.get('Content-Length', 0))
    if img_size > 1000000:  # 1MB threshold for image size
        large_images.append(img_url)

if large_images:
    seo_data.append(["Image File Sizes", "Bad", f"Large Images Found: {', '.join(large_images)}", url, ""])
else:
    seo_data.append(["Image File Sizes", "Good", "No Large Images Found", url, ""])

# Image File Names: Verify keywords in filenames
image_keywords = []
for img in images:
    img_src = img.get('src')
    if img_src and ' ' in img_src:
        image_keywords.append(img_src)

if image_keywords:
    seo_data.append(["Image File Names", "Bad", f"Images with Spaces in Filenames: {', '.join(image_keywords)}", url, ""])
else:
    seo_data.append(["Image File Names", "Good", "All Image File Names are Optimized", url, ""])

# Lazy Loading: Check if images have the 'loading="lazy"' attribute
lazy_loaded_images = [img for img in images if img.get('loading') == 'lazy']
if lazy_loaded_images:
    seo_data.append(["Lazy Loading", "Good", "Lazy Loading Found", url, ""])
else:
    seo_data.append(["Lazy Loading", "Bad", "Lazy Loading Not Found", url, url])

# Save the results to a CSV file
filename = f'{company}_seo_analysis_with_international_and_security.csv'
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write headers
    writer.writerow(["SEO Aspect", "Status", "Key Point", "URL", "Bad Practice URL"])

    # Write SEO data
    writer.writerows(seo_data)

print(f"SEO analysis with additional checks saved to {filename}")
