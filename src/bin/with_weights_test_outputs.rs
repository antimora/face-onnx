use burn::module::Param;
use burn::prelude::*;
use burn::record::*;

use burn::{backend::ndarray::NdArray, tensor::Tensor};

use burn_import::pytorch::PyTorchFileRecorder;
use face_onnx::model::face_detector::Model;

#[derive(Debug, Module)]
struct TestData<B: Backend> {
    scores: Param<Tensor<B, 3>>,
    boxes: Param<Tensor<B, 3>>,
}

type B = burn::backend::NdArray;

fn main() {
    // Get image index argument (first) from command line
    type Backend = NdArray<f32>;

    // Get a default device for the backend
    let device = Default::default();

    // Create a new model and load the state
    let model: Model<Backend> = Model::default();

    let input = Tensor::ones([1, 3, 480, 640], &device);

    // Run the model on the input
    let (scores, boxes) = model.forward(input);

    assert_eq!(scores.dims(), [1, 17640, 2]);
    assert_eq!(boxes.dims(), [1, 17640, 4]);

    let test_data: TestDataRecord<B> = PyTorchFileRecorder::<FullPrecisionSettings>::new()
        .load("onnx_outputs.pt".into(), &Default::default())
        .unwrap();

    if scores.all_close(test_data.scores.val(), Some(1e-6), Some(1e-6)) {
        println!("Scores are about the same!");
    } else {
        println!("Scores are not the same!");
    }

    if boxes.all_close(test_data.boxes.val(), Some(1e-6), Some(1e-6)) {
        println!("Boxes are about the same!");
    } else {
        println!("Boxes are not the same!");
    }
}
