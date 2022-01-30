import os


def shell(cmd):
    print(cmd)
    status_code = os.system(cmd)

    if status_code != 0:
        exit(status_code)


shell('helm upgrade --install --create-namespace --namespace darkbot-prod darkbot . --values=darkbot_prod.yaml --values=secret_prod.yaml')