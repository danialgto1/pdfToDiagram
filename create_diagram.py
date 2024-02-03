import json
from graphviz import Digraph
from utils import format_long_text
import base64



def create_requirement_diagrams(json_data):
# List to store base64-encoded PNG images
    png_images_base64 = []
    for section_data in json_data:
        dot = Digraph(comment='SysML Diagram', format='png')
        dot.attr(rankdir='structs' , splines='ortho' , nodesep='1')
        section_name = section_data['section']
        spec_name = section_data['spec']['name']
        child_list = []
        # Section node with green rectangle
        dot.node(section_name, (f'{section_name}\n{format_long_text(spec_name)}'), shape='box',fontsize='22', color='lightgreen', style='filled'  )

        # Connect section node to requirements
        for requirement in section_data['spec']['requirements']:
            requirement_id = requirement['id']

            # Requirement node with attributes
            requirement_label = (f"{requirement_id}\n{format_long_text(requirement['shall'])}")
            if 'attributes' in requirement:
                attributes = "\n".join([f"{attr['name']}:\t {attr['value']}" for attr in requirement['attributes']]).upper()
                requirement_label += f"\n\n{attributes}"
            if requirement.get('child', None):
                child_list +=  requirement.get('child', None).get('ids')
            if requirement_id not in child_list:
                dot.node(requirement_id, requirement_label, shape='box', color='lightblue', style='filled')
                dot.edge(section_name, requirement_id)
            else:
                dot.node(requirement_id, requirement_label, shape='box', color='lightyellow', style='filled')

            # Connect child requirements to their parent
            if 'child' in requirement:
                for child_id in requirement['child']['ids']:
                    dot.edge(requirement_id, child_id)
    
    
        # Use the pipe method to capture the binary PNG data
        png_data = dot.pipe(format='png')
        dot.render(f'd/{section_name}', cleanup=True)

        # Convert binary data to base64
        png_base64 = base64.b64encode(png_data).decode()
    
        # Append base64-encoded PNG to the list
        png_images_base64.append(png_base64)
  
    return png_images_base64