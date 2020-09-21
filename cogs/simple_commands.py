# coding=utf-8
import asyncio
import time
import datetime
import traceback
from json import load
from typing import List, Optional

import discord
from discord.ext import commands

from utils.cog_class import Cog
from utils.ctx_class import MyContext

mod_list_file = open("parsed_mod_list.json", "r")
mod_list = load(mod_list_file)
mod_list_file.close()

total_mods = len(mod_list)
numbers = [str(i) for i in range(total_mods)]
strings = ["next", "previous", "end", "start", "quit"]
items = numbers + strings


def mod_details_embed(mod: dict) -> discord.Embed:
    mod_embed = discord.Embed(title=mod["name"],
                              description=mod["short_description"],
                              url=mod["url"],
                              timestamp=datetime.datetime.strptime(mod["date_modified"], "%Y-%m-%dT%H:%M:%S"))
    mod_embed.add_field(name="Downloads", value=mod["downloads"])
    mod_embed.add_field(name="Internal ID", value=mod["id"])
    if mod["latest_supported_version"] is not None:
        mod_embed.add_field(name="Latest Supported Version", value=mod["latest_supported_version"])
    mod_embed.set_footer(text="Mod was last updated at")
    return mod_embed


class SimpleCommands(Cog):
    @commands.command()
    async def ping(self, ctx: MyContext):
        """
        Check that the bot is online, give the latency between the bot and discord servers.
        """
        _ = await ctx.get_translate_function()

        t_1 = time.perf_counter()
        await ctx.trigger_typing()  # tell Discord that the bot is "typing", which is a very simple request
        t_2 = time.perf_counter()
        time_delta = round((t_2 - t_1) * 1000)  # calculate the time needed to trigger typing
        await ctx.send(_("Pong. — Time taken: {miliseconds}ms", miliseconds=time_delta))  # send a message telling the
        # user the calculated ping time

    @commands.group()
    async def search(self, ctx: MyContext):
        """
        Search through the mod list for something
        """
        _ = await ctx.get_translate_function()

        if ctx.invoked_subcommand is None:
            await ctx.send(_("Do `fmhelp search` for a list of subcommands!"))

    @search.command(name="name")
    async def _name(self, ctx: MyContext, *name):
        """
        Search through the mod list for a mod with <name> in it's name
        """
        search_query = " ".join(name)
        search_query = search_query.lower()
        temp_mod_list: List[dict] = []
        for mod in mod_list:
            if search_query in mod["name"].lower():
                temp_mod_list.append(mod)
        if len(temp_mod_list) == 0:
            await ctx.send("Didn't find any matching mods.")
            return
        search_result_embed = discord.Embed(title="Search Results!",
                                            description=f"I found {len(temp_mod_list)} mods matching your query. "
                                                        f"Type `next` to flip to the next page, and `previous` "
                                                        f"to flip to the previous page. Type `end` to go to the end, "
                                                        f"and `start` to go to the start. Type a number to go to that "
                                                        f"mod. Type `quit` to quit.")
        await ctx.send(embed=search_result_embed)
        results_message: discord.Message = await ctx.send(embed=mod_details_embed(temp_mod_list[0]))

        def param(m):
            return m.content.lower().strip() in items and \
                   m.channel == ctx.channel and m.author.id == ctx.author.id

        current_mod = 0
        end_of_list = len(temp_mod_list) - 1
        while True:
            try:
                msg: discord.Message = await self.bot.wait_for(event="message", check=param, timeout=120)
            except asyncio.TimeoutError:
                await results_message.edit(content="Timed out waiting for response.")
                break
            msg_content: str = msg.content.lower()
            await msg.delete()
            if msg_content.isdigit():
                msg_content_int = int(msg_content) - 1
                if not -1 < msg_content_int < end_of_list + 1:
                    await ctx.send("Out of bounds.", delete_after=15)
                else:
                    current_mod = msg_content_int
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "next":
                if current_mod + 1 >= end_of_list:
                    await ctx.send("Reached end of list.", delete_after=15)
                else:
                    current_mod += 1
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "previous":
                if current_mod - 1 < 0:
                    await ctx.send("Reached end of list.", delete_after=15)
                else:
                    current_mod -= 1
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "end":
                current_mod = end_of_list
                await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "start":
                current_mod = 0
                await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "quit":
                await results_message.edit(content="Exited!")
                break

    @search.command(name="description", aliases=["desc"])
    async def _desc(self, ctx: MyContext, *name):
        search_query = " ".join(name)
        search_query = search_query.lower()
        temp_mod_list: List[dict] = []
        for mod in mod_list:
            if search_query in mod["short_description"].lower():
                temp_mod_list.append(mod)
        if len(temp_mod_list) == 0:
            await ctx.send("Didn't find any matching mods.")
            return
        search_result_embed = discord.Embed(title="Search Results!",
                                            description=f"I found {len(temp_mod_list)} mods matching your query. "
                                                        f"Type `next` to flip to the next page, and `previous` "
                                                        f"to flip to the previous page. Type `end` to go to the end, "
                                                        f"and `start` to go to the start. Type a number to go to that "
                                                        f"mod. Type `quit` to quit.")
        await ctx.send(embed=search_result_embed)
        results_message: discord.Message = await ctx.send(embed=mod_details_embed(temp_mod_list[0]))

        def param(m):
            return m.content.lower().strip() in items and \
                   m.channel == ctx.channel and m.author.id == ctx.author.id

        current_mod = 0
        end_of_list = len(temp_mod_list) - 1
        while True:
            try:
                msg: discord.Message = await self.bot.wait_for(event="message", check=param, timeout=120)
            except asyncio.TimeoutError:
                await results_message.edit(content="Timed out waiting for response.")
                break
            msg_content: str = msg.content.lower()
            await msg.delete()
            if msg_content.isdigit():
                msg_content_int = int(msg_content) - 1
                if not -1 < msg_content_int < end_of_list + 1:
                    await ctx.send("Out of bounds.", delete_after=15)
                else:
                    current_mod = msg_content_int
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "next":
                if current_mod + 1 >= end_of_list:
                    await ctx.send("Reached end of list.", delete_after=15)
                else:
                    current_mod += 1
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "previous":
                if current_mod - 1 < 0:
                    await ctx.send("Reached end of list.", delete_after=15)
                else:
                    current_mod -= 1
                    await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "end":
                current_mod = end_of_list
                await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "start":
                current_mod = 0
                await results_message.edit(embed=mod_details_embed(temp_mod_list[current_mod]))
            elif msg_content == "quit":
                await results_message.edit(content="Exited!")
                break

    @commands.command(name="info")
    async def _info(self, ctx: MyContext, mod_id: int, channel_to_send_to: Optional[discord.TextChannel]):
        for mod in mod_list:
            if mod["id"] == mod_id:
                actual_mod = mod
                break
        else:
            await ctx.send("Didn't find a mod with that ID.")
            return
        if channel_to_send_to is not None:
            try:
                msg = await channel_to_send_to.send(embed=mod_details_embed(actual_mod))
                await msg.add_reaction("✔")
                await msg.add_reaction("🚫")
            except discord.DiscordException as exception:
                await ctx.send("Message failed to send! ```{}```".format("".join(traceback.format_exception(
                    type(exception), exception, exception.__traceback__))))
            else:
                await ctx.send("Sent message to that channel.")

        else:
            await ctx.send(embed=mod_details_embed(actual_mod))


setup = SimpleCommands.setup
