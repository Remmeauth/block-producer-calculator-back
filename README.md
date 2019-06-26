# block-producer-calculator-back

Block producer investments payback calculator.

  * [API](#api)
  * [Development](#development)
  * [Production](#production)

## API

`POST | /investments-payback/month` — calculate active block producer investments payback per month.

| Arguments                     | Type    | Required | Description                                                        |
| :---------------------------: | :-----: | :------: | ------------------------------------------------------------------ |
| money_per_month               | Integer | Yes      | How much money comes into blockchain per month.                    |
| token_price                   | Float   | Yes      | Token price.                                                       |
| all_block_producers_stakes    | Integer | Yes      | All block producers stakes number in the blockchain besides you.   |
| active_block_producers_votes  | Integer | Yes      | Active block producers votes number in the blockchain besides you. |
| stake                         | Integer | Yes      | Your block producer's stake number.                                |
| votes                         | Integer | Yes      | Your block producer's votes number.                                |

```bash
$ curl -X POST 127.0.0.1:8000/profit/month \
      -H "Accept: application/json" \
      -H "Content-type: application/json" \
      -d $'{
            "economy": {
                "money_per_month": 50000,
                "token_price": 0.0071,
                "all_block_producers_stakes": 350000000,
                "active_block_producers_votes": 300000000
            },
            "block_producer": {
                "stake": 300000,
                "votes": 300000
            }
         }' | python -m json.tool
{
    "result": {
        "fiat": 39.964317726236075,
        "tokens": 5628.777144540292
    }
}
```

`POST | /profit/roi` — calculate returning on investment for 4 years.

```bash
$ curl -X POST 127.0.0.1:8000/profit/roi \
      -H "Accept: application/json" \
      -H "Content-type: application/json" \
      -d $'{
            "economy": {
                "money_per_month": 50000,
                "token_price": 0.0071,
                "all_block_producers_stakes": 350000000,
                "active_block_producers_votes": 300000000
            },
            "block_producer": {
                "stake": 300000,
                "votes": 300000
            }
         }' | python -m json.tool
{
    'result': {
        'percent': 26.220804592280146,
        'statistics_per_month': [
            {
                'block_producer_stake': 300000,
                'month': 1,
                'month_reward_in_fiat': 39.964317726236075,
                'month_reward_in_tokens': 5628.777144540292,
                'token_price': 0.0071,
                'token_price_growth_percent': 10
            },
            ...
            {
                'block_producer_stake': 378662.41377684043,
                'month': 48,
                'month_reward_in_fiat': 47.8153284351674,
                'month_reward_in_tokens': 347.90929819234447,
                'token_price': 0.13743619007484045,
                'token_price_growth_percent': 3.8692390084819794
            }
        ]
    }
}
```

`GET | /token/price/usd` — get the price of the `Remme` token in dollars (USD).

```bash
$ curl 127.0.0.1:8000/token/price/usd -H "Accept: application/json" \
      -H "Content-type: application/json" | python -m json.tool
{
    "result": 0.007113124
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
