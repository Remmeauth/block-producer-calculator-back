# block-producer-calculator-back

Block producer investments payback calculator.

  * [API](#api)
  * [Development](#development)

## API

`POST | /investments-payback/month` — calculate active block producer investments payback per month.

```bash
$ curl -X POST 127.0.0.1:8000/investments-payback/month \
      -H "Accept: application/json" \
      -H "Content-type: application/json" \
      -d $'{
            "economy": {
                "money_per_month": 50000,
                "token_price": 0.0071,
                "active_block_producers_stakes": 300000000,
                "active_block_producers_votes": 10000000
            },
            "block_producer": {
                "stake": 300000,
                "votes": 1000000
            }
         }' | python -m json.tool
```

## Development

Clone the project with the following command:

```bash
$ git clone https://github.com/remmeauth/block-producer-calculator-back.git
$ cd block-producer-calculator-back
```

To build the project, use the following command:

```bash
$ docker build -t block-producer-calculator-back . -f Dockerfile.development
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 8000:8000 -v $PWD:/block-producer-calculator-back \
      --name block-producer-calculator-back block-producer-calculator-back
```

If you need to enter the bash of the container, use the following command:

```bash
$ docker exec -it block-producer-calculator-back bash
```

Clean all containers with the following command:

```bash
$ docker rm $(docker ps -a -q) -f
```

Clean all images with the following command:

```bash
$ docker rmi $(docker images -q) -f
```
