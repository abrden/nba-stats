# nba-stats

## Usage
```
$ sudo docker-compose build

$ sudo docker-compose up --scale 1_mapper=2 --scale 2_mapper=2 --scale 31_mapper=2 --scale 32_mapper=2 --scale 1_reducer=2 --scale 2_reducer=2 --scale 31_reducer=2 --scale 32_reducer=2 --force-recreate
```