# -*- coding: utf-8 -*-

import yaml


def main():
    with open("config.yaml", "r", encoding='utf-8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    load_dir = config["load_dir"]
    preprocessing = config["preprocessing"]
    word_num = config["word_num"]
    word_order = config["word_order"]


if __name__ == "__main__":
    main()

