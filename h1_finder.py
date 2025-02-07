from bs4 import BeautifulSoup
import requests
import csv

site = "https://pakistanyouthparliament.org/sitemap.xml"

response = requests.get(site)

# Going through the main site map
if response.status_code == 200:

    site_map = response.text
    soup = BeautifulSoup(site_map, "xml")
    
    component_map = []
    for link in soup.find_all('loc'):
        component_map.append(str(link)[5: -6])

    # going through individual sitemaps. for posts, news, etc
    for site in component_map:

        r = requests.get(site)

        if r.status_code == 200:

            content = r.text
            soup = BeautifulSoup(content, 'xml')

            post_map = []

            for link in soup.find_all('loc'):

                # I was getting two responses
                # <loc> and <image:loc>
                # I will be formatting these strings

                link = str(link)
                if link.startswith('<loc>'):
                    post_map.append(link[5: -6])

            # Now getting through each post
            for p in post_map:

                r = requests.get(p)

                if r.status_code == 200:

                    content = r.text
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):

                        # print(tag)
                        with open('headers.csv', 'a', newline="") as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([p, tag.name, tag.text.strip()])
                
                else:
                    print(f"Error Opening Post{p}")

        else:
            print(f"Error Opening Site{site}")


else:
    print("A error occurred")
