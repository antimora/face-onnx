#!/usr/bin/env python3


# This script converts initializers in an ONNX model to constants.

import onnx
from onnx import numpy_helper
import numpy as np

def convert_initializers_to_constants(model_path, output_path):
    # Load the model
    model = onnx.load(model_path)

    # Get all initializers
    initializers = {i.name: i for i in model.graph.initializer}

    # New list to hold updated nodes
    new_nodes = []

    # Set to keep track of processed initializers
    processed_initializers = set()

    # Iterate through all nodes in the graph
    for node in model.graph.node:
        constant_nodes = []
        if node.op_type in ['Mul', 'Add', 'Sub', 'Div']:
            for i, input_name in enumerate(node.input):
                if input_name in initializers and input_name not in processed_initializers:
                    # Convert initializer to constant
                    init = initializers[input_name]
                    tensor = numpy_helper.to_array(init)

                    # Create new constant node
                    constant_node = onnx.helper.make_node(
                        'Constant',
                        inputs=[],
                        outputs=[input_name],
                        value=onnx.helper.make_tensor(
                            name=input_name,
                            data_type=init.data_type,
                            dims=init.dims,
                            vals=tensor.flatten().tolist()
                        )
                    )

                    constant_nodes.append(constant_node)
                    processed_initializers.add(input_name)

        # Add constant nodes before the current node
        new_nodes.extend(constant_nodes)
        new_nodes.append(node)

    # Replace old nodes with new nodes
    del model.graph.node[:]
    model.graph.node.extend(new_nodes)

    # Remove processed initializers
    initializers_to_keep = [init for init in model.graph.initializer if init.name not in processed_initializers]
    del model.graph.initializer[:]
    model.graph.initializer.extend(initializers_to_keep)

    # Save the modified model
    onnx.save(model, output_path)
    print(f"Modified model saved to {output_path}")



# Usage
input_model = "face_detector_opt.onnx"
output_model = "face_detector_opt_transformed.onnx"
convert_initializers_to_constants(input_model, output_model)
