import pandas as pd
import os
import json

def convert_excel_to_csv():
    """Convert the Excel roadmap file to CSV for easier processing"""
    
    excel_file = "FY26_27 Me@Sams Roadmap data file.xlsx"
    
    if not os.path.exists(excel_file):
        print(f"❌ Excel file '{excel_file}' not found in current directory")
        print("Available files:")
        for file in os.listdir('.'):
            if file.endswith(('.xlsx', '.xls', '.csv')):
                print(f"  - {file}")
        return False
    
    try:
        print(f"📖 Reading Excel file: {excel_file}")
        
        # Try to read all sheets
        excel_file_obj = pd.ExcelFile(excel_file)
        sheet_names = excel_file_obj.sheet_names
        
        print(f"📄 Found {len(sheet_names)} sheet(s): {', '.join(sheet_names)}")
        
        # Read the first sheet or a sheet that looks like roadmap data
        roadmap_sheet = None
        for sheet in sheet_names:
            if any(keyword in sheet.lower() for keyword in ['roadmap', 'timeline', 'plan', 'data', 'main']):
                roadmap_sheet = sheet
                break
        
        if not roadmap_sheet:
            roadmap_sheet = sheet_names[0]  # Use first sheet as fallback
        
        print(f"📊 Using sheet: '{roadmap_sheet}'")
        df = pd.read_excel(excel_file, sheet_name=roadmap_sheet)
        
        print(f"✅ Successfully loaded {len(df)} rows and {len(df.columns)} columns")
        print("\n📋 Column names found:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Save as CSV
        csv_filename = "roadmap_data.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\n💾 Saved as CSV: {csv_filename}")
        
        # Show sample data
        print("\n👀 Sample data (first 3 rows):")
        print(df.head(3).to_string())
        
        # Try to identify key columns
        print("\n🔍 Analysis of columns:")
        identify_columns(df)
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading Excel file: {str(e)}")
        return False

def identify_columns(df):
    """Analyze columns to identify roadmap elements"""
    
    suggestions = {
        'title_columns': [],
        'date_columns': [],
        'category_columns': [],
        'status_columns': []
    }
    
    for col in df.columns:
        col_lower = col.lower()
        sample_values = df[col].dropna().head().astype(str).str.lower()
        
        # Check for title/name columns
        if any(keyword in col_lower for keyword in ['title', 'name', 'initiative', 'project', 'feature', 'item']):
            suggestions['title_columns'].append(col)
        
        # Check for date/quarter columns
        elif any(keyword in col_lower for keyword in ['date', 'quarter', 'q1', 'q2', 'q3', 'q4', 'launch', 'release', 'timeline', 'when']):
            suggestions['date_columns'].append(col)
        
        # Check for category columns
        elif any(keyword in col_lower for keyword in ['category', 'team', 'area', 'domain', 'type', 'group']):
            suggestions['category_columns'].append(col)
        
        # Check for status columns
        elif any(keyword in col_lower for keyword in ['status', 'state', 'progress', 'phase']):
            suggestions['status_columns'].append(col)
        
        # Check sample values for quarter patterns
        elif any('fy' in val and 'q' in val for val in sample_values):
            suggestions['date_columns'].append(col)
    
    # Print suggestions
    for key, columns in suggestions.items():
        if columns:
            category_name = key.replace('_', ' ').title()
            print(f"  {category_name}: {', '.join(columns)}")
    
    # Generate mapping suggestions
    print("\n💡 Suggested column mapping for visualization:")
    if suggestions['title_columns']:
        print(f"  Title/Name: {suggestions['title_columns'][0]}")
    if suggestions['date_columns']:
        print(f"  Launch Quarter: {suggestions['date_columns'][0]}")
    if suggestions['category_columns']:
        print(f"  Category: {suggestions['category_columns'][0]}")
    if suggestions['status_columns']:
        print(f"  Status: {suggestions['status_columns'][0]}")

def create_sample_csv():
    """Create a sample CSV file with the expected format"""
    
    sample_data = [
        {
            'Title': 'Mobile App Enhancement',
            'Quarter': 'FY26 Q1',
            'Category': 'Technology',
            'Status': 'In Progress',
            'Priority': 'High',
            'Description': 'Enhance mobile app user experience and performance'
        },
        {
            'Title': 'Member Rewards Program',
            'Quarter': 'FY26 Q1',
            'Category': 'Member Experience',
            'Status': 'Planning',
            'Priority': 'High',
            'Description': 'Launch comprehensive member rewards and loyalty program'
        },
        {
            'Title': 'Inventory Management System',
            'Quarter': 'FY26 Q2',
            'Category': 'Operations',
            'Status': 'Planning',
            'Priority': 'Medium',
            'Description': 'Implement advanced inventory tracking and management'
        },
        {
            'Title': 'Personalized Shopping Experience',
            'Quarter': 'FY26 Q2',
            'Category': 'Technology',
            'Status': 'Research',
            'Priority': 'High',
            'Description': 'AI-powered personalized shopping recommendations'
        },
        {
            'Title': 'Staff Training Platform',
            'Quarter': 'FY26 Q3',
            'Category': 'People & Culture',
            'Status': 'Planning',
            'Priority': 'Medium',
            'Description': 'Digital platform for employee training and development'
        },
        {
            'Title': 'Sustainability Initiative',
            'Quarter': 'FY26 Q3',
            'Category': 'Corporate',
            'Status': 'Planning',
            'Priority': 'Low',
            'Description': 'Environmental sustainability and green practices program'
        }
    ]
    
    df = pd.DataFrame(sample_data)
    df.to_csv('sample_roadmap_data.csv', index=False)
    print("📝 Created sample CSV file: sample_roadmap_data.csv")
    print("   Use this as a template for your data structure")

def main():
    print("🚀 Me@Sams Roadmap Data Converter")
    print("=" * 50)
    
    # Try to convert existing Excel file
    success = convert_excel_to_csv()
    
    if not success:
        print("\n📝 Creating sample template instead...")
        create_sample_csv()
    
    print("\n" + "=" * 50)
    print("🎯 Next Steps:")
    print("1. Review the converted CSV file or use the sample template")
    print("2. Run 'python roadmap_visualizer.py' to create static charts")
    print("3. Open 'interactive_roadmap.html' in your browser for interactive view")
    print("4. Upload your CSV data to the interactive dashboard")

if __name__ == "__main__":
    main()