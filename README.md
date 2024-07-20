Test repository to solve https://github.com/tracel-ai/burn/issues/1915 issue.

The original onnx file is transformed:

1. onnx-simplifier
2. onnx_initializers_to_consts.py
3. rename_node_input_output.py

face_detector_opt_transformed_io_names.onnx is copied to `src/model/face-detector.onnx`

## Error 1

The onnx file builds however when loading weights, the following error is raised:

```
[face-onnx]% RUST_BACKTRACE=1 cargo run --bin with_weights


    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.18s
     Running `target/debug/face-onnx`
thread 'main' panicked at /Users/dilshod/.cargo/registry/src/index.crates.io-6f17d22bba15001f/rand-0.8.5/src/distributions/uniform.rs:998:1:
Uniform::new called with `low` non-finite.
stack backtrace:
   0: rust_begin_unwind
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/std/src/panicking.rs:652:5
   1: core::panicking::panic_fmt
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/panicking.rs:72:14
   2: core::panicking::panic
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/panicking.rs:146:5
   3: <rand::distributions::uniform::UniformFloat<f32> as rand::distributions::uniform::UniformSampler>::new
             at /Users/dilshod/.cargo/registry/src/index.crates.io-6f17d22bba15001f/rand-0.8.5/src/distributions/uniform.rs:832:17
   4: rand::distributions::uniform::Uniform<X>::new
             at /Users/dilshod/.cargo/registry/src/index.crates.io-6f17d22bba15001f/rand-0.8.5/src/distributions/uniform.rs:189:17
   5: burn_tensor::tensor::distribution::Distribution::sampler
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/distribution.rs:97:17
   6: <f32 as burn_tensor::tensor::element::base::ElementRandom>::random::{{closure}}
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/element/base.rs:151:54
   7: <f32 as burn_tensor::tensor::element::base::ElementRandom>::random
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/element/base.rs:125:17
   8: burn_tensor::tensor::data::TensorData::random
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/data.rs:205:23
   9: burn_ndarray::ops::tensor::<impl burn_tensor::tensor::ops::tensor::FloatTensorOps<burn_ndarray::backend::NdArray<E,Q>> for burn_ndarray::backend::NdArray<E,Q>>::float_random
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-ndarray/src/ops/tensor.rs:43:13
  10: <burn_tensor::tensor::api::kind::Float as burn_tensor::tensor::api::numeric::Numeric<B>>::random
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/api/numeric.rs:2754:32
  11: burn_tensor::tensor::api::numeric::<impl burn_tensor::tensor::api::base::Tensor<B,_,K>>::random
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-tensor/src/tensor/api/numeric.rs:666:19
  12: burn_core::nn::initializer::uniform_draw
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/nn/initializer.rs:186:5
  13: burn_core::nn::initializer::Initializer::init_tensor
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/nn/initializer.rs:135:17
  14: burn_core::nn::initializer::Initializer::init_with::{{closure}}
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/nn/initializer.rs:106:34
  15: <alloc::boxed::Box<F,A> as core::ops::function::Fn<Args>>::call
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/alloc/src/boxed.rs:2036:9
  16: burn_core::module::param::base::Uninitialized<P>::initialize
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/base.rs:83:9
  17: burn_core::module::param::base::Param<T>::val::{{closure}}
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/base.rs:124:30
  18: core::cell::once::OnceCell<T>::get_or_init::{{closure}}
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/cell/once.rs:162:50
  19: core::cell::once::OnceCell<T>::try_init
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/cell/once.rs:287:19
  20: core::cell::once::OnceCell<T>::get_or_try_init
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/cell/once.rs:239:9
  21: core::cell::once::OnceCell<T>::get_or_init
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/cell/once.rs:162:15
  22: burn_core::module::param::base::Param<T>::val
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/base.rs:115:9
  23: burn_core::module::param::tensor::<impl burn_core::module::base::Module<B> for burn_core::module::param::base::Param<burn_tensor::tensor::api::base::Tensor<B,_>>>::visit
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/tensor.rs:91:40
  24: burn_core::module::param::primitive::<impl burn_core::module::base::Module<B> for core::option::Option<T>>::visit
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/primitive.rs:20:13
  25: burn_core::module::base::Module::num_params
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/base.rs:49:9
  26: burn_core::module::param::primitive::<impl burn_core::module::base::Module<B> for core::option::Option<T>>::load_record
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/module/param/primitive.rs:29:27
  27: <burn_core::nn::conv::conv2d::Conv2d<B> as burn_core::module::base::Module<B>>::load_record
             at /Users/dilshod/.cargo/git/checkouts/burn-178c6829f420dae1/0d5025e/crates/burn-core/src/nn/conv/conv2d.rs:48:10
  28: <face_onnx::model::face_detector::Model<B> as burn_core::module::base::Module<B>>::load_record
             at ./target/debug/build/face-onnx-867926c7954c0d2f/out/model/face-detector.rs:13:10
  29: face_onnx::model::face_detector::Model<B>::from_file
             at ./target/debug/build/face-onnx-867926c7954c0d2f/out/model/face-detector.rs:85:9
  30: <face_onnx::model::face_detector::Model<B> as core::default::Default>::default
             at ./target/debug/build/face-onnx-867926c7954c0d2f/out/model/face-detector.rs:76:9
  31: face_onnx::main
             at ./src/main.rs:13:33
  32: core::ops::function::FnOnce::call_once
             at /rustc/129f3b9964af4d4a709d1383930ade12dfe7c081/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
[face-onnx]%
```

## Error 2

```
[face-onnx]% cargo run --bin without_weights

   Compiling face-onnx v0.1.0 (/Users/dilshod/Projects/face-onnx)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.96s
     Running `target/debug/without_weights`
thread 'main' panicked at /Users/dilshod/.cargo/registry/src/index.crates.io-6f17d22bba15001f/bytemuck-1.16.1/src/internal.rs:32:3:
cast_slice>PodCastError(TargetAlignmentGreaterAndInputNotAligned)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace

```
