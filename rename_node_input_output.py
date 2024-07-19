#!/usr/bin/env python3

# This script renames the input and output nodes of an ONNX model.

import onnx
from onnx import numpy_helper
import numpy as np

def rename_node_io(model_path, output_path):
    # Load the ONNX model
    model = onnx.load(model_path)

    # Create a dictionary to store new names
    name_map = {}

    # Function to generate a new name
    def get_new_name(old_name):
        if old_name not in name_map:
            new_name = f"renamed_{len(name_map)}"
            name_map[old_name] = new_name
        return name_map[old_name]

    # Iterate through all nodes in the graph
    for node in model.graph.node:
        # Rename inputs
        for i, input_name in enumerate(node.input):
            if input_name.isdigit():
                new_name = get_new_name(input_name)
                node.input[i] = new_name

        # Rename outputs
        for i, output_name in enumerate(node.output):
            if output_name.isdigit():
                new_name = get_new_name(output_name)
                node.output[i] = new_name

    # Update initializers
    for initializer in model.graph.initializer:
        if initializer.name in name_map:
            initializer.name = name_map[initializer.name]

    # Update input names
    for input in model.graph.input:
        if input.name in name_map:
            input.name = name_map[input.name]

    # Update output names
    for output in model.graph.output:
        if output.name in name_map:
            output.name = name_map[output.name]

    # Save the modified model
    onnx.save(model, output_path)

    print(f"Model saved with renamed nodes to {output_path}")

# Example usage
input_model_path = "face_detector_opt_transformed.onnx"
output_model_path = "face_detector_opt_transformed_io_names.onnx"
rename_node_io(input_model_path, output_model_path)
