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

| Arguments                     | Type    | Required | Description                                                        |
| :---------------------------: | :-----: | :------: | ------------------------------------------------------------------ |
| money_per_month               | Integer | Yes      | How much money comes into blockchain per month.                    |
| token_price                   | Float   | Yes      | Token price.                                                       |
| token_price_growth_percent    | Integer | Yes      | Token price growth percent.                                        |
| all_block_producers_stakes    | Integer | Yes      | All block producers stakes number in the blockchain besides you.   |
| active_block_producers_votes  | Integer | Yes      | Active block producers votes number in the blockchain besides you. |
| stake                         | Integer | Yes      | Your block producer's stake number.                                |
| votes                         | Integer | Yes      | Your block producer's votes number.                                |

```bash
$ curl -X POST 127.0.0.1:8000/profit/roi \
      -H "Accept: application/json" \
      -H "Content-type: application/json" \
      -d $'{
            "months": 12,
            "economy": {
                "money_per_month": 50000,
                "token_price": 0.0071,
                "token_price_growth_percent": 3,
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
        'percents': {
            'fiat': 64.73746422445299,
            'tokens': 19.00984920867224
        },
        'statistics_per_month': [
            {
                'block_producer_stake_in_fiat': 2130.0,
                'block_producer_stake_in_tokens': 300000,
                'month': 1,
                'month_reward_in_fiat': 39.964317726236075,
                'month_reward_in_tokens': 5628.777144540292,
                'token_price': 0.0071
            },
            ...
            {
                'block_producer_stake_in_fiat': 3508.9079879808487,
                'block_producer_stake_in_tokens': 357029.5476260167,
                'month': 12,
                'month_reward_in_fiat': 45.65658183829063,
                'month_reward_in_tokens': 4645.533258697715,
                'token_price': 0.009828060482143564
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
