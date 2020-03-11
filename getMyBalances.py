import yaml

from ctapi import CTAPI

if __name__ == "__main__":

    with open("secrets.yml") as f:
        secrets = yaml.load(f, Loader=yaml.FullLoader)

        api_key = ""
        secret = ""

        if secrets:
            for key, value in secrets.items():
                if key.__eq__('secrets'):
                    api_key = value['key']
                    secret = value['secret']

        print(api_key)
        print(secret)

        api = CTAPI(api_key, secret)

        balances = api.getBalance()

        if balances['result']['success']:
            sum = 0
            print("+-------+------------+------------+------------+")
            print("|  SYM  |   amount   | price_fiat | value_fiat |")
            print("+-------+------------+------------+------------+")
            for b in balances['result']['details']:
                details = balances['result']['details'][b]
                if float(details['value_fiat']) > 0.01:
                    sum = sum + float(details['value_fiat'])
                    print("| %5s | %10.2f | %10.2f | %10.2f |" % (b, float(details['amount']),
                                                                  float(details['price_fiat']),
                                                                  float(details['value_fiat'])))

            print("+-------+------------+------------+------------+")
            print("")
            print("Sum: %15.2f EUR" % (sum))
            print("=" * 24)
        else:
            print("ERROR: Unable to get balances")
            print("\t Message: " + balances['result']['error'] + ", Reason: " + balances['result']['error_msg'])
