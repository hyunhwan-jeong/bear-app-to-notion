def main():
    import argparse

    parser = argparse.ArgumentParser(description="Import Bear App's markdown files to Notion.")
    parser.add_argument("-t", "--token", required=True, \
                        help="token_v2 value from your web cookie at notion.so(Can be found in your web browser inspector")
    parser.add_argument("-u", "--url", required=True, \
                        help="a hyperlink (i.e. https address) to your notion page to put the input markdown files.")
    parser.add_argument("-i", "--indir", required=True, \
                        help="path to where the markdown files are stored.")

    args = parser.parse_args()

    print(args)
    from notion.client import NotionClient
    from md2notion.upload import upload
    from notion.block import PageBlock
    import io
    from pathlib import Path
    import glob
    from tqdm import tqdm

    client = NotionClient(token_v2=args.token)
    print(client)
    print(args.url)
    page = client.get_block(args.url)

    for fname in tqdm(glob.glob("{args.indir}/**/*.md", recursive=True)):
        with open(fname, "r", encoding="utf-8") as mdFile:

            md_txt = mdFile.read().split("\n")
            page_title = md_txt[0].replace("#", "").strip()
            md_txt = "\n".join(md_txt[1:-1])

            mdFile = io.StringIO(md_txt)
            mdFile.__dict__["name"] = fname #Set this so we can resolve images later
            newPage = page.children.add_new(PageBlock, title=page_title)

            def convertImagePath(imagePath, mdFilePath):
                ret = Path(mdFilePath).parent / Path(mdFilePath).stem / Path(imagePath).name
                return ret
            upload(mdFile, newPage, imagePathFunc=convertImagePath)


if __name__ == "__main__":
    main()
