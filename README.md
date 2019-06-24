# block-producer-calculator-back

Block producer investments payback calculator.

  * [API](#api)
  * [Development](#development)
  * [Production](#production)

## API

`POST | /investments-payback/month` — calculate active block producer investments payback per month.

| Arguments                     | Type    | Required | Description                                                         |
| :---------------------------: | :-----: | :------: | ------------------------------------------------------------------- |
| money_per_month               | Integer | Yes      | How much money comes into blockchain per month.                     |
| token_price                   | Float   | Yes      | Token price.                                                        |
| active_block_producers_stakes | Integer | Yes      | Active block producers stakes number in the blockchain besides you. |
| active_block_producers_votes  | Integer | Yes      | Active block producers votes number in the blockchain besides you.  |
| stake                         | Integer | Yes      | Your block producer's stake number.                                 |
| votes                         | Integer | Yes      | Your block producer's votes number.                                 |

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
{
    "payback": 145774.64788732395
}
```

`GET | /token/price/usd` — get the price of the `Remme` token in dollars (USD).

```bash
$ curl 127.0.0.1:8000/token/price/usd -H "Accept: application/json" \
      -H "Content-type: application/json" | python -m json.tool
{
    "price": 0.0071
}
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
      -e COIN_MARKET_CAP_API_KEY='8d63f1d0-da4e-4422-ad30-be5c298e4c01' \
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

## Production

To build the project, use the following command:

```bash
$ docker build -t block-producer-calculator-back . -f Dockerfile.production
```

To run the project, use the following command. It will start the server and occupate current terminal session:

```bash
$ docker run -p 8000:8000 -e PORT=8000 -e COIN_MARKET_CAP_API_KEY='8d63f1d0-da4e-4422-ad30-be5c298e4c01' \
      -v $PWD:/block-producer-calculator-back \
      --name block-producer-calculator-back block-producer-calculator-back
```
