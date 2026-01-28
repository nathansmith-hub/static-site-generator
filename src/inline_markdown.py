import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        sections = old_node.text.split(delimiter)

        num_sections = len(sections)

        if num_sections % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        split_nodes = []
        for i in range(num_sections):
            if sections[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
            
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        image_list = extract_markdown_images(old_node.text)
        remaining_text = old_node.text

        for alt, url in image_list:
            markdown = f"![{alt}]({url})"

            sections = remaining_text.split(markdown, 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                split_nodes.append(TextNode(before, TextType.TEXT))

            split_nodes.append(TextNode(alt, TextType.IMAGE, url))

            remaining_text = after

        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_nodes)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        split_nodes = []
        link_list = extract_markdown_links(old_node.text)
        remaining_text = old_node.text

        for alt, url in link_list:
            markdown = f"[{alt}]({url})"

            sections = remaining_text.split(markdown, 1)
            before = sections[0]
            after = sections[1]

            if before != "":
                split_nodes.append(TextNode(before, TextType.TEXT))

            split_nodes.append(TextNode(alt, TextType.LINK, url))

            remaining_text = after

        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_nodes)
    
    return new_nodes
