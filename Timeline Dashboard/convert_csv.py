import csv
import json

def convert_csv_to_js():
    roadmap_data = []
    
    with open('FY26_27 Me@Sams_timeline dashboard.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Clean and map the data
            item = {
                'title': row['Product Item Name'].strip(),
                'quarter': row['Proposed Roadmap (Launch) FY QTR'].strip(),
                'category': row['Product Group'].strip(),
                'status': row['Product Development Life Cycle Stage'].strip(),
                'priority': row['PPD Priority'].strip(),
                'product': row['Product'].strip(),
                'itemType': row['Item Type'].strip(),
                'productManager': row['Product Manager'].strip(),
                'productLeader': row['Product Leader '].strip()
            }
            
            # Only include items with valid quarter data
            if item['quarter'] and item['quarter'] != '':
                roadmap_data.append(item)
    
    # Generate JavaScript array
    js_data = "let roadmapData = " + json.dumps(roadmap_data, indent=4) + ";"
    
    with open('roadmap_data.js', 'w', encoding='utf-8') as outfile:
        outfile.write(js_data)
    
    print(f"Converted {len(roadmap_data)} items from CSV to JavaScript")
    return roadmap_data

if __name__ == "__main__":
    data = convert_csv_to_js()
    print(f"Created roadmap_data.js with {len(data)} items")
    
    # Show quarter breakdown
    quarters = {}
    for item in data:
        quarter = item['quarter']
        if quarter in quarters:
            quarters[quarter] += 1
        else:
            quarters[quarter] = 1
    
    print("\nQuarter breakdown:")
    for quarter, count in sorted(quarters.items()):
        print(f"  {quarter}: {count} items")