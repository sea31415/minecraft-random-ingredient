## Minecraft Random Ingredient

This is a python script that generates datapacks for Minecraft that randomize the crafting ingredients.
It's similar to [fasguy's](https://fasguy.net/minecraft_toolbox/info) [Crafting-Recipe Randomizer](https://fasguy.net/minecraft_toolbox/crafting-recipe-randomizer) but instead of randomizing the result of a crafting recipe, it randomizes the ingredients, while keeping the "shape" of the recipe the same.

For example, sticks may be swapped with nether quartz ore and diamonds may be swapped with cobblestone so that a diamond sword is crafted with two cobblestone on top of a nether quartz ore.
Additionally, ingredients are always swapped for all recipes, so in this example all recipes that use diamonds would use nether quartz ore instead.
(The example is in the "pre-made-datapacks" folder)

There is a cheatsheet included with every datapack that lists how all the ingredients got randomized.
This may for example include:
```
nether_quartz_ore is used for stick
cobblestone is used for diamond
```

### Installation/Usage:
- You can just download one of the pre-made datapacks and add it to your world.
  I recommend doing this, since it quite quickly can get very difficult/near impossible.
  (I will add ones in there that seem reasonably achievable to me, they'll be sorted into easy/medium/hard and i'll add more when i find time to find them. If you find ones (especially easy ones) please send me the seed and i'll add them to the folder :] )
- If you want to generate your own:
1. Have python 3.x installed (the easiest way on Windows is to download it through the [Microsoft Store](https://apps.microsoft.com/store/detail/python-311/9NRWMJP3717K?hl=en-us&gl=us))
2. Download the entire repository to your computer and unzip it.
3. Inside the folder, unzip "files.zip" into a folder called "files" (just rightclick and "Extract All...")
4. Run main.py
5. Follow the on-screen instructions

#### The program supports 2 command-line arguments for automation, both must be present if either one is needed:
- The first argument is the seed, which can either be a number, or "auto_seed" if you want a randomly generated seed.
- The second argument defines wether or not "show_notification" should be set true for all recipes (true/yes to enable) (currently unsupported!)

So for example:
```
python main.py
```
```
python main.py auto_seed false
```
```
python main.py 57483902 yes
```

### Other info:
- I will eventually make a "beginners tips" info file for this. If you've played randomized loot drops, or better yet randomized crafting, (or watched other people play them a lot) you wont need these.
- From tests it seems that on average, one of the ingredients gets mapped to itself, i have half-implemented an "all-random-shuffle" which is supposed to get around this, but I think it doesn't work properly so i need to do more tests. (If you know python, feel free to play around with it)

### Current Problems (should still be playable with these existing):
- Because of how the recipe book works/seems to work, it unlocks more crafting recipes than I'd want. For example, holding a log is supposed to unlock only my new randomized recipes that use logs, but it also unlocks all the vanilla recipes that normally use logs which now of course dont use logs.
  (Is there a way to disable the auto-population of the recipe book?)
- Because of how the recipe book works/seems to work, (and unlike the original random crafting,) this requires a few thousand commands to run constantly (all done through the datapack) to unlock the crafting recipes to make this playable.
  (This does not seem to make a perfomance impact on my computer but I'd be curious to see if it does on lower end hardware. On a self-hosted server with 2 players it gets kinda unplayable very quickly so in it's current iteration i would not recommend playing this in multiplayer, it is compatible though if you want to try)
- Some recipes do not have the "show_notification" set to true, which might be necessary for it to be playable (I will change this soon).
- The armor Trims may have to be taken out of the ingredients list.
- I lack the creativity to make a good pack.png haha.
