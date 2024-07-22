Test repository to solve https://github.com/tracel-ai/burn/issues/1915 issue.

The original onnx file is transformed:

1. onnx-simplifier
2. onnx_initializers_to_consts.py
3. rename_node_input_output.py


To generate test data, run `gen_onnx_test_data.py` script.

To run the test, run:

```shell
cargo run --bin with_weights_test_outputs --release

```
