import requests
from bs4 import BeautifulSoup

def fetch_and_print_grid_from_published_doc(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        grid = {}

        for index, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) == 3:  # Ensures there are exactly three columns as expected
                try:
                    # Attempt to parse x, y coordinates and character
                    x = int(cells[0].text.strip())
                    char = cells[1].text.strip()
                    y = int(cells[2].text.strip())
                    
                    if y not in grid:
                        grid[y] = {}
                    grid[y][x] = char
                except ValueError:
                    # Handles the case where conversion to int fails
                    print(f"Skipping row {index}: cannot convert to int.")
                    continue

        # Determine grid dimensions and print the grid
        max_x = max(max(row.keys()) for row in grid.values()) if grid else 0
        max_y = max(grid.keys()) if grid else 0

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                print(grid.get(y, {}).get(x, ' '), end='')
            print()
    else:
        print("Failed to retrieve the document")

# Example usage
url = 'https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub'
fetch_and_print_grid_from_published_doc(url)
