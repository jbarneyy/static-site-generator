from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode

import os
import shutil


def main():
    copy_src_to_dst("static", "public")


def copy_src_to_dst(src: str, dst: str):
    abs_src = os.path.abspath(src)
    abs_dst = None

    if os.path.exists(os.path.abspath(dst)):
        abs_dst = os.path.abspath(dst)
        shutil.rmtree(abs_dst)
        os.mkdir(abs_dst)
    else:
        os.mkdir(os.path.abspath(dst))
        abs_dst = os.path.abspath(dst)

    src_to_dst_helper(abs_src, abs_dst)


def src_to_dst_helper(src: str, dst: str):
    src_list = os.listdir(src)

    for item in src_list:
        item_src_path = os.path.join(src, item)
        item_dst_path = os.path.join(dst, item)

        if os.path.isfile(item_src_path):
            shutil.copy(item_src_path, item_dst_path)

            print(f"Copying file: {item_src_path} ---> {item_dst_path}")
        else:
            os.mkdir(item_dst_path)

            print(f"Creating new dir and recursing: {item_dst_path}")
            src_to_dst_helper(item_src_path, item_dst_path)



main()