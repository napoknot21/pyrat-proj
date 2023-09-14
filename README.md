# PyRat Project

## Prerequisites
Ensure you have ```git``` and the lastest version of ```Python3```. If you haven't, you can download git [here](https://git-scm.com/downloads).

**Note**: If you are on ```Windows```, try to install ```python3``` from the ```Microsoft Store```, this avoid path errors

## Installation

First of all, open a terminal (yes, we need it)
    - **Windows**: Open `Git Bash` (yes, it's better than `cmd`)
    - **MAC**: Open `Terminal`
    - **Linux**: Open `Terminal`

Once done, you have to clone this repository ! (copy-paste this command)
```
git clone https://github.com/napoknot21/pyrat-project.git
```

Enter to the cloned directory
```
cd pyrat-project
```

Give execution permission to the ```setup.sh``` script !
```
chmod +x setup.sh
```

Finally, just run the installation script (It will automatically install packages, dependencies... all)
```
./setup.sh
```


### Note

This section is for troubleshooting. If the script executed without any issues, you can skip this section.

If the script does not execute on your device, there's an alternative version written in Python inside the `extras/` directory that performs the same tasks.

So, go the `extras/` directory
```
cd extras
```

Run the python script
```
python3 setup_altern.py
```
