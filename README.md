
codes and dataset for IEEE ICC2024 
<!--- just
## Prerequisites
Ubuntu 16.04 (or mac), Tensorflow v1.5.0 or higher, 
Python 3.5 or higher



## Train a model using additional physical layer traces:
* In `sim`, training set is in `cooked_traces`, validation set is in `cooked_test_traces`, run 
```
python3 multi_agent.py
```
  
* hyperparameters (line 15-18): 
  1. `LAYER` and `NEURON`: number of hidden layes and neurons, respectively.
  2. `SCHEME`: lower-layer information index (listed in `ENUM`), if `SCHEME` is empty, then it reduces to the baseline `pensieve`
  3. `EPOCHS`: Training epoches
  
## Test the model
* An example model is saved in ./model/`nn_model_layer={LAYER}_neuron={NEURON}_ep_{EPOCH}.ckpt`
* terminal run 
```
python3 rl_no_training.py SUBSET EPOCH BASE LAYER NEURON
```
  
  1. Change `SCHEME` based on the model in `rl_no_training.py`
  2. `SUBSET`: index of dataset (1-5)
  3. `BASE: folder name for the corresponding model 



## Acknowledgements

Thanks [pensieve](https://github.com/hongzimao/pensieve) for open-sourcing codes of RL for adaptive video streaming

 ---> 
