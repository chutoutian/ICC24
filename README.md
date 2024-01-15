

## Prerequisites
Ubuntu 16.04 (or OSX), Tensorflow v1.1.0 or higher, TFLearn v0.3.1 
Python 3.5 or higher



##Train a model using certain physical layer traces:
* cooked_traces: training set
* cooked_test_traces: validation set
* In `sim`, run 
```
python3 multi_agent.py
```
  
* hyperparameter settings (line 15-18): 
  1. `LAYER` and `NEURON`: number of hidden layes and neurons, respectively.
  2. `SCHEME`: lower-layer information index (listed in `ENUM`), if `SCHEME` is empty, then it reduces to the baseline `pensieve`
  3. `EPOCHS`: Training epoches
  
##Test the model
* model is saved in ./model/`nn_model_layer={LAYER}_neuron={NEURON}_ep_{EPOCH}.ckpt`
* terminal run 
```
python rl_no_training.py SUBSET EPOCH BASE LAYER NEURON
```
  
  1. Change `SCHEME` based on the model in `rl_no_training.py`
  2. `SUBSET`: index of dataset (1-5)
  3. `BASE: folder name for the corresponding model 


  




## 