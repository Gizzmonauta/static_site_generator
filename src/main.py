from textnode import TextNode, TextType

def main():
    print(TextNode("This is my anchor text", TextType.LINK, "https://example.com"))

if __name__ == "__main__":
    main()
