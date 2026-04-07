# Install
Dit project is de uitvoering van Arthur Groot Zevert voor de warmte modellering van een huishouden. Voor meer informatie over de opdracht zie  [Opdracht uitleg](Opdracht_bescrhijving.md). 


## 1. Clone the repository
```bash
git clone https://github.com/AGrootZevert/assignment-CE-delft.git
```

## 2. Install UV
Uv is the package manager used in this project. It can be installed following the instructions here: [UV intallation](https://docs.astral.sh/uv/getting-started/installation/) 

(The requirements can be found in the [pyproject.toml](pyproject.toml))

## 3. Setup the virtual python enviroment
In the terminal run: 

For Linux
```bash
Make setup
```

Windows
```Powershell
./Make.ps1 setup
```

## 4. Setting up .env (Environment Variables)

Define the specific parameters of your local environment in a `.env` file.
If you haven't done before, create/update your `.env` file in the root, that is in the same folder as Makefile.

It should look like this:


```python
# path to the data storage
TEMPERATURE_DATA_PATH = "YOUR_PATH_TO_DATA_LOCATION"
```

## 5. Running the model
The example calculations can be done with the [script](scripts\heat_consumption_house.py). Here the temperature data is loaded and with it the power consumption is determined. Finally figures are generated and they are stored, together with the processed data in an `out/` folder.