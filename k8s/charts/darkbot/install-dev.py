import os
import argparse


def shell(cmd):
    print(cmd)
    status_code = os.system(cmd)

    if status_code != 0:
        exit(status_code)


my_parser = argparse.ArgumentParser(description='')
my_parser.add_argument('--darkbot_image',
                       type=str,
                       help='darkbot_image',)
args = my_parser.parse_args()

shell(f'helm upgrade --install --create-namespace --namespace darkbot-dev darkbot . --values=darkbot_dev.yaml --values=secret_dev.yaml --set darkbot_image={args.darkbot_image}')
