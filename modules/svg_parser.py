#!/usr/bin/env python3
"""
SVG Parser Module
Handles SVG template parsing and text region identification for resume generation
"""

import xml.etree.ElementTree as ET
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class TextRegion:
    """Represents a text placement region in the SVG template"""
    id: str
    x: float
    y: float
    width: float
    height: float
    max_chars: int
    font_size: int
    region_type: str  # 'header', 'sidebar', 'main_content'

class SVGParser:
    """
    Parses SVG template and identifies text placement regions based on clip paths
    """
    
    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.tree = None
        self.root = None
        self.namespaces = {
            'svg': 'http://www.w3.org/2000/svg',
            'xlink': 'http://www.w3.org/1999/xlink'
        }
        self.text_regions = {}
        
    def load_svg(self) -> bool:
        """Load and parse the SVG file"""
        try:
            self.tree = ET.parse(self.svg_path)
            self.root = self.tree.getroot()
            return True
        except Exception as e:
            print(f"Error loading SVG: {e}")
            return False
    
    def extract_clip_paths(self) -> Dict[str, Dict]:
        """Extract clip path definitions and their coordinates"""
        clip_paths = {}
        
        # Try to find defs section with clip paths (with and without namespace)
        defs = self.root.find('.//defs') or self.root.find('.//svg:defs', self.namespaces)
        if defs is None:
            return clip_paths
            
        # Find all clipPath elements
        clip_path_elements = defs.findall('.//clipPath') or defs.findall('.//svg:clipPath', self.namespaces)
        
        for clip_path in clip_path_elements:
            clip_id = clip_path.get('id')
            if not clip_id:
                continue
                
            # Extract path data from child path element
            path = clip_path.find('.//path') or clip_path.find('.//svg:path', self.namespaces)
            if path is not None:
                path_data = path.get('d', '')
                coords = self._parse_path_coordinates(path_data)
                if coords:
                    clip_paths[clip_id] = coords
                    
        return clip_paths
    
    def _parse_path_coordinates(self, path_data: str) -> Optional[Dict]:
        """Parse SVG path data to extract bounding box coordinates"""
        try:
            # Clean path data - fix malformed numbers
            path_data = re.sub(r'(?<![0-9])\.', '0.', path_data)  # Fix leading dots
            path_data = re.sub(r'([0-9])\.([0-9])\.([0-9])', r'\1.\2\3', path_data)  # Fix double dots
            
            # Extract numbers from path
            numbers = re.findall(r'-?\d+\.?\d*', path_data)
            if len(numbers) < 4:
                return None
                
            # Convert to floats
            coords = []
            for num in numbers:
                try:
                    coords.append(float(num))
                except ValueError:
                    continue
                    
            if len(coords) < 4:
                return None
                
            # For rectangular paths, we expect: M x y h width v height H x2 Z
            # Or similar patterns. Extract bounding box.
            if 'M' in path_data and ('h' in path_data or 'H' in path_data):
                # Pattern like: M26.023 167.777h195.579v27.727H26.023
                x, y = coords[0], coords[1]
                if len(coords) >= 4:
                    width = abs(coords[2])
                    height = abs(coords[3])
                    return {
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height
                    }
            
            # Fallback: treat first 4 numbers as x, y, width, height
            if len(coords) >= 4:
                return {
                    'x': coords[0],
                    'y': coords[1], 
                    'width': abs(coords[2] - coords[0]) if coords[2] > coords[0] else abs(coords[2]),
                    'height': abs(coords[3] - coords[1]) if coords[3] > coords[1] else abs(coords[3])
                }
                
        except Exception as e:
            pass
            
        return None
    
    def identify_text_regions(self) -> Dict[str, TextRegion]:
        """
        Identify and categorize text regions based on Template.pdf analysis
        """
        clip_paths = self.extract_clip_paths()
        text_regions = {}
        
        for clip_id, coords in clip_paths.items():
            region = self._classify_region(clip_id, coords)
            if region:
                text_regions[clip_id] = region
                
        return text_regions
    
    def _classify_region(self, clip_id: str, coords: Dict) -> Optional[TextRegion]:
        """
        Classify clip path region based on position and size
        Based on Template.pdf layout analysis
        """
        x, y, width, height = coords['x'], coords['y'], coords['width'], coords['height']
        
        # Template dimensions: viewBox="0 0 594.96 842.25"
        # Left sidebar boundary approximately at x=258 (from SVG analysis)
        sidebar_boundary = 258
        
        # Classify based on position
        if x < sidebar_boundary:
            # Left sidebar regions
            region_type = 'sidebar'
            
            # Determine specific sidebar section based on Y position
            if y < 200:
                # Contact/header area
                if height > 100:
                    # Photo region
                    return TextRegion(clip_id, x, y, width, height, 0, 12, 'photo')
                else:
                    # Contact info
                    return TextRegion(clip_id, x, y, width, height, 90, 10, 'contact')
            elif y < 400:
                # Strengths/Skills area
                return TextRegion(clip_id, x, y, width, height, 200, 9, 'strengths')
            elif y < 600:
                # Education area  
                return TextRegion(clip_id, x, y, width, height, 100, 9, 'education')
            else:
                # Languages/Technical area
                return TextRegion(clip_id, x, y, width, height, 150, 9, 'technical')
                
        else:
            # Main content area
            region_type = 'main_content'
            
            if y < 150:
                # Header/Name area
                if height > 30:
                    return TextRegion(clip_id, x, y, width, height, 80, 18, 'name')
                else:
                    return TextRegion(clip_id, x, y, width, height, 100, 12, 'tagline')
            elif y < 300:
                # Bio section
                return TextRegion(clip_id, x, y, width, height, 400, 11, 'bio')
            else:
                # Experience sections
                return TextRegion(clip_id, x, y, width, height, 500, 10, 'experience')
        
        return None
    
    def get_region_by_type(self, region_type: str) -> List[TextRegion]:
        """Get all regions of a specific type"""
        return [region for region in self.text_regions.values() 
                if region.region_type == region_type]
    
    def add_text_to_svg(self, text_content: Dict[str, str]) -> str:
        """
        Add text content to SVG regions and return modified SVG string
        """
        if not self.root:
            return ""
            
        # Create text elements for each region
        for region_id, content in text_content.items():
            if region_id in self.text_regions:
                region = self.text_regions[region_id]
                self._create_text_element(region, content)
        
        # Return modified SVG as string
        return ET.tostring(self.root, encoding='unicode')
    
    def _create_text_element(self, region: TextRegion, content: str):
        """Create SVG text element for a region"""
        text_elem = ET.Element('text')
        text_elem.set('x', str(region.x + 5))  # Small padding
        text_elem.set('y', str(region.y + region.font_size))
        text_elem.set('font-family', 'Arial, sans-serif')
        text_elem.set('font-size', str(region.font_size))
        text_elem.set('fill', '#333333')
        
        # Handle multi-line text if needed
        lines = self._wrap_text(content, region.max_chars, region.width)
        
        for i, line in enumerate(lines):
            if i == 0:
                text_elem.text = line
            else:
                tspan = ET.SubElement(text_elem, 'tspan')
                tspan.set('x', str(region.x + 5))
                tspan.set('dy', str(region.font_size * 1.2))
                tspan.text = line
        
        self.root.append(text_elem)
    
    def _wrap_text(self, text: str, max_chars: int, max_width: float) -> List[str]:
        """Wrap text to fit within region constraints"""
        if len(text) <= max_chars:
            return [text]
            
        # Simple word wrapping
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if len(test_line) <= max_chars:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        return lines[:3]  # Limit to 3 lines max

def main():
    """Test the SVG parser"""
    parser = SVGParser("12.svg")
    
    if parser.load_svg():
        print("SVG loaded successfully")
        
        regions = parser.identify_text_regions()
        print(f"Found {len(regions)} text regions:")
        
        for region_id, region in regions.items():
            print(f"  - {region_id}: {region.region_type} ({region.width}x{region.height})")
    else:
        print("Failed to load SVG")

if __name__ == "__main__":
    main()