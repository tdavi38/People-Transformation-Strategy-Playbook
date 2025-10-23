import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

class RoadmapVisualizer:
    def __init__(self):
        self.fig_size = (16, 10)
        self.colors = {
            'Q1': '#FF6B6B',  # Red
            'Q2': '#4ECDC4',  # Teal
            'Q3': '#45B7D1',  # Blue
            'Q4': '#96CEB4',  # Green
            'Ongoing': '#FECA57',  # Yellow
            'Completed': '#A0A0A0'  # Gray
        }
        
    def parse_quarter(self, quarter_str):
        """Parse quarter string like 'FY26 Q1' to datetime"""
        try:
            if pd.isna(quarter_str) or quarter_str == '':
                return None
            
            # Handle different formats
            if 'FY' in str(quarter_str) and 'Q' in str(quarter_str):
                parts = str(quarter_str).replace('FY', '').strip().split()
                fy_year = int(parts[0])
                quarter = parts[1].replace('Q', '')
                
                # FY26 Q1 = Oct 2025, Q2 = Jan 2026, Q3 = Apr 2026, Q4 = Jul 2026
                base_year = 2000 + fy_year - 1
                quarter_months = {'1': 10, '2': 1, '3': 4, '4': 7}
                
                if quarter in ['2', '3', '4']:
                    base_year += 1
                    
                month = quarter_months.get(quarter, 1)
                return datetime(base_year, month, 1)
            
            return None
        except:
            return None
    
    def create_timeline_chart(self, data_file=None, sample_data=None):
        """Create a timeline/Gantt chart style roadmap"""
        
        if sample_data is not None:
            df = pd.DataFrame(sample_data)
        elif data_file:
            # Try to read the data file
            try:
                if data_file.endswith('.xlsx'):
                    df = pd.read_excel(data_file)
                elif data_file.endswith('.csv'):
                    df = pd.read_csv(data_file)
                else:
                    raise ValueError("Unsupported file format")
            except Exception as e:
                print(f"Error reading file: {e}")
                return self.create_sample_roadmap()
        else:
            return self.create_sample_roadmap()
        
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Try to identify relevant columns
        title_col = None
        quarter_col = None
        category_col = None
        status_col = None
        
        for col in df.columns:
            if any(word in col for word in ['title', 'name', 'feature', 'initiative']):
                title_col = col
            elif any(word in col for word in ['quarter', 'q1', 'q2', 'q3', 'q4', 'launch', 'release']):
                quarter_col = col
            elif any(word in col for word in ['category', 'team', 'area', 'domain']):
                category_col = col
            elif any(word in col for word in ['status', 'state']):
                status_col = col
        
        if not title_col or not quarter_col:
            print("Could not identify required columns. Creating sample roadmap...")
            return self.create_sample_roadmap()
        
        # Clean and prepare data
        df = df.dropna(subset=[title_col, quarter_col])
        df['parsed_date'] = df[quarter_col].apply(self.parse_quarter)
        df = df.dropna(subset=['parsed_date'])
        
        # Sort by date
        df = df.sort_values('parsed_date')
        
        # Create the visualization
        fig, ax = plt.subplots(figsize=self.fig_size)
        
        # Set up the plot
        y_pos = range(len(df))
        
        for i, (idx, row) in enumerate(df.iterrows()):
            date = row['parsed_date']
            title = row[title_col]
            
            # Determine color based on quarter
            quarter = f"Q{((date.month - 1) // 3) + 1}"
            color = self.colors.get(quarter, '#95A5A6')
            
            # Create bar for each item
            bar_height = 0.6
            rect = Rectangle((mdates.date2num(date), i - bar_height/2), 
                           30, bar_height, 
                           facecolor=color, alpha=0.7, edgecolor='black', linewidth=0.5)
            ax.add_patch(rect)
            
            # Add text label
            ax.text(mdates.date2num(date) + 15, i, title, 
                   ha='center', va='center', fontsize=8, weight='bold')
        
        # Format the plot
        ax.set_ylim(-0.5, len(df) - 0.5)
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"Item {i+1}" for i in range(len(df))])
        
        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.xticks(rotation=45)
        
        # Add grid and labels
        ax.grid(True, axis='x', alpha=0.3)
        ax.set_xlabel('Timeline', fontsize=12, weight='bold')
        ax.set_ylabel('Roadmap Items', fontsize=12, weight='bold')
        ax.set_title('Me@Sams Roadmap - Release Timeline by Quarter', 
                    fontsize=16, weight='bold', pad=20)
        
        # Add legend
        legend_elements = [Rectangle((0,0),1,1, facecolor=color, alpha=0.7, label=quarter) 
                          for quarter, color in self.colors.items() if quarter.startswith('Q')]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def create_sample_roadmap(self):
        """Create a sample roadmap to demonstrate the visualization"""
        sample_data = [
            {'title': 'Mobile App Enhancement', 'quarter': 'FY26 Q1', 'category': 'Technology', 'status': 'In Progress'},
            {'title': 'Member Rewards Program', 'quarter': 'FY26 Q1', 'category': 'Member Experience', 'status': 'Planning'},
            {'title': 'Inventory Management System', 'quarter': 'FY26 Q2', 'category': 'Operations', 'status': 'Planning'},
            {'title': 'Personalized Shopping Experience', 'quarter': 'FY26 Q2', 'category': 'Technology', 'status': 'Research'},
            {'title': 'Staff Training Platform', 'quarter': 'FY26 Q3', 'category': 'People & Culture', 'status': 'Planning'},
            {'title': 'Sustainability Initiative', 'quarter': 'FY26 Q3', 'category': 'Corporate', 'status': 'Planning'},
            {'title': 'Advanced Analytics Dashboard', 'quarter': 'FY26 Q4', 'category': 'Technology', 'status': 'Concept'},
            {'title': 'Customer Service AI', 'quarter': 'FY26 Q4', 'category': 'Technology', 'status': 'Research'},
            {'title': 'Supply Chain Optimization', 'quarter': 'FY27 Q1', 'category': 'Operations', 'status': 'Concept'},
            {'title': 'New Store Format Pilot', 'quarter': 'FY27 Q2', 'category': 'Retail', 'status': 'Concept'}
        ]
        
        return self.create_timeline_chart(sample_data=sample_data)
    
    def create_quarterly_view(self, data_file=None, sample_data=None):
        """Create a quarterly breakdown view"""
        
        if sample_data is not None:
            df = pd.DataFrame(sample_data)
        else:
            # Use sample data for demo
            sample_data = [
                {'title': 'Mobile App Enhancement', 'quarter': 'FY26 Q1', 'category': 'Technology'},
                {'title': 'Member Rewards Program', 'quarter': 'FY26 Q1', 'category': 'Member Experience'},
                {'title': 'Inventory Management System', 'quarter': 'FY26 Q2', 'category': 'Operations'},
                {'title': 'Personalized Shopping Experience', 'quarter': 'FY26 Q2', 'category': 'Technology'},
                {'title': 'Staff Training Platform', 'quarter': 'FY26 Q3', 'category': 'People & Culture'},
                {'title': 'Sustainability Initiative', 'quarter': 'FY26 Q3', 'category': 'Corporate'},
                {'title': 'Advanced Analytics Dashboard', 'quarter': 'FY26 Q4', 'category': 'Technology'},
                {'title': 'Customer Service AI', 'quarter': 'FY26 Q4', 'category': 'Technology'},
            ]
            df = pd.DataFrame(sample_data)
        
        # Group by quarter
        quarters = df['quarter'].unique()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        axes = axes.flatten()
        
        for i, quarter in enumerate(sorted(quarters)[:4]):
            ax = axes[i]
            quarter_data = df[df['quarter'] == quarter]
            
            # Create a simple list view for each quarter
            y_positions = range(len(quarter_data))
            
            for j, (idx, row) in enumerate(quarter_data.iterrows()):
                color = self.colors.get(quarter[-2:], '#95A5A6')
                
                # Create colored bar
                ax.barh(j, 1, color=color, alpha=0.7, height=0.6)
                
                # Add text
                ax.text(0.5, j, f"{row['title']}\n({row['category']})", 
                       ha='center', va='center', fontsize=9, weight='bold')
            
            ax.set_xlim(0, 1)
            ax.set_ylim(-0.5, len(quarter_data) - 0.5)
            ax.set_title(f'{quarter}', fontsize=14, weight='bold')
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Remove spines
            for spine in ax.spines.values():
                spine.set_visible(False)
        
        plt.suptitle('Me@Sams Roadmap - Quarterly Breakdown', fontsize=18, weight='bold')
        plt.tight_layout()
        return fig

