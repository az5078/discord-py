import interactions

async def delete_alert_role_func(ctx: interactions.CommandContext):
    role_list = await ctx.guild.get_all_roles()
    day_list = ['월', '화', '수', '목', '금']
    
    for day in day_list:
        if (day == '월' or day == '화'):
            for i in range(9):
                role_name = '{}.{}'.format(day, i+1)
                for role in role_list:
                    if role_name == role.name:
                        await ctx.guild.delete_role(role.id)

        else:
            for i in range(7):
                role_name = '{}.{}'.format(day, i+1)
                for role in role_list:
                    if role_name == role.name:
                        await ctx.guild.delete_role(role.id)

    role_delete_complete_embed = interactions.Embed(title = '**역할 제거가 완료되었습니다!**')

    await ctx.send(embeds = role_delete_complete_embed)


            

