# localpilot
_Any way you want it, that's the way you need it_

## Installation 
1. First, open VS Code and add the following to your settings.json file: 
```json
    "github.copilot.advanced": {
        "debug.testOverrideProxyUrl": "http://localhost:5001",
        "debug.overrideProxyUrl": "http://localhost:5001"

    }
```

2. Create a virtualenv to run this Python process, install the requirements, and download the models. 
```python
virtualvenv venv
source venv/bin/activate
pip install -r requirements.txt
# First setup run. This will download several models to your ~/models folder.
python app.py --setup 
``` 

3. Run it! 
```python
python app.py
```

Enjoy your on-device Copilot! 

## Caveat FAQ

**Is the code as good as GitHub Copilot?** For simple line completions yes. For simple function completions, yes. For complex functions... maybe. 

**Is it as fast as GitHub Copilot?** On my Macbook Pro with an Apple M2 Max, the 7b models are roughly as fast. The 34b models are not. Please consider this repo a demonstration of a very inefficient implementation. I'm sure we can make it faster; please do submit a pull request if you'd like to help. For example, I think we need debouncer because sometimes llama.cpp/GGML isn't fast at interrupting itself when a newer request comes in.

**Can this be packaged as a simple Mac app?** Yes!, I'm sure it can be, I just haven't had the time. 

**Is it good?** Only if your network is bad. I don't think it's competitive if you have fast Internet.

