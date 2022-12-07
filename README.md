# destboard

## Description

Electronic destination board (行先表示板) for Waveshare e-Paper display.

## Requirement

- [Raspberry Pi 4 Model B](https://www.amazon.com/dp/B07TD42S27/)
- [7.5inch E-Ink display HAT for Raspberry Pi](https://www.waveshare.com/7.5inch-e-paper-hat.htm)
- Python 3.9.2

## Usage

Run script as below,

```
$ uvicorn main:app --reload
```

and send HTTP request like

```
POST http://127.0.0.1:8000/0/0
{
  "name": "山田",
  "status": "10/30 休暇",
  "present": true
}
```

**PRESS Ctrl+C TO QUIT.**

## Install

Fork and clone this repository.

```
$ git clone git@github.com:[yourname]/destboard.git
```

Create python virtual env.

```
$ python3 -m venv .env
$ source ./.env/bin/activate
```

Install packages.

```
(.env)$ python -m pip install -r .\requirements.txt
```

This script uses demo code as SDK. You have to clone [waveshare/e-Paper](https://github.com/waveshare/e-Paper) and copy ``e-Paper/RaspberryPi_JetsonNano/python/lib/`` to top of this repo.

## Contribution

1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create new Pull Request

## License

MIT License

## Author

[minato](https://blog.minatoproject.com/)
