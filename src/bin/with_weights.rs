use burn::{backend::ndarray::NdArray, tensor::Tensor};

use face_onnx::model::face_detector::Model;

fn main() {
    // Get image index argument (first) from command line
    type Backend = NdArray<f32>;

    // Get a default device for the backend
    let device = Default::default();

    // Create a new model and load the state
    let model: Model<Backend> = Model::default();

    print!("{}", model);
    let input = Tensor::ones([1, 3, 480, 640], &device);

    // Run the model on the input
    let (scores, boxes) = model.forward(input);

    assert_eq!(scores.dims(), [1, 17640, 2]);
    assert_eq!(boxes.dims(), [1, 17640, 4]);
}
