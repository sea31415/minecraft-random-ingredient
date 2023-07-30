## Minecraft Random Ingredient

This is a python script that generates datapacks for Minecraft that randomize the crafting ingredients.
It's similar to [fasguy's](https://fasguy.net/minecraft_toolbox/info) [Crafting-Recipe Randomizer](https://fasguy.net/minecraft_toolbox/crafting-recipe-randomizer) but instead of randomizing the result of a crafting recipe, it randomizes the ingredients, while keeping the "shape" of the recipe the same.

For example, sticks may be swapped with nether quartz ore and diamonds may be swapped with cobblestone so that a diamond sword is crafted with two cobblestone on top of a nether quartz ore.
Additionally, ingredients are always swapped for all recipes, so in this example all recipes that use diamonds would use nether quartz ore instead.
(The example is in the "pre-made-datapacks" folder)

### Installation/Usage:
- You can just download one of the pre-made datapacks and add it to your world.
- If you want to generate your own:
1. Download the entire repository to your computer and unzip it.
2. Inside the folder, unzip "files.zip" into a folder called "files" (just rightclick and "Extract All...")
3. Run main.py
4. Follow the onscreen instructions

#### The program supports 2 command-line arguments for automation, both must be present if either one is needed:
- The first argument is the seed, which can either be a number, or "auto_seed" if you want a randomly generated seed.
- The second argument defines wether or not "show_notification" should be set true for all recipes (true/yes to enable) (currently unsupported)

So for example:
```
python main.py auto_seed false
```
```
python main.py 57483902 yes
```

### Current Problems (should still be playable with these existing):
- Because of how the recipe book works/seems to work, it unlocks more crafting recipes than I'd want. For example, holding a log is supposed to unlock only my new randomized recipes that use logs, but it also unlocks all the vanilla recipes that normally use logs which now of course dont use logs.
  (Is there a way to disable the auto-population of the recipe book?)
- Because of how the recipe book works/seems to work, and unlike the original random crafting, this requires a few thousand commands to run constantly (all done through the datapack) to unlock the crafting recipes to make this playable.
  (This does seem to make a perfomance impact on my computer but I'd be curious to see if it does on lower end hardware.)
- Some recipes do not have the "show_notification" set to true, which might be necessary for it to be playable (I will change this soon).
- The armor Trims may have to be taken out of the ingredients list.
- I lack the creativity to make a good pack.png haha.
