#!/usr/bin/env python3

import onnxruntime
import numpy as np
import torch

def test_onnx_model(model_path, output_path):
    # Create an ONNX Runtime session
    session = onnxruntime.InferenceSession(model_path)

    # Get the input name
    input_name = session.get_inputs()[0].name

    # Create a dummy input tensor filled with ones
    input_data = np.ones((1, 3, 480, 640), dtype=np.float32)

    # Run inference
    (scores, boxes) = session.run(None, {input_name: input_data})

    # print(f"Output type: {type(outputs)}")

    # # Print the output shape(s)
    # for i, output in enumerate(outputs):
    #     print(f"Output {i} shape: {output.shape}")

    # # Convert outputs to PyTorch tensors
    # torch_outputs = [torch.from_numpy(output) for output in outputs]

    # (scores, boxes) = torch_outputs

    torch_outputs = {
        "scores": torch.from_numpy(scores),
        "boxes": torch.from_numpy(boxes)
    }

    # Save outputs to a PyTorch file
    torch.save(torch_outputs, output_path)
    print(f"Outputs saved to {output_path}")

    return torch_outputs

if __name__ == "__main__":
    model_path = "face_detector_opt_transformed_io_names.onnx"
    output_path = "onnx_outputs.pt"
    results = test_onnx_model(model_path, output_path)