def main():
    """Main function to create roadmap visualizations"""
    visualizer = RoadmapVisualizer()
    
    print("Creating Me@Sams Roadmap Visualizations...")
    
    # Try to use the Excel file if it exists
    excel_file = "FY26_27 Me@Sams Roadmap data file.xlsx"
    
    try:
        # Create timeline chart
        print("Generating timeline roadmap...")
        timeline_fig = visualizer.create_timeline_chart(excel_file)
        timeline_fig.savefig('roadmap_timeline.png', dpi=300, bbox_inches='tight')
        print("✓ Timeline roadmap saved as 'roadmap_timeline.png'")
        
        # Create quarterly view
        print("Generating quarterly breakdown...")
        quarterly_fig = visualizer.create_quarterly_view(excel_file)
        quarterly_fig.savefig('roadmap_quarterly.png', dpi=300, bbox_inches='tight')
        print("✓ Quarterly roadmap saved as 'roadmap_quarterly.png'")
        
        # Show the plots
        plt.show()
        
    except Exception as e:
        print(f"Note: Could not read Excel file directly. Error: {e}")
        print("Creating sample roadmap visualization...")
        
        # Create sample visualizations
        timeline_fig = visualizer.create_sample_roadmap()
        timeline_fig.savefig('sample_roadmap_timeline.png', dpi=300, bbox_inches='tight')
        
        quarterly_fig = visualizer.create_quarterly_view()
        quarterly_fig.savefig('sample_roadmap_quarterly.png', dpi=300, bbox_inches='tight')
        
        print("✓ Sample visualizations created")
        print("To use your actual data:")
        print("1. Export your Excel file to CSV format")
        print("2. Ensure columns include: Title/Name, Quarter/Launch Date, Category (optional)")
        print("3. Run this script again")
        
        plt.show()

if __name__ == "__main__":
    main()