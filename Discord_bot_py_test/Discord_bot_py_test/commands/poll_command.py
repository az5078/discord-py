import interactions
import time

async def poll_command(ctx, duration, emoji_list):
    poll_embed = interactions.Embed(
        title = '투표하세요!', 
        color = interactions.Color.green(),
        description = "투표 보기는 " + " ".join(emoji_list) + " 입니다." + "\n이외의 이모지는 무시됩니다.\n" + "**남은 시간: {}초**".format(duration)
        )
    message = await ctx.send(embeds = poll_embed)
    for emoji in emoji_list:
        await message.create_reaction(emoji)
        
    while duration - 1:
        time.sleep(1)
        duration -= 1
        if duration > 10:
            embed_color = interactions.Color.green()
        else:
            embed_color = interactions.Color.red()

        poll_embed.color = embed_color
        poll_embed.description = "투표 보기는 " + " ".join(emoji_list) + " 입니다." + "\n이외의 이모지는 무시됩니다.\n" + "**남은 시간: {}초**".format(duration)

        await message.edit(embeds = poll_embed)
    
    time.sleep(1)
    poll_embed = interactions.Embed(
        title = '투표 종료', 
        color = 0xffd700,
        description = "투표 보기는 " + " ".join(emoji_list) + " 입니다." + "\n이외의 이모지는 무시됩니다.\n" + "**종료되었습니다.**".format(duration)
        )
    await message.edit(embeds = poll_embed)
    
    message = await ctx.channel.get_message(message.id)
    result = ''
    for reaction in message.reactions:
        number_reacted = reaction.count - 1
        result += '{} : {}\n'.format(reaction.emoji.name, number_reacted)

    poll_embed.add_field(
        name = '**투표 결과**',
        value = result,
        inline = False
        )

    await message.edit(embeds = poll_embed)