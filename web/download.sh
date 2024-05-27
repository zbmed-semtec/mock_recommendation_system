pip install gdown

mkdir -p data

cd data

gdown https://drive.google.com/uc?id=1vvNtObBs_7-5A5ibozHTeIpwJgYOVWxH -O relish_text.jsonl
gdown https://drive.google.com/uc?id=1OYwyZfvVG4ZGCjpLFpj1XH96s2mFyEZ2 -O relish_recoms.jsonl