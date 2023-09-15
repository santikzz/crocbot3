async def process_manga():
    # load manga json
    f = open("mangas.json", "r")
    mangas = f.read()
    f.close()
    mangas = json.loads(mangas)
    pinged = False
    # croc-chat
    channel = client.get_channel(879174924277780500)
    for manga in mangas:
        # get manga info from lectormo
        data = scraper.get_manga_info(manga["url"])
        # check for new chapter
        if data["last_chapter_number"] > manga["last"]:
            manga["last"] = data["last_chapter_number"]
            if not pinged:
                await channel.send("<@&1066784707712397374> Nuevos capitulos!")
                pinged = True
            print(f"New chapter for {data['manga_title']}!")
            # send discord embed
            embed = discord.Embed(title=f"{data['manga_title']} (Nuevo capitulo {data['last_chapter_number']})", description=f"{data['last_chapter_title']}", url=manga["url"])
            embed.add_field(name="", value=data['manga_description'][:512])
            embed.set_image(url=data['manga_image'])
            await channel.send(embed=embed)
    # save manga json
    f = open("mangas.json", "w")
    f.write(json.dumps(mangas))
    f.close()