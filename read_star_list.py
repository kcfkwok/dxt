"""Program to read and parse star data from star_list1.md"""

import re
from typing import List, Dict
from config import config

# Mapping of Bayer designation prefixes to Greek letters
BAYER_TO_GREEK = {
    'alf': 'α', 'bet': 'β', 'gam': 'γ', 'del': 'δ', 'eps': 'ε',
    'zet': 'ζ', 'eta': 'η', 'the': 'θ', 'tet':'θ', 'iot': 'ι', 'kap': 'κ',
    'lam': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omi': 'ο',
    'pi': 'π', 'rho': 'ρ', 'sig': 'σ', 'tau': 'τ', 'ups': 'υ',
    'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'ome': 'ω', 'Sigma': 'Σ',
}

def parse_star_list(file_path: str) -> Dict:
    """Parse star data from markdown table file.
    
    Args:
        file_path: Path to the markdown file
        
    Returns:
        List of dictionaries containing star data
    """
    stars = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        # Skip header and separator lines
        next(f)  # Skip header
        next(f)  # Skip separator
        
        for line in f:
            # Remove leading/trailing whitespace and pipes
            line = line.strip().strip('|')
            if not line:
                continue
                
            # Split into fields
            fields = [field.strip() for field in line.split('|')]
            
            # Extract data (HR ID is first field)
            try:
                hr_id = fields[0] #int(fields[0])
                bayer_name = fields[1]
                
                # Convert Bayer designation to Greek letter if needed
                if bayer_name:
                    # Handle cases like "alf1" or "alf/α And"
                    for prefix, greek in BAYER_TO_GREEK.items():
                        # Match prefix followed by optional number or slash
                        if bayer_name.lower().startswith(prefix):
                            # Replace prefix with Greek letter while preserving suffix
                            suffix = bayer_name[len(prefix):]
                            bayer_name = greek + suffix
                            break
                
                star_data = {
                    'hr_id': fields[0], #int(fields[0]),
                    'bayer_name': bayer_name,
                    'constellation': fields[2],
                    'ra': float(fields[3]),
                    'dec': float(fields[4]),
                    'magnitude': float(fields[5]),
                    'distance_ly': int(fields[6]),
                    'spectrum': fields[7],
                    'chinese_name': fields[8] if fields[8] else None
                }
                stars[hr_id]=star_data
            except (ValueError, IndexError) as e:
                print(f"Skipping malformed line: {line}. Error: {e}")
                
    return stars

def find_star_by_hr(stars: Dict, hr_id: str) -> Dict:
    """Find star by HR ID.
    
    Args:
        stars: List of star dictionaries
        hr_id: HR catalog number to search for
        
    Returns:
        Star dictionary or None if not found
    """
    if hr_id in stars:
        star= stars[hr_id]
        if star['hr_id'] == hr_id:
            return star
    return None

def find_stars_in_constellation(stars: Dict, constellation: str) -> List[Dict]:
    """Find all stars in a given constellation.
    
    Args:
        stars: List of star dictionaries
        constellation: Chinese constellation name to search for
        
    Returns:
        List of matching star dictionaries
    """
    return [star for hr_id, star in stars.items() if star['constellation'] == constellation]

def main():
    """Main function to demonstrate usage."""
    try:
        stars = parse_star_list(config.star_list_path)
        print(f"Successfully parsed {len(stars)} stars")
        
        # Example usage
        hr_15 = find_star_by_hr(stars, 15)
        print(f"\nHR 15 data: {hr_15}")
        
        andromeda_stars = find_stars_in_constellation(stars, '仙女')
        print(f"\nFound {len(andromeda_stars)} stars in Andromeda constellation")
        
    except FileNotFoundError:
        print("Error: star_list1.md not found")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
